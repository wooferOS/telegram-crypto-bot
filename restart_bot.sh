#!/bin/bash

echo "🔍 Закриваю порти..."
fuser -k 10000/tcp 2>/dev/null
fuser -k 5000/tcp 2>/dev/null

echo "🔍 Вбиваю Flask та ngrok..."
pkill -f "main.py" 2>/dev/null
pkill -f flask 2>/dev/null
pkill -f ngrok 2>/dev/null

echo "🌐 Запускаю ngrok..."
nohup ./ngrok http 10000 --log=stdout > /tmp/ngrok.log 2>&1 &

sleep 3

echo "🚀 Запускаю Flask..."
nohup python3 main.py > /tmp/bot.log 2>&1 &

