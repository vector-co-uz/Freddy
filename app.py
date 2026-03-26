import time
import asyncio
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

import ai
import config # Импортируем конфиг

user_buffers = {}
last_owner_activity = 0

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_owner_activity
    if not update.business_message: return

    user_id = update.business_message.from_user.id
    current_time = time.time()

    # Проверка владельца (из конфига)
    if str(update.effective_user.id) == config.BUSINESS_CHAT_ID:
        last_owner_activity = current_time
        return

    # Проверка спячки (из конфига)
    if current_time - last_owner_activity < config.OWNER_OFFLINE_THRESHOLD:
        return

    # Накопление
    if user_id not in user_buffers: user_buffers[user_id] = []
    user_buffers[user_id].append(update.business_message.text)

    await asyncio.sleep(config.DEBOUNCE_TIME)

    if user_id in user_buffers and user_buffers[user_id]:
        full_msg = "\n".join(user_buffers.pop(user_id))
        response = ai.send_message_to_user(user_id, full_msg)
        await update.business_message.reply_text(response)

def main():
    app = Application.builder().token(config.BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.UpdateType.BUSINESS_MESSAGE, text_message_handler))
    print("Vector Assistant запущен через config.py")
    app.run_polling()

if __name__ == "__main__":
    main()