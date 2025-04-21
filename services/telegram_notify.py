import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ Telegram config missing!")
        print("TELEGRAM_BOT_TOKEN exists:", bool(TELEGRAM_TOKEN))
        print("TELEGRAM_CHAT_ID exists:", bool(CHAT_ID))
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("❌ Telegram API error:", response.status_code, response.text)
        else:
            print("✅ Уведомление отправлено в Telegram")
    except Exception as e:
        print(f"❌ Ошибка при отправке сообщения в Telegram: {e}")
