import os
import time
import requests
from threading import Thread
from services.review_storage import update_review_status

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
OFFSET = None


def process_callback(callback):
    global OFFSET
    callback_id = callback["id"]
    data = callback["data"]  # approve:1 или reject:2
    message = callback["message"]
    chat_id = message["chat"]["id"]
    message_id = message["message_id"]

    if ":" not in data:
        return

    action, index = data.split(":")
    index = int(index)

    if action == "approve":
        update_review_status(index, "approved")
        answer = "✅ Отзыв одобрен."
    elif action == "reject":
        update_review_status(index, "rejected")
        answer = "❌ Отзыв отклонён."
    else:
        return

    # Уведомление пользователю
    requests.post(BASE_URL + "/sendMessage", json={
        "chat_id": chat_id,
        "text": answer
    })

    # Удалим inline-кнопки
    requests.post(BASE_URL + "/editMessageReplyMarkup", json={
        "chat_id": chat_id,
        "message_id": message_id,
        "reply_markup": {"inline_keyboard": []}
    })

    # Подтвердим callback Telegram
    requests.post(BASE_URL + "/answerCallbackQuery", json={"callback_query_id": callback_id})


def polling_loop():
    global OFFSET
    print("▶️ Telegram polling запущен")
    while True:
        try:
            resp = requests.get(BASE_URL + "/getUpdates", params={"offset": OFFSET, "timeout": 10})
            data = resp.json()
            for update in data.get("result", []):
                OFFSET = update["update_id"] + 1
                if "callback_query" in update:
                    process_callback(update["callback_query"])
        except Exception as e:
            print("❌ Ошибка в polling:", e)
        time.sleep(2)


def start_polling():
    thread = Thread(target=polling_loop)
    thread.daemon = True
    thread.start()
