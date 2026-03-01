# 🚀 Building the Future of IT Support: The Gemini-Powered AI Ticketing Tool

## 🌟 The Vision
In the high-stakes world of IT support, every second counts. Traditional ticketing systems are reactive—users wait hours for a response, and technicians repeat the same troubleshooting steps. 

Our mission was to flip the script: **What if the ticketing system could talk back?**

Today, we built a modular, real-time AI Ticketing Tool that transforms a static support request into a live, voice-driven troubleshooting session.

---

## 🏗️ The Architecture: From Monolith to Modular
We started with a single, complex Python file and refactored it into a clean, professional architecture:
- **`agent.py`**: The "Voice of Reason." Defines specialized personas (Technical, Billing, General) and powers the Multi-modal Live interaction.
- **`ai_ticketing_tool.py`**: The high-performance FastAPI backend.
- **`models.py`**: Structured Pydantic models with a pre-seeded database of 20 real-world support scenarios.
- **`interface/`**: A premium, responsive dashboard for managing tickets and launching AI calls.

---

## 🛠️ The Technical Challenge: Overcoming the "1008 Policy Violation"
One of the most intense moments of the hackathon was meeting the **Gemini 1008 Policy Violation**. 
- **The Symptom**: The AI agent would join the call but immediately get rejected by the Gemini API.
- **The Solution**: Through deep-dives into the `google-genai` library, we discovered that explicitly synchronizing the `system_instruction` and standardizing on the `gemini-2.0-flash-exp` model was the key to unlocking the real-time voice bridge.

---

## 🎤 The Experience: How it Works
1. **Ticket Creation**: A user reports a problem (e.g., "Wi-Fi is connected but internet is not working").
2. **AI Matching**: The system automatically assigns a **Technical Specialist** persona.
3. **Live Voice Session**: The user clicks "Start Call." The AI agent joins via **Stream's ultra-low-latency edge network**, listens to the user's symptoms, and provides step-by-step guidance.
4. **Resolution**: Once satisfied, the AI triggers a **Ticket Closure Tool**, popping up a confirmation on the user's screen.

---

## 🔮 Future Scope: The Road to 1.0
This is just the beginning. Our roadmap for the "Total Support" platform includes:
- **Knowledge Base RAG**: Integrating internal docs so the AI can provide company-specific solutions (e.g., "Which VPN server should I use for region X?").
- **Live Screen Sharing**: Allowing the AI to "see" the user's screen in real-time to debug UI issues or configuration errors.
- **Auto-Transcription & Summarization**: Automatically generating a post-call summary and adding it to the ticket notes.
- **Multi-Agent Collaboration**: If a "General" agent detects a billing issue, it seamlessly hand-offs the call to a "Billing" agent without disconnecting the user.

---

## 🏆 Conclusion
By combining **Google Gemini's** reasoning with **Stream's** real-time video/audio infrastructure, we've created a tool that doesn't just manage tickets—it solves problems.

**Built for the Vision Agents Hackathon 2025.**
