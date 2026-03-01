# Fresh AI Ticketing Tool - for Vision Possible: Agent Protocol by Stream 🚀

Inspired by real-world support inefficiencies. Built to automate repetitive ticket resolution through real-time AI voice agents.

<img width="2652" height="1250" alt="image" src="https://github.com/user-attachments/assets/4c600f52-fdb3-4f35-957f-8f25892053ff" />

FreshAI was built from a real-world experience. While working on support projects in service-based industries, I consistently observed that a significant amount of time is spent on repetitive troubleshooting calls. Support engineers often guide users through the same solutions again and again — even though those solutions have already been documented in previous tickets.

Over time, it became clear that the inefficiency was not about capability, but about repetition. Many issues are recurring. The knowledge already exists. Yet during live calls, that knowledge is not automatically leveraged in a structured, intelligent way.

This led to one fundamental question:

What if an AI agent could join support calls, understand the issue context, use structured reasoning, and resolve repetitive problems automatically?

FreshAI is the first step toward answering that question.


## 🌟 Click below to watch Demo Video
[![Watch the video](https://i.ytimg.com/vi/nQDvEw5tIpQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=nQDvEw5tIpQ)



## 🌟 Blog Post

https://onkarpawar.hashnode.dev/building-the-future-of-it-support-the-gemini-powered-ai-ticketing-tool 

## 🌟 Key Features
- **Real-Time Voice Support:** Integrated voice calls with AI agents via the Gemini Live API.
- **Persona-Based Interaction:** Targeted technical, billing, and general support personas.
- **In-Memory Ticet Management:** Simple and fast CRUD for support tickets.
- **Modular Data System:** Clean separation between models, server logic, and AI agent logic.
- **Interactive Web Interface:** Beautiful frontend for ticket tracking and starting AI sessions.


## 🏗️ Modular Architecture
The project has been refactored into distinct modules for better maintainability and professional deployment:

- **`ai_ticketing_tool.py`**: The FastAPI core that manages the REST API endpoints and orchestrates the web server.
- **`agent.py`**: The AI logic layer. Defines agent personas, instructions, and handles the real-time interaction logic (transcripts, audio processing, tool calling).
- **`models.py`**: Data models (Pydantic) and the in-memory ticket database. 
- **`interface/index.html`**: The modern, responsive UI.

<img width="2214" height="1246" alt="image" src="https://github.com/user-attachments/assets/cfbf3106-e1d8-4b38-84df-d8cae5e36798" />

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python 3.12+
- **AI Engine:** Google Gemini (google-genai)
- **Voice Bridge:** GetStream Video & RTC
- **Frontend:** Vanilla JS, Tailwind CSS, HTML5

## 🚀 Setup & Installation

### 1. Prerequisites
Ensure you have `uv` or `pip` installed.

### 2. Environment Variables
You'll need valid API keys for both Google Gemini and Stream.
Create a `.env` file or set the following environment variables:
```bash
GOOGLE_API_KEY=your_google_api_key
STREAM_API_KEY=your_stream_api_key
STREAM_API_SECRET=your_stream_api_secret
```

### 3. Installation
Using `uv`:
```bash
uv sync
```
Or via `pip`:
```bash
pip install -r requirements.txt
```

### 4. Running the Application
```bash
python ai_ticketing_tool.py
```
Visit `http://localhost:8000` in your browser.

<img width="2104" height="1152" alt="image" src="https://github.com/user-attachments/assets/2143ff36-9ac8-45cf-8533-d0573f001d5e" />


## 📂 Project Structure
```text
Vision-Agents-main/
├── ai_ticketing_tool.py  # Entry point (FastAPI server)
├── agent.py              # AI Agent implementation
├── models.py             # Data models & storage
├── interface/            # Frontend assets
│   └── index.html        # Main UI
└── README.md             # This guide
```

---
Built with ❤️ for the Gemini Vision Agents Hackathon.
