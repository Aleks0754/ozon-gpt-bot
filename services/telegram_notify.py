import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_USER_ID:
        print("❌ Telegram config missing!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_USER_ID, "text": message}

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("❌ Telegram API error:", response.status_code, response.text)
        else:
            print("✅ Сообщение отправлено")
    except Exception as e:
        print("❌ Ошибка отправки Telegram:", e)

def send_telegram_message_with_buttons(text: str, reply: str, index: int):
    if not TELEGRAM_TOKEN or not TELEGRAM_USER_ID:
        print("❌ Telegram config missing for inline buttons!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": f"📩 Новый отзыв:\n{text}\n\n🤖 Ответ:\n{reply}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "✅ Одобрить", "callback_data": f"approve:{index}"},
                    {"text": "❌ Отклонить", "callback_data": f"reject:{index}"}
                ]
            ]
        }
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Сообщение с кнопками отправлено")
            message_id = response.json().get("result", {}).get("message_id")
            return message_id
        else:
            print("❌ Telegram API error:", response.status_code, response.text)
    except Exception as e:
        print("❌ Ошибка отправки inline-кнопок:", e)
