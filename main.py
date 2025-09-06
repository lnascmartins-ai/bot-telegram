import logging
import requests
from flask import Flask, request

TOKEN = "7533353385:AAEbr_KGJY1S6YA6y0gmsDpa8igEuFQdAbI"
API_FOOTBALL_KEY = "40cd52c15b6d3b42c73781e7b8809843"
CHAT_ID = "6906485579"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        msg = data["message"].get("text", "")
        if msg == "/start":
            send_message("👋 Bot está ativo! Pronto para analisar jogos.")
        else:
            send_message("⚽ Análise em breve...")
    return "ok"

@app.route("/")
def home():
    return "Bot está rodando!", 200
