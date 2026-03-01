import os
import logging
import asyncio
import uuid
from datetime import datetime
from typing import List, Dict
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from getstream import Stream as StreamVideo
import uvicorn

# Import modular components
from models import Ticket, AgentSessionRequest, TICKETS, SESSION_AUDIO
from agent import launch_ai_agent

# Constants and Credentials
GOOGLE_API_KEY = "GEMINI_API_KEY"
STREAM_API_KEY = "KEY"
STREAM_API_SECRET = "SECRET"

# Set environment variables for vision-agents plugins
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["STREAM_API_KEY"] = STREAM_API_KEY
os.environ["STREAM_API_SECRET"] = STREAM_API_SECRET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Ticketing Tool - Hackathon Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = os.path.join(os.path.dirname(__file__), "interface", "index.html")
    with open(index_path, "r") as f:
        return f.read()

@app.get("/api/tickets", response_model=List[Ticket])
async def get_tickets():
    print(f"DEBUG: 🛰️ API Req - Returning {len(TICKETS)} tickets to UI")
    return list(TICKETS.values())

@app.post("/api/tickets", response_model=Ticket)
async def create_ticket(ticket_data: Dict[str, str]):
    tid = f"TIC-{uuid.uuid4().hex[:6].upper()}"
    ticket = Ticket(
        id=tid,
        subject=ticket_data["subject"],
        description=ticket_data["description"],
        category=ticket_data.get("type", "General"),
        created_at=datetime.now().isoformat(),
        status="open"
    )
    TICKETS[tid] = ticket
    print(f"DEBUG: 🎫 Ticket Created: {tid} | Category: {ticket.category}")
    return ticket

@app.delete("/api/tickets")
async def clear_tickets():
    TICKETS.clear()
    print("DEBUG: 🧹 System Wiped - All tickets cleared.")
    return {"status": "cleared"}

@app.post("/api/tickets/{ticket_id}/resolve")
async def resolve_ticket_api(ticket_id: str, data: dict):
    if ticket_id in TICKETS:
        TICKETS[ticket_id].status = "closed"
        TICKETS[ticket_id].agent_comment = data.get("solution", "Resolved by user confirmation.")
        TICKETS[ticket_id].comments.append({
            "author": "System",
            "text": "Ticket officially closed via user confirmation.",
            "timestamp": datetime.now().isoformat()
        })
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.post("/api/tickets/{ticket_id}/chat")
async def add_chat_message_api(ticket_id: str, message: Dict[str, str]):
    if ticket_id in TICKETS:
        TICKETS[ticket_id].chat_history.append({
            "sender": message.get("sender", "Unknown"),
            "text": message.get("text", ""),
            "timestamp": datetime.now().isoformat()
        })
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.get("/tokens/{user_id}")
async def get_token_api(user_id: str):
    client = StreamVideo(STREAM_API_KEY, STREAM_API_SECRET)
    token = client.create_token(user_id)
    return {"token": token, "api_key": STREAM_API_KEY}

@app.get("/avatar-video")
async def get_avatar_video():
    video_path = os.path.join(os.path.dirname(__file__), "ai avator Video.mp4")
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    raise HTTPException(status_code=404, detail="Video not found")

@app.get("/audio/{call_id}/{chunk_idx}.wav")
async def get_audio_chunk(call_id: str, chunk_idx: int):
    if call_id in SESSION_AUDIO and chunk_idx < len(SESSION_AUDIO[call_id]):
        return Response(content=SESSION_AUDIO[call_id][chunk_idx], media_type="audio/wav")
    raise HTTPException(status_code=404)

@app.post("/start-agent-session")
async def start_agent_session_api(request: AgentSessionRequest):
    if request.ticket_id not in TICKETS:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Run agent in background task
    asyncio.create_task(launch_ai_agent(request.ticket_id, request.call_id, request.call_type))
    return {"status": "Agent scheduled to join"}

if __name__ == "__main__":
    print("Cleaning up port 8000...")
    os.system("lsof -i :8000 -t | xargs kill -9 > /dev/null 2>&1")
    print("🚀 Starting Modular AI Ticketing Tool (v14.0)...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
