# 🌐 AI Companion: Cyber Friend

> A modern AI-powered companion for mental wellness, empathetic conversation, mood tracking, journaling, and avatar customization.  
> Available as both a **desktop** and **web application**.

---

📸 **Screenshots / Interface Preview**
*(Add screenshots or screen recordings of your web/desktop UI below this line)*

---

## 🌟 Core Features

- **🧍 Customizable Avatar**  
  Choose your AI friend’s gender, name, and portrait.

- **🧠 AI Chat Interface**  
  Friendly, empathetic chat powered by **OpenAI** or a local LLM via **Hugging Face**.

- **📊 Mood Tracker**  
  Emoji-based daily mood selection with a modern stats and recent entries dashboard.

- **🔐 Encrypted Journal**  
  Secure and private journaling with daily notes and reflections.

- **🎙️ Voice Interaction (Desktop)**  
  Text-to-speech and speech-to-text support for fluid conversations.

- **🪐 Offline-first**  
  Works offline by default with optional online AI for enhanced responses.

---

## 🖥️ Web Application (Built with Flask)

### 🧭 UI/UX Highlights

- Responsive **sidebar navigation**
- **Avatar setup** with emoji/video backgrounds
- **Mood dashboard** with horizontal emoji selector and card-style stats
- **Journal tab** for encrypted reflections
- Scrollable **recent entries**
- Fully **mobile responsive** interface

---

## 🚀 Setup Instructions

### 1. 📦 Install Dependencies

Clone the repository and install required packages:

```bash
git clone https://github.com/your-username/cyber-friend.git
cd cyber-friend
pip install -r requirements.txt
For desktop version, ensure PyQt5, SpeechRecognition, and pyttsx3 are installed.

2. 🖥️ Run the Desktop App
bash
Copier
Modifier
python desktop_app.py
3. 🌐 Run the Web App
bash
Copier
Modifier
cd web_app
python app.py
Visit: http://127.0.0.1:5000/

📂 Folder Structure
pgsql
Copier
Modifier
cyber-friend/
│
├── desktop_app/            # PyQt-based desktop application
├── web_app/                # Flask web application
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JS, images
│   └── app.py              # Main Flask backend
│
├── data/                   # Local encrypted journal and mood storage
├── assets/                 # Emoji assets, UI images
├── README.md
└── requirements.txt
🧠 Web API Endpoints
Endpoint	Method	Description
/	GET	Load main web UI
/api/chat	POST	Chat with AI ({messages, user_info})
/api/mood	GET/POST	Get or save today's mood
/api/mood/history	GET	Retrieve all past moods
/api/journal	GET/POST	Get or save journal entry
/api/avatar	GET/POST	Manage avatar details

🔒 Security & Environment
No API keys are stored in the codebase.

For OpenAI/Hugging Face integration, create a .env file:

ini
Copier
Modifier
OPENAI_API_KEY=your_openai_key
HF_API_TOKEN=your_huggingface_token
Ensure .env is added to your .gitignore.

🤝 Contributing
Fork this repository.

Create a new branch: git checkout -b my-feature.

Make your changes and commit them.

Push to your fork: git push origin my-feature.

Create a pull request and describe your changes.

📜 License
Licensed under the MIT License.

🙏 Credits
UI inspired by wellness/productivity apps.

Emoji assets by Twemoji.

AI models by OpenAI & Hugging Face.
