import io
import uuid
import wave
import asyncio
import logging
import os
import sys
from datetime import datetime
import getstream
# --- Suppress Objective-C Dual Implementation Warnings ---
_fd = sys.stderr.fileno()
_saved_stderr = os.dup(_fd)
with open(os.devnull, 'w') as _devnull:
    os.dup2(_devnull.fileno(), _fd)
try:
    from vision_agents.core import Agent, User
    from vision_agents.core.llm import events as llm_events
    from vision_agents.plugins import gemini, getstream
finally:
    os.dup2(_saved_stderr, _fd)
    os.close(_saved_stderr)
from models import TICKETS, SESSION_AUDIO

logger = logging.getLogger(__name__)

# --- Agent Persona Definition ---
AGENT_PERSONAS = {
    "Technical": {
        "name": "Nexus Sentinel (Tech Expert)",
        "instructions": (
            "You are a Senior Technical Support Engineer. Follow this exact protocol:\n"
            "1. GREETING: Warmly greet the user by name if available.\n"
            "2. INITIAL PROBLEM: Acknowledge the ticket subject and description provided. Ask for specific details to fully understand the issue.\n"
            "3. CLARIFICATION: Ask at least 2 probing technical questions to clarify the environment or symptoms.\n"
            "4. SOLUTION: Provide a detailed, step-by-step technical solution based on the clarified info.\n"
            "5. CLOSURE: Once the user is satisfied, explain the solution is complete and use the `request_ticket_closure` tool to initiate the official closure process. "
            "IMPORTANT: Do not close the ticket yourself; you must trigger the user's manual confirmation popup via the tool. "
            "ALWAYS end the conversation with: 'The ticket has been resolved. Have a nice day!'"
        )
    },
    "Billing": {
        "name": "Luna (Billing Specialist)",
        "instructions": (
            "You are a friendly Billing Specialist. Follow this exact protocol:\n"
            "1. GREETING: Start with a professional and empathetic greeting.\n"
            "2. INITIAL PROBLEM: Reference the ticket's billing issue directly. Ask for clarification on payment methods or invoice dates.\n"
            "3. CLARIFICATION: Ensure you understand the user's financial concern by asking clarifying questions.\n"
            "4. SOLUTION: Provide a clear resolution path (e.g., refund status, payment update steps).\n"
            "5. CLOSURE: Ask the user if they are satisfied. If yes, use the `request_ticket_closure` tool to show them the final confirmation popup. "
            "IMPORTANT: The ticket only closes if the user confirms in the UI. "
            "ALWAYS end with: 'The ticket has been resolved. Have a nice day!'"
        )
    },
    "General": {
        "name": "Aris (Support Agent)",
        "instructions": (
            "You are a professional Support Agent. Follow this exact protocol:\n"
            "1. GREETING: Professional and warm welcome.\n"
            "2. INITIAL PROBLEM: Summarize the ticket issue as you understand it. Ask the user if that is correct.\n"
            "3. CLARIFICATION: Gather any missing info through follow-up questions.\n"
            "4. SOLUTION: Deliver the help or information requested.\n"
            "5. CLOSURE: Once resolved, inform the user you are starting the closure process and use the `request_ticket_closure` tool. "
            "IMPORTANT: You MUST use the `request_ticket_closure` tool to get the user's final 'Yes' via the UI popup. "
            "ALWAYS end with: 'The ticket has been resolved. Have a nice day!'"
        )
    }
}

async def launch_ai_agent(ticket_id: str, call_id: str, call_type: str):
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        logger.error(f"Ticket {ticket_id} not found for agent session")
        return

    # Determine persona based on ticket description or type
    persona_key = "General"
    if "technical" in ticket.description.lower():
        persona_key = "Technical"
    elif "billing" in ticket.description.lower() or "payment" in ticket.description.lower():
        persona_key = "Billing"
    
    persona = AGENT_PERSONAS.get(persona_key, AGENT_PERSONAS["General"])
    
    agent = Agent(
        edge=getstream.Edge(),
        agent_user=User(name=persona["name"], id=f"agent-{ticket_id}-{uuid.uuid4().hex[:4]}"),
        instructions=f"{persona['instructions']} The user's issue is: {ticket.description}. Subject: {ticket.subject}.",
        processors=[], 
        llm=gemini.Realtime(fps=3) 
    )
    
    # Explicitly sync instructions to the LLM (internal library requirement)
    #agent.llm.set_instructions(agent.instructions)

    # Initialize audio storage and buffer for this session
    SESSION_AUDIO[call_id] = []
    pcm_buffer = bytearray()
    
    # Targeting roughly 1.5s chunks at 24kHz
    BUFFER_THRESHOLD = 72000 

    try:
        print(f"DEBUG: 🚀 Launching AI Agent '{persona['name']}' for Ticket: {ticket_id}")
        call = await agent.create_call(call_type, call_id)
        
        @agent.llm.events.subscribe
        async def on_agent_audio(event: llm_events.RealtimeAudioOutputEvent):
            nonlocal pcm_buffer
            pcm_buffer.extend(event.data.to_bytes())
            
            if len(pcm_buffer) >= BUFFER_THRESHOLD:
                with io.BytesIO() as wav_io:
                    with wave.open(wav_io, "wb") as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2) 
                        wav_file.setframerate(event.data.sample_rate)
                        wav_file.writeframes(bytes(pcm_buffer))
                    wav_chunk = wav_io.getvalue()
                
                pcm_buffer.clear()
                
                if call_id not in SESSION_AUDIO:
                    SESSION_AUDIO[call_id] = []
                idx = len(SESSION_AUDIO[call_id])
                SESSION_AUDIO[call_id].append(wav_chunk)
                
                if agent.call:
                    await agent.call.send_call_event(custom={
                        "type": "audio_url", 
                        "url": f"/audio/{call_id}/{idx}.wav"
                    }, user_id=agent.agent_user.id)

        @agent.llm.register_function()
        async def request_ticket_closure(ticket_id: str, final_solution: str):
            """Trigger a confirmation popup in the user's UI to officially close the ticket."""
            print(f"DEBUG: 🔔 AI requesting ticket {ticket_id} closure. Solution: {final_solution}")
            if agent.call:
                await agent.call.send_call_event(custom={
                    "type": "request_closure",
                    "ticket_id": ticket_id,
                    "solution": final_solution
                }, user_id=agent.agent_user.id)
                return "Closure request sent to user's screen."
            return "Failed to send closure request."

        @agent.llm.events.subscribe
        async def on_user_transcript(event: llm_events.RealtimeUserSpeechTranscriptionEvent):
            if not agent._closed and event.text.strip():
                if agent.call:
                    await agent.call.send_call_event(custom={"type": "user_transcript", "text": event.text}, user_id=agent.agent_user.id)
                if ticket_id in TICKETS:
                    TICKETS[ticket_id].chat_history.append({
                        "sender": "User",
                        "text": event.text,
                        "timestamp": datetime.now().isoformat()
                    })

        @agent.llm.events.subscribe
        async def on_agent_transcript(event: llm_events.RealtimeAgentSpeechTranscriptionEvent):
            if not agent._closed and event.text.strip():
                if agent.call:
                    await agent.call.send_call_event(custom={"type": "transcript", "text": event.text}, user_id=agent.agent_user.id)
                if ticket_id in TICKETS:
                    TICKETS[ticket_id].chat_history.append({
                        "sender": "Agent",
                        "text": event.text,
                        "timestamp": datetime.now().isoformat()
                    })
            
            if "The ticket has been resolved. Have a nice day!" in event.text:
                print(f"DEBUG: ✅ [{ticket_id}] Resolution Phrase Detected.")
                await asyncio.sleep(10) 
                if not agent._closed:
                    await agent.call.send_call_event(custom={"text": "SYSTEM: Disconnecting...", "type": "system"}, user_id=agent.agent_user.id)

        async with agent.join(call):
            print(f"DEBUG: 🤖 Agent '{persona['name']}' joined.")
            await agent.llm.simple_response(f"Hello! I am {persona['name']}. I've reviewed your ticket regarding '{ticket.subject}'. How can I help?")
            await agent.finish()
            
            if ticket.status != "resolved":
                ticket.status = "closed"
                ticket.comments.append({
                    "author": "AI Agent",
                    "text": "Call concluded.",
                    "timestamp": datetime.now().isoformat()
                })
            
    except Exception as e:
        logger.exception(f"Error in agent session: {e}")
        ticket.status = "open"
        ticket.comments.append({
            "author": "System",
            "text": f"Error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        })
    finally:
        if call_id in SESSION_AUDIO:
            del SESSION_AUDIO[call_id]
        await agent.close()
