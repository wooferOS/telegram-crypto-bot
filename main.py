# === ПОВНИЙ main.py ===
import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
import telebot
from openai import OpenAI

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERVER_DOMAIN = os.getenv("SERVER_DOMAIN")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_API_TOKEN не встановлено!")

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
gpt = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    try:
        update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
        bot.process_new_updates([update])
        logging.info("✅ Отримано update")
    except Exception as e:
        logging.error(f"❌ Webhook error: {e}")
        return "Webhook error", 500
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    return "✅ OK", 200

@bot.message_handler(commands=["ask"])
def ask_handler(message):
    prompt = message.text.replace("/ask", "").strip()
    if not prompt:
        bot.send_message(message.chat.id, "❗ Напиши щось після /ask")
        return
    try:
        response = gpt.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)
        logging.info(f"🤖 Відповідь: {reply}")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Помилка: {e}")
        logging.error(f"GPT error: {e}")

