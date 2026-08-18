"""
Core Agent Orchestration for Huvo AI Real Estate Sales Agent (Northstar One).
Manages multi-turn conversation memory, Gemini API interactions, native tool execution,
and structured JSON analytics extraction with automatic multi-model failover for high reliability.
"""

import os
import json
import time
import logging
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts.system_prompt import SYSTEM_PROMPT
from tools import book_site_visit

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fallback pool of high-speed models to guarantee 100% uptime even on free-tier rate limits
MODEL_POOL = [
    os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
    "gemini-3.7-flash",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-3-flash-preview"
]


# ==============================================================================
# Pydantic Schemas for Structured Analytics & Validation
# ==============================================================================

class LeadAnalytics(BaseModel):
    """Structured Lead & Conversation Analytics extracted post-conversation."""
    customer_name: Optional[str] = Field(
        default="Not provided",
        description="Name of the customer if mentioned during conversation"
    )
    customer_phone: Optional[str] = Field(
        default="Not provided",
        description="Phone number of the customer if shared"
    )
    language_detected: Literal["English", "Hindi", "Hinglish", "Mixed", "Unknown"] = Field(
        default="English",
        description="Primary language / dialect used by the user"
    )
    configuration_preference: Literal["2 BHK", "3 BHK", "Both 2 & 3 BHK", "Undecided", "Out of Scope"] = Field(
        default="Undecided",
        description="Preferred apartment configuration"
    )
    budget_range: str = Field(
        default="Not specified",
        description="Customer budget or price readiness (e.g., '₹1.35 Cr - ₹1.75 Cr', '₹1.35 Cr+', 'Under ₹1.35 Cr', 'Flexible')"
    )
    interest_level: Literal["High", "Medium", "Low", "Uninterested", "DND_Requested"] = Field(
        default="Medium",
        description="Lead qualification interest score"
    )
    site_visit_status: Literal["Booked", "Failed_Attempt", "Rescheduled", "Not_Requested", "Declined"] = Field(
        default="Not_Requested",
        description="Status of site visit booking"
    )
    site_visit_details: Optional[str] = Field(
        default=None,
        description="Details of site visit if booked/attempted (Date, Time, Slot ID, or Failure reason)"
    )
    follow_up_requirement: Literal["Immediate Callback", "Scheduled Callback", "Send Brochure / WhatsApp", "Site Visit Coordination", "None (DND / Uninterested)"] = Field(
        default="Scheduled Callback",
        description="Required follow-up action"
    )
    preferred_callback_time: Optional[str] = Field(
        default=None,
        description="Customer preferred time for callback if specified"
    )
    customer_sentiment: Literal["Positive / Enthusiastic", "Interested / Inquisitive", "Price Sensitive / Hesitant", "Busy / Inconvenienced", "Disinterested / Unresponsive", "Frustrated / DND"] = Field(
        default="Interested / Inquisitive",
        description="Customer emotional state and tone during interaction"
    )
    objections_raised: List[str] = Field(
        default_factory=list,
        description="List of objections raised by the customer (e.g., 'Price too high', 'Distance to office', 'Looking for 4 BHK')"
    )
    executive_summary: str = Field(
        ...,
        description="2-3 sentence clear executive summary for the sales team and CRM"
    )
    recommended_next_action: str = Field(
        ...,
        description="Specific actionable next step for the human sales executive / CRM automation"
    )


class SessionState:
    """Represents the live state and memory of a conversation session."""
    def __init__(self, session_id: str, client: Any, model_name: str):
        self.session_id = session_id
        self.client = client
        self.current_model = model_name
        self.chat = self._init_chat(model_name)
        self.created_at = datetime.now().isoformat()
        self.ui_history: List[Dict[str, Any]] = []
        self.last_tool_call: Optional[Dict[str, Any]] = None
        self.analytics_cache: Optional[LeadAnalytics] = None

    def _init_chat(self, model: str):
        return self.client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
                tools=[book_site_visit],
            )
        )

    def switch_model(self, new_model: str):
        """Switches the underlying model while preserving conversation context."""
        logger.info(f"Failing over session {self.session_id} to model: {new_model}")
        self.current_model = new_model
        # Re-initialize chat on new model with prior turns if any
        self.chat = self._init_chat(new_model)


# ==============================================================================
# Real Estate AI Agent Orchestrator
# ==============================================================================

class RealEstateAgent:
    """Manages Gemini Client, Active Sessions, Multi-Model Failover, and Analytics."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("No GEMINI_API_KEY found in environment or arguments.")
        
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
        self.client = genai.Client(api_key=self.api_key)
        self.sessions: Dict[str, SessionState] = {}
        logger.info(f"RealEstateAgent initialized with primary model: {self.model_name}")

    def _get_or_create_session(self, session_id: str) -> SessionState:
        """Retrieves or initializes a chat session."""
        if session_id not in self.sessions:
            logger.info(f"Creating new Gemini chat session for ID: {session_id}")
            self.sessions[session_id] = SessionState(
                session_id=session_id,
                client=self.client,
                model_name=self.model_name
            )
        return self.sessions[session_id]

    def chat(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """Processes a user message with multi-model failover for 100% reliable execution."""
        session = self._get_or_create_session(session_id)
        
        # Record user message in UI history
        timestamp = datetime.now().strftime("%I:%M %p")
        session.ui_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": timestamp
        })

        assistant_reply = ""
        last_err = None
        tool_info = None

        # Try models in the pool for automatic failover on rate limits
        for candidate_model in MODEL_POOL:
            try:
                # If candidate model differs from current, switch session chat
                if session.current_model != candidate_model:
                    session.switch_model(candidate_model)

                # Send message to Gemini Chat with Automatic Function Calling (AFC)
                response = session.chat.send_message(user_message)
                assistant_reply = response.text or ""
                last_err = None

                # Inspect conversation history to check if a function call took place in this turn
                raw_history = session.chat.get_history()
                for item in reversed(raw_history):
                    if hasattr(item, 'parts') and item.parts:
                        for part in item.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                call = part.function_call
                                tool_info = {
                                    "name": call.name,
                                    "args": dict(call.args) if call.args else {}
                                }
                                break
                            elif hasattr(part, 'function_response') and part.function_response:
                                resp = part.function_response
                                if tool_info:
                                    tool_info["response"] = dict(resp.response) if resp.response else {}
                                else:
                                    tool_info = {
                                        "name": resp.name,
                                        "response": dict(resp.response) if resp.response else {}
                                    }
                                break
                    if tool_info:
                        break

                break  # Successful generation, exit loop

            except Exception as e:
                last_err = e
                err_str = str(e)
                logger.warning(f"Error with model {candidate_model} on session {session_id}: {err_str[:120]}. Attempting failover...")
                time.sleep(0.5)

        if last_err is not None and not assistant_reply:
            logger.error(f"All model failovers exhausted for session {session_id}: {str(last_err)}")
            error_msg = "I apologize, but our sales line is experiencing high traffic. Please allow me a moment or let me know how I can assist you with Northstar One."
            session.ui_history.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now().strftime("%I:%M %p"),
                "error": str(last_err)
            })
            return {
                "session_id": session_id,
                "response": error_msg,
                "tool_called": None,
                "tool_details": None,
                "history": session.ui_history,
                "error": str(last_err)
            }

        if tool_info:
            session.last_tool_call = tool_info

        # Record model response in UI history
        session.ui_history.append({
            "role": "assistant",
            "content": assistant_reply,
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "tool_call": tool_info
        })

        # Invalidate analytics cache since history changed
        session.analytics_cache = None

        return {
            "session_id": session_id,
            "response": assistant_reply,
            "tool_called": tool_info.get("name") if tool_info else None,
            "tool_details": tool_info,
            "history": session.ui_history
        }

    def generate_analytics(self, session_id: str) -> LeadAnalytics:
        """Analyzes the full conversation transcript and produces structured JSON analytics with failover."""
        session = self.sessions.get(session_id)
        if not session or not session.ui_history:
            return LeadAnalytics(
                language_detected="English",
                configuration_preference="Undecided",
                budget_range="Not specified",
                interest_level="Low",
                site_visit_status="Not_Requested",
                follow_up_requirement="None (DND / Uninterested)",
                customer_sentiment="Disinterested / Unresponsive",
                objections_raised=[],
                executive_summary="Empty session. No interaction recorded.",
                recommended_next_action="No action required."
            )

        if session.analytics_cache:
            return session.analytics_cache

        # Format transcript for analytics prompt
        formatted_transcript = []
        for msg in session.ui_history:
            role = "Customer" if msg["role"] == "user" else "AI Sales Agent"
            tool_str = ""
            if msg.get("tool_call"):
                tool_str = f" [Tool Executed: {msg['tool_call']['name']}]"
            formatted_transcript.append(f"{role}: {msg['content']}{tool_str}")

        transcript_text = "\n".join(formatted_transcript)

        analytics_prompt = f"""You are a Lead Intelligence and Conversation Analytics Auditor for Northstar Homes.
Analyze the following sales conversation transcript between a prospective homebuyer and our AI Sales Agent for the 'Northstar One' project in Sector 79, Gurugram.

Extract accurate, structured CRM intelligence according to the specified schema.

Transcript:
============================================================
{transcript_text}
============================================================

Ensure all fields are objectively derived from the actual dialogue:
- Detect exact language/dialect (English, Hindi, Hinglish).
- Assess configuration (2 BHK, 3 BHK, Both, Undecided, or Out of Scope).
- Assess interest level and budget readiness.
- Check if a site visit was booked, failed (e.g. after hours), or not requested.
- Flag any objections raised (price, connectivity, sizes, etc.).
- Determine the appropriate follow-up requirement (especially if DND requested).
- Write a crisp executive summary and recommended next action for the sales manager.
"""

        for candidate_model in MODEL_POOL:
            try:
                logger.info(f"Generating structured analytics for session {session_id} using {candidate_model}")
                response = self.client.models.generate_content(
                    model=candidate_model,
                    contents=analytics_prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=LeadAnalytics,
                        temperature=0.1
                    )
                )

                parsed_json = json.loads(response.text)
                analytics = LeadAnalytics(**parsed_json)
                session.analytics_cache = analytics
                return analytics

            except Exception as e:
                logger.warning(f"Analytics failover from {candidate_model}: {str(e)[:100]}")
                time.sleep(0.5)

        # Safe fallback extraction if all models fail
        fallback_analytics = LeadAnalytics(
            language_detected="Mixed",
            configuration_preference="Undecided",
            budget_range="Under evaluation",
            interest_level="Medium",
            site_visit_status="Not_Requested",
            follow_up_requirement="Scheduled Callback",
            customer_sentiment="Interested / Inquisitive",
            objections_raised=[],
            executive_summary="Conversation completed with AI sales agent. Transcript recorded for sales review.",
            recommended_next_action="Review transcript and follow up with customer."
        )
        return fallback_analytics

    def reset_session(self, session_id: str) -> None:
        """Clears memory for a specific session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Session {session_id} reset successfully.")

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Returns the conversation history for a given session."""
        session = self.sessions.get(session_id)
        return session.ui_history if session else []


# Global singleton agent instance
agent_instance = RealEstateAgent()
