# config.py
import os

# API Ключи (можно прописать напрямую или брать из переменных окружения)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'ВАШ_ТОКЕН_ТЕЛЕГРАМ')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'ВАШ_КЛЮЧ_GEMINI')
BUSINESS_CHAT_ID = os.getenv('BUSINESS_CHAT_ID', 'ВАШ_ID')

# Настройки модели
MODEL_NAME = "models/gemini-1.5-flash-latest"

# Настройки бота
DEBOUNCE_TIME = 10           # Ожидание пачки сообщений (сек)
OWNER_OFFLINE_THRESHOLD = 300 # Время "спячки" после вашей активности (сек)
HISTORY_LIMIT = 6            # Сколько сообщений помнить