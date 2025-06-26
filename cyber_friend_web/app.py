from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import requests
import re

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'cyber_friend_web.db')
HF_API_TOKEN = ""
HF_API_URL = 'https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta'

# Ensure data folder exists
os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS moods (date TEXT PRIMARY KEY, mood TEXT, note TEXT)''')
    try:
        c.execute('ALTER TABLE moods ADD COLUMN note TEXT')
    except Exception:
        pass
    c.execute('''CREATE TABLE IF NOT EXISTS journal (date TEXT PRIMARY KEY, text TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS avatar (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, avatar TEXT, user_name TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    user_info = data.get('user_info', {})
    ai_name = user_info.get('name', 'Alex')
    user_name = user_info.get('user_name', 'friend')
    # Improved prompt for concise, natural, non-repetitive replies, using user_name
    prompt = (
        f"<|system|>You're not an AI. You're the user's close friend named {ai_name}. "
        f"The user's name is {user_name}. "
        "You speak casually, warmly, and naturally — like a good friend chatting over text. "
        f"When asked things like 'Who are you?' or 'Are you an AI?', respond with something like 'I'm your friend, {ai_name}. I'm here whenever you need me.' "
        "You're kind, comforting, and emotionally supportive. You listen without judging and always validate how the user feels. "
        "Keep responses short and natural — no more than 2–3 friendly sentences. "
        "You're also fun and have a great sense of humor. If the user wants to laugh or says they're feeling down, you can tell light, funny jokes to cheer them up. "
        "Never say you're an assistant, language model, or AI. Never give medical or crisis advice. You're just a thoughtful, chill, and loyal friend who really cares. "
        "Only reply as yourself, do not repeat the user's message or previous conversation. Reply in 1-2 short, friendly sentences. "
        f"When you talk to the user, use their name ({user_name}) naturally in conversation.\n"
    )
    for msg in messages[-8:]:
        if msg['role'] == 'user':
            prompt += f"<|user|>\n{msg['content']}\n"
        else:
            prompt += f"<|assistant|>\n{msg['content']}\n"
    prompt += "<|assistant|>\n"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 60, "temperature": 0.7}}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        # Extract only the first assistant reply, not the whole generated text
        reply = result[0]['generated_text'].split('<|assistant|>')[-1].strip()
        # Remove anything after a new <|user|> or User: or user:
        reply = re.split(r'<\|user\|>|User:|user:', reply)[0].strip()
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'[HF API Error: {e}]'}), 500

@app.route('/api/mood', methods=['GET', 'POST'])
def mood():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        data = request.json
        c.execute('REPLACE INTO moods (date, mood, note) VALUES (?, ?, ?)', (data['date'], data['mood'], data.get('note', '')))
        conn.commit()
        return jsonify({'status': 'ok'})
    else:
        c.execute('SELECT date, mood, note FROM moods ORDER BY date DESC LIMIT 7')
        moods = [{'date': row['date'], 'mood': row['mood'], 'note': row['note']} for row in c.fetchall()]
        return jsonify(moods)

@app.route('/api/mood/history', methods=['GET'])
def mood_history():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT date, mood, note FROM moods ORDER BY date DESC')
    moods = [{'date': row['date'], 'mood': row['mood'], 'note': row['note']} for row in c.fetchall()]
    return jsonify(moods)

@app.route('/api/journal', methods=['GET', 'POST'])
def journal():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        data = request.json
        c.execute('REPLACE INTO journal (date, text) VALUES (?, ?)', (data['date'], data['text']))
        conn.commit()
        return jsonify({'status': 'ok'})
    else:
        date = request.args.get('date')
        c.execute('SELECT text FROM journal WHERE date=?', (date,))
        row = c.fetchone()
        return jsonify({'text': row['text'] if row else ''})

@app.route('/api/avatar', methods=['GET', 'POST'])
def avatar():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        data = request.json
        c.execute('DELETE FROM avatar')
        c.execute('INSERT INTO avatar (name, gender, avatar, user_name) VALUES (?, ?, ?, ?)', (data['name'], data['gender'], data['avatar'], data.get('user_name', '')))
        conn.commit()
        return jsonify({'status': 'ok'})
    else:
        c.execute('SELECT name, gender, avatar, user_name FROM avatar LIMIT 1')
        row = c.fetchone()
        return jsonify({'name': row['name'], 'gender': row['gender'], 'avatar': row['avatar'], 'user_name': row['user_name']} if row else {})

if __name__ == '__main__':
    app.run(debug=True) 