import os
import telebot
from dotenv import load_dotenv
import requests

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
SERVER_DOMAIN = os.getenv("SERVER_DOMAIN")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_API_TOKEN не встановлено!")
if not SERVER_DOMAIN:
    raise ValueError("❌ SERVER_DOMAIN не встановлено!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Дізнаємось актуальний ngrok HTTPS-URL
try:
    ngrok_url = requests.get("http://127.0.0.1:4040/api/tunnels").json()["tunnels"][0]["public_url"]
except Exception as e:
    raise RuntimeError(f"❌ Не вдалося отримати ngrok URL: {e}")

webhook_url = f"{ngrok_url}/webhook"
current = bot.get_webhook_info().url

if current == webhook_url:
    print(f"ℹ️ Webhook вже налаштовано: {webhook_url}")
else:
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print(f"✅ Webhook встановлено: {webhook_url}")

