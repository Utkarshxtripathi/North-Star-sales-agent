import os
import uvicorn
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from backend.agent import agent_instance, LeadAnalytics
except ImportError:
    from agent import agent_instance, LeadAnalytics

# Initialize FastAPI application
app = FastAPI(
    title="Northstar Sales Agent - Northstar One API",
    description="Conversational Real Estate AI Agent with Dual Voice/Chat Prompting, Function Calling, and Structured CRM Analytics.",
    version="1.0.0"
)

# Enable CORS for web client integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure directories for static assets and HTML templates from project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
static_dir = os.path.join(project_root, "static")
templates_dir = os.path.join(project_root, "templates")

os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Schema for incoming user chat request
class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the user session")
    message: str = Field(..., description="Customer message text in English, Hindi, or Hinglish")

# Schema for agent chat response with tool metadata
class ChatResponse(BaseModel):
    session_id: str
    response: str
    tool_called: Optional[str] = None
    tool_details: Optional[Dict[str, Any]] = None
    history: List[Dict[str, Any]]

# Schema for structured analytics extraction request
class AnalyticsRequest(BaseModel):
    session_id: str = Field(..., description="Session ID whose transcript is to be analyzed")

# Schema for clearing session memory request
class ResetSessionRequest(BaseModel):
    session_id: str = Field(..., description="Session ID to reset")

# Serve the web application frontend
@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Health check and configuration status endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Northstar Real Estate Sales Agent",
        "project": "Northstar One (Sector 79, Gurugram)",
        "model": agent_instance.model_name,
        "api_key_configured": bool(agent_instance.api_key)
    }

# Process multi-turn chat message and return assistant response
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
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

# Extract structured CRM lead intelligence from conversation history
@app.post("/api/analytics", response_model=LeadAnalytics)
async def analytics_endpoint(request: AnalyticsRequest):
    analytics = agent_instance.generate_analytics(session_id=request.session_id)
    return analytics

# Reset memory and state for a conversation session
@app.post("/api/session/reset")
async def reset_session_endpoint(request: ResetSessionRequest):
    agent_instance.reset_session(session_id=request.session_id)
    return {"status": "success", "message": f"Session {request.session_id} memory cleared."}

# Retrieve full message history for a given session
@app.get("/api/session/{session_id}/history")
async def get_history_endpoint(session_id: str):
    history = agent_instance.get_session_history(session_id=session_id)
    return {"session_id": session_id, "history": history}

# Server execution entry point
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run("backend.main:app", host=host, port=port, reload=True)
