import os
import requests
import time
from telegram import Bot
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# Função para obter jogos de hoje nas ligas-alvo
def buscar_jogos_atuais():
    headers = {
        "x-apisports-key": API_FOOTBALL_KEY
    }
    
    ligas = [39, 135, 78, 79]  # Premier League, Serie A, Bundesliga, 2. Bundesliga
    mensagens = []

    for liga_id in ligas:
        url = f"https://v3.football.api-sports.io/fixtures?league={liga_id}&season=2024&date={time.strftime('%Y-%m-%d')}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            dados = response.json()
            for jogo in dados['response']:
                time1 = jogo['teams']['home']['name']
                time2 = jogo['teams']['away']['name']
                horario = jogo['fixture']['date'][11:16]
                estagio = jogo['fixture']['status']['long']
                mensagem = f"📢 *Jogo Hoje*\n{time1} vs {time2}\n⏰ Horário: {horario}h\n📍 Status: {estagio}"
                mensagens.append(mensagem)
        else:
            mensagens.append(f"Erro ao buscar dados da Liga {liga_id}: {response.status_code}")

    return mensagens

# Função principal para enviar os jogos
def enviar_alerta():
    jogos = buscar_jogos_atuais()
    for msg in jogos:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="Markdown")

if __name__ == "__main__":
    print("Bot iniciado. Enviando jogos do dia...")
    enviar_alerta()
