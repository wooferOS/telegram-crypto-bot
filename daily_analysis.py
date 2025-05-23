import os
import datetime
from binance.client import Client
from dotenv import load_dotenv

# Завантажуємо змінні з .env
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
BUDGET_USD = float(os.getenv("TRADING_BUDGET", "100"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

client = Client(API_KEY, API_SECRET)

SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT', 'XRPUSDT', 'ADAUSDT', 'AAVEUSDT', 'MASKUSDT']

def get_price_change(symbol):
    klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=2)
    if len(klines) < 2:
        return 0
    open_price = float(klines[0][1])
    close_price = float(klines[1][4])
    change_percent = ((close_price - open_price) / open_price) * 100
    return round(change_percent, 2), close_price

def analyze_market():
    buy = []
    sell = []
    stop_loss_data = []

    for symbol in SYMBOLS:
        change, current_price = get_price_change(symbol)
        coin = symbol.replace("USDT", "")

        if change <= -5:
            buy.append(coin)
            sl = round(current_price * 0.9, 2)
            stop_loss_data.append(f"🔻 Stop Loss {coin}: {sl} USDT")
        elif change >= 8:
            sell.append(coin)

    report = f"""📊 Сигнал на {datetime.date.today()}:

✅ Купити: {', '.join(buy) if buy else '—'}
❌ Продавати: {', '.join(sell) if sell else '—'}

📉 Stop Loss:
{chr(10).join(stop_loss_data) if stop_loss_data else '—'}
💰 Бюджет: ${BUDGET_USD}
"""
    return report

if __name__ == "__main__":
    print(analyze_market())
