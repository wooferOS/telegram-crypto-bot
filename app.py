from flask import Flask, request

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    return "Webhook received", 200
