import asyncio
import os
import uuid
from vision_agents.core import Agent, User
from vision_agents.plugins import gemini, getstream, deepgram, elevenlabs

GOOGLE_API_KEY = "GEMINI_API_KEY"
STREAM_API_KEY = "KEY"
STREAM_API_SECRET = "SECRET"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["STREAM_API_KEY"] = STREAM_API_KEY
os.environ["STREAM_API_SECRET"] = STREAM_API_SECRET

async def test_join():
    llm = gemini.LLM("gemini-1.5-flash-latest") 
    agent = Agent(
        edge=getstream.Edge(),
        agent_user=User(name="Test Agent", id=f"agent-test"),
        instructions="Greet the user and then finish.",
        processors=[],
        llm=llm,
        tts=elevenlabs.TTS(),
        stt=deepgram.STT(eager_turn_detection=True)
    )
    
    call_id = "test-call-" + uuid.uuid4().hex[:6]
    print(f"Creating call {call_id}...")
    call = await agent.create_call("default", call_id)
    
    print("Joining call...")
    async with agent.join(call):
        print("Joined! Sending response...")
        await agent.simple_response("Hello, this is a test.")
        print("Response sent. Finishing...")
        # await agent.finish() # Don't wait forever
    print("Done.")

if __name__ == "__main__":
    asyncio.run(test_join())
