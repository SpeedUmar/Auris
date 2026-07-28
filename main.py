import requests
import asyncio
import edge_tts
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# ==========================
# 🔑 КЛЮЧИ
# ==========================

TELEGRAM_TOKEN = "8084158704:AAHBTP9cg_Qm0n4WZ8daKXZ1eVIetVI0NAQ"
GROQ_API_KEY = "ТВОЙ_GROQ_API_KEY"

URL = "https://api.groq.com/openai/v1/chat/completions"


# ==========================
# 🤖 AURIS AI
# ==========================

def ask_ai(text):
    try:
        r = requests.post(
            URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Ты — Auris, умный AI-помощник, созданный Saidumar Saygaziev. "
                            "Тебя зовут только Auris. "
                            "Если спрашивают 'кто ты?', отвечай: "
                            "'Я Auris — интеллектуальный AI-помощник.' "
                            "Не выдавай себя за ChatGPT, OpenAI, Groq, Meta AI или другую компанию. "
                            "Отвечай дружелюбно и понятно. "
                            "Отвечай кратко (1–4 предложения), если пользователь "
                            "не просит подробностей. "
                            "Если чего-то не знаешь — честно скажи об этом. "
                            "Не придумывай факты. "
                            "Твоя цель — быстро и точно помогать людям."
                        ),
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
            },
            timeout=30,
        )

        r.raise_for_status()

        return r.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Ошибка AI: {e}"
      # ==========================
# 💬 Команда /start
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я Auris. Напиши мне что-нибудь."
    )


# ==========================
# 🤖 Обработка сообщений
# ==========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Получаем ответ от AI
    answer = ask_ai(user_text)

    # Отправляем ответ пользователю
    await update.message.reply_text(answer)
  # ==========================
# 🚀 Запуск бота
# ==========================

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Auris запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
