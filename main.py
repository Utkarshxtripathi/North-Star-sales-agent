"""
FastAPI Server for Huvo AI Real Estate Conversational Agent (Northstar One).
Provides REST endpoints for interactive chat, conversation memory, tool status,
and structured lead analytics extraction.
"""

import os
import uvicorn
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent import agent_instance, LeadAnalytics

# Initialize FastAPI App
app = FastAPI(
    title="Huvo AI - Northstar One Sales Agent API",
    description="Conversational Real Estate AI Agent with Dual Voice/Chat Prompting, Function Calling, and Structured CRM Analytics.",
    version="1.0.0"
)

# Enable CORS for cross-origin integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Templates & Static Directory
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
templates_dir = os.path.join(current_dir, "templates")

os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)


# ==============================================================================
# Request & Response Schemas
# ==============================================================================

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the user session")
    message: str = Field(..., description="Customer message text in English, Hindi, or Hinglish")


class ChatResponse(BaseModel):
    session_id: str
    response: str
    tool_called: Optional[str] = None
    tool_details: Optional[Dict[str, Any]] = None
    history: List[Dict[str, Any]]


class AnalyticsRequest(BaseModel):
    session_id: str = Field(..., description="Session ID whose transcript is to be analyzed")


class ResetSessionRequest(BaseModel):
    session_id: str = Field(..., description="Session ID to reset")


# ==============================================================================
# API Endpoints
# ==============================================================================

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    """Renders the conversational web application interface."""
    return templates.TemplateResponse(request=request, name="index.html")



@app.get("/api/health")
async def health_check():
    """Health check endpoint confirming server and model configuration."""
    return {
        "status": "healthy",
        "service": "Huvo AI Real Estate Sales Agent",
        "project": "Northstar One (Sector 79, Gurugram)",
        "model": agent_instance.model_name,
        "api_key_configured": bool(agent_instance.api_key)
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Handles multi-turn conversational chat with Gemini and auto-executes tools."""
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty."
        )
    
    result = agent_instance.chat(
        session_id=request.session_id,
        user_message=request.message
    )
    return result


@app.post("/api/analytics", response_model=LeadAnalytics)
async def analytics_endpoint(request: AnalyticsRequest):
    """Extracts structured CRM lead intelligence and insights from conversation transcript."""
    analytics = agent_instance.generate_analytics(session_id=request.session_id)
    return analytics


@app.post("/api/session/reset")
async def reset_session_endpoint(request: ResetSessionRequest):
    """Resets memory state for a given conversation session."""
    agent_instance.reset_session(session_id=request.session_id)
    return {"status": "success", "message": f"Session {request.session_id} memory cleared."}


@app.get("/api/session/{session_id}/history")
async def get_history_endpoint(session_id: str):
    """Retrieves full conversation history for a given session."""
    history = agent_instance.get_session_history(session_id=session_id)
    return {"session_id": session_id, "history": history}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run("main:app", host=host, port=port, reload=True)
