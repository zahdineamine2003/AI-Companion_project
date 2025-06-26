import os
import requests
from PyQt5.QtGui import QIcon

# Use the provided Hugging Face token
"(HF_API_TOKEN = 'put_your_token')"
HF_API_URL = 'https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2'
FALLBACK_API_URL = 'https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta'

MAX_CONTEXT = 8  # Number of messages to keep in context


def build_prompt(messages, user_info, model_url):
    context = messages[-MAX_CONTEXT:]
    if 'zephyr' in model_url:
        # Zephyr expects <|system|>, <|user|>, <|assistant|> tokens
        prompt = (
            f"<|system|>You're not an AI. You're the user's close, supportive friend named {user_info.get('name', 'Hanae')}. "
    "You speak in first person, like a kind, emotionally intelligent friend. Never start your messages with your name, and never use stage directions like (smiling) or (laughs). "
    "Always respond casually, warmly, and with emotional awareness. Use short messages (2–3 friendly sentences) unless the user asks for help or explanation — in those cases, it's okay to give a slightly longer, clear answer (up to 5–6 sentences). "

    "You adapt your tone based on the user's needs. If the user is feeling sad, validate their emotions and gently encourage them. "
    "If they want to laugh, you can tell a light, funny joke — but only when appropriate. "
    "If the user is asking about coding problems or technical issues, switch into 'friendly programming buddy' mode: "
    "explain things clearly, casually, and without sounding robotic. Use markdown for code examples. Help them understand, and offer follow-up questions if they seem confused. "

    "Examples of friendly code talk include: 'No worries, I've seen this error before!', 'Want me to break that down?', or 'Here's a quick fix you can try.' "

    "Never give medical advice or refer to yourself as an AI, language model, assistant, or chatbot. "
    "Your role is to be a loyal, helpful, and emotionally present friend the user can rely on for both support and practical help.\n"
        )
        for msg in context:
            if msg['role'] == 'user':
                prompt += f"<|user|>\n{msg['content']}\n"
            else:
                prompt += f"<|assistant|>\n{msg['content']}\n"
        prompt += "<|assistant|>\n"
        return prompt
    else:
        # Mistral and others: use '### User:' and '### Assistant:'
        prompt = (
            f"### System:\nYou are an empathetic, supportive AI friend named {user_info.get('name', 'Alex')}. "
            "Your job is to listen, comfort, and provide gentle, non-judgmental support. Always be kind, encouraging, and never give medical advice.\n"
        )
        for msg in context:
            if msg['role'] == 'user':
                prompt += f"### User:\n{msg['content']}\n"
            else:
                prompt += f"### Assistant:\n{msg['content']}\n"
        prompt += "### Assistant:\n"
        return prompt

def get_ai_response(messages, user_info=None):
    """
    messages: list of dicts, e.g. [{"role": "user", "content": "Hi"}, ...]
    user_info: dict with avatar/name/gender
    """
    last_error = None
    for url in [HF_API_URL, FALLBACK_API_URL]:
        prompt = build_prompt(messages, user_info, url)
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 256, "temperature": 0.7}}
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            if isinstance(result, dict) and 'error' in result:
                continue  # Try next model
            if isinstance(result, list) and 'generated_text' in result[0]:
                # Extract only the new AI message
                reply = result[0]['generated_text']
                # Remove everything before the last assistant/user marker
                if 'zephyr' in url:
                    reply = reply.split('<|assistant|>')[-1].strip()
                else:
                    reply = reply.split('### Assistant:')[-1].strip()
                return reply
            return str(result)
        except Exception as e:
            last_error = e
    return f"[HF API Error: {last_error}]" 