
import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram config missing")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
