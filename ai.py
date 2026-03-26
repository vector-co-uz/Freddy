import sqlite3
import json
import time
from google import genai
import prompts
import config # Импортируем наш новый конфиг

# Инициализация Gemini
client = genai.Client(api_key=config.GEMINI_API_KEY)

def init_db():
    conn = sqlite3.connect('chat_history.db')
    curr = conn.cursor()
    curr.execute('CREATE TABLE IF NOT EXISTS history (user_id TEXT PRIMARY KEY, messages TEXT)')
    conn.commit()
    conn.close()

init_db()

def get_history(user_id):
    try:
        conn = sqlite3.connect('chat_history.db')
        curr = conn.cursor()
        curr.execute("SELECT messages FROM history WHERE user_id = ?", (str(user_id),))
        row = curr.fetchone()
        conn.close()
        return json.loads(row[0]) if row else []
    except: return []

def save_history(user_id, history):
    conn = sqlite3.connect('chat_history.db')
    curr = conn.cursor()
    history = history[-config.HISTORY_LIMIT:] # Берем лимит из конфига
    curr.execute("INSERT OR REPLACE INTO history (user_id, messages) VALUES (?, ?)",
                 (str(user_id), json.dumps(history)))
    conn.commit()
    conn.close()

def send_message_to_user(user_id, message):
    msg_lower = message.lower().strip()
    
    # 1. Сначала FAQ
    for key, ans in prompts.FAQ_DATA.items():
        if key in msg_lower: return ans

    # 2. ИИ
    history = get_history(user_id)
    history.append({"role": "user", "parts": [{"text": message}]})

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=config.MODEL_NAME, # Берем имя модели из конфига
                contents=history,
                config={
                    "system_instruction": prompts.SYSTEM_INSTRUCTIONS["default"],
                    "temperature": 0.2,
                }
            )
            ai_text = response.text.strip()
            history.append({"role": "model", "parts": [{"text": ai_text}]})
            save_history(user_id, history)
            return ai_text
        except Exception as e:
            if "429" in str(e):
                time.sleep(20)
                continue
            return "Ошибка связи."
    return "Лимит исчерпан."