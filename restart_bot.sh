#!/bin/bash

echo "🔍 Закриваю процеси на портах 10000 і 5000..."
fuser -k 10000/tcp 2>/dev/null
fuser -k 5000/tcp 2>/dev/null

echo "🔍 Вбиваю Python процеси Flask, якщо зависли..."
pkill -f "main.py" 2>/dev/null
pkill -f flask 2>/dev/null

echo "🌐 Перезапускаю ngrok..."
pkill -f ngrok 2>/dev/null
nohup ./ngrok http 10000 > /dev/null 2>&1 &

echo "🚀 Запускаю Flask..."
python3 main.py

