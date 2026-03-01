# AI Ticketing Tool - Vision Agents Hackathon 🚀

A modular, real-time AI-powered ticketing system that uses Google's Gemini Multimodal Live API to provide voice-based support.

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
