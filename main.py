import os
from dotenv import load_dotenv
import telebot

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if not TELEGRAM_TOKEN:
    print("❌ TELEGRAM_API_TOKEN не знайдено в .env")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    bot.reply_to(message, "Привіт! Я криптобот і працюю 🟢")

if __name__ == "__main__":
    print("✅ Bot polling запущено")
    bot.polling(none_stop=True)
