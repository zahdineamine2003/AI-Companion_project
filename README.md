
# 🤖 AI Companion: Cyber Friend

A modern **AI-powered mental wellness companion** for mood tracking, journaling, and chatting with a customizable avatar.  
Available as both a **desktop** and **web application**.

---

## 📸 Interface Preview

**🔵 Welcome Screen**  
![Welcome Screen](https://github.com/zahdineamine2003/AI-Companion_project/blob/39ec8917782ca54f6338b7cb41cd4546efe05613/cyber_friend/welcome.png?raw=true)

---
**🟣 Screen Recording (Live Preview)**  
![Screen Recording](https://raw.githubusercontent.com/zahdineamine2003/AI-Companion_project/6a3af6fd47e225c3e45d18ff640d2344de0306d4/cyber_friend/video.gif)

---

## 🌟 Features

- 🧍 Customizable avatar (name, gender, image)
- 🧠 Chat interface powered by OpenAI or Hugging Face
- 📊 Mood tracker with emoji and statistics
- 🔐 Encrypted journaling for mental reflections
- 🎙️ Voice interaction (speech-to-text & text-to-speech)
- 🪐 Offline-first functionality
- 📱 Mobile-responsive design

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cyber-friend.git
cd cyber-friend
````

---

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv

# For macOS/Linux:
source venv/bin/activate

# For Windows:
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### For Desktop Version (Additional Packages):

```bash
pip install PyQt5 SpeechRecognition pyttsx3
```

---

## 🚀 Running the App

### 🖥️ Run the Desktop Version

```bash
python desktop_app.py
```

---

### 🌐 Run the Web Version

```bash
cd web_app
python app.py
```

Visit the app at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧭 App Navigation

| Tab     | Function                           |
| ------- | ---------------------------------- |
| Home    | Launch chat with your AI companion |
| Mood    | Select and view your current mood  |
| Journal | Write secure daily reflections     |
| Avatar  | Customize your AI friend           |

---

## 🎯 Web API Endpoints

| Endpoint            | Method   | Description                            |
| ------------------- | -------- | -------------------------------------- |
| `/`                 | GET      | Load main web UI                       |
| `/api/chat`         | POST     | Chat with AI (`{messages, user_info}`) |
| `/api/mood`         | GET/POST | Get or save today's mood               |
| `/api/mood/history` | GET      | Retrieve all past moods                |
| `/api/journal`      | GET/POST | Get or save journal entry              |
| `/api/avatar`       | GET/POST | Manage avatar details                  |

---

## 📁 Project Structure

```
cyber-friend/
│
├── desktop_app/            # PyQt-based desktop app
├── web_app/                # Flask web app
│   ├── templates/          # HTML pages
│   ├── static/             # CSS, JS, images
│   └── app.py              # Flask routes & logic
│
├── data/                   # Local encrypted mood/journal storage
├── assets/                 # Emoji icons, UI images
├── requirements.txt
└── README.md
```

---

## 🔐 Environment & Security

No API keys are stored in the codebase.

To integrate OpenAI or Hugging Face, create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
HF_API_TOKEN=your_huggingface_token
```

✅ Be sure to add `.env` to your `.gitignore`.

---

## 🤝 Contributing

We welcome contributions! Follow these steps:

1. **Fork** the repository
2. Create a new branch:

```bash
git checkout -b my-feature
```

3. Commit your changes
4. Push to your fork:

```bash
git push origin my-feature
```

5. Open a **pull request** and describe your updates

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙏 Credits

* UI inspired by modern productivity & wellness apps
* Emoji assets from [Twemoji](https://twemoji.twitter.com)
* AI powered by [OpenAI](https://openai.com) and [Hugging Face](https://huggingface.co)

---

✨ *Let your cyber companion help you reflect, connect, and grow.*


