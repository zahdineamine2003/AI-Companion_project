# AI Companion: Cyber Friend

A desktop application that provides a virtual AI-powered friend for mental wellness support, empathetic conversation, and daily emotional check-ins.

## Features
- Customizable avatar (male/female, name, portrait)
- AI chat interface (OpenAI or local LLM)
- Mood tracker with daily/weekly summaries
- Encrypted daily journal/notes
- Voice interaction (TTS/STT)
- Offline-first, optional online AI

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python main.py
   ```

## Folder Structure
- `ui/` - UI components
- `core/` - Core logic (AI, sentiment, DB, voice)
- `assets/` - Avatars, icons
- `data/` - Local encrypted user data 