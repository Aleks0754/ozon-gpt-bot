import os
import json
import requests
import time
from main import update_review_status

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"
OFFSET = None

def handle_callback(callback):
    data = callback["data"]
    chat_id = callback["message"]["chat"]["id"]
    message_id = callback["message"]["message_id"]

    if ":" in data:
        action, index_str = data.split(":")
        index = int(index_str)

        if action in ["approve", "reject"]:
            update_review_status(index, action)
            new_text = f"✅ Вы {('одобрили' if action == 'approve' else 'отклонили')} отзыв №{index}"

            # Редактируем сообщение
            requests.post(f"{API_URL}/editMessageText", data={
                "chat_id": chat_id,
                "message_id": message_id,
                "text": new_text
            })

def polling_loop():
    global OFFSET
    print("🔄 Запуск Telegram polling...")
    while True:
        try:
            response = requests.get(f"{API_URL}/getUpdates", params={
                "timeout": 30,
                "offset": OFFSET
            })
            updates = response.json()["result"]

            for update in updates:
                OFFSET = update["update_id"] + 1
                if "callback_query" in update:
                    handle_callback(update["callback_query"])

            time.sleep(1)
        except Exception as e:
            print("⚠️ Ошибка polling:", e)
            time.sleep(5)

if __name__ == "__main__":
    polling_loop()
