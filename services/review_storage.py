import json
from pathlib import Path

STORAGE_FILE = Path("reviews.json")

# Временное хранилище для связи message_id и индекса
INDEX_TO_MESSAGE = {}


def _load_data():
    if STORAGE_FILE.exists():
        return json.loads(STORAGE_FILE.read_text(encoding="utf-8"))
    return []

def _save_data(data):
    STORAGE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def save_review(text, reply):
    from services.telegram_notify import send_telegram_message_with_buttons
    data = _load_data()
    new_item = {"text": text, "reply": reply, "status": "pending"}
    data.append(new_item)
    _save_data(data)
    index = len(data) - 1
    message_id = send_telegram_message_with_buttons(text, reply, index)
    INDEX_TO_MESSAGE[index] = message_id

def get_all_reviews(status: str = None):
    data = _load_data()
    if status:
        return [r for r in data if r.get("status") == status]
    return data

def update_review_status(index, status):
    from services.telegram_notify import send_telegram_message
    data = _load_data()
    if 0 <= index < len(data):
        data[index]["status"] = status
        _save_data(data)

        if status == "approved":
            send_telegram_message(
                f"✅ Отзыв подтверждён:\n{data[index]['text']}\n\nОтвет:\n{data[index]['reply']}"
            )

s.telegram_notify import send_telegram_message
    data = _load_data()
    if 0 <= index < len(data):
        data[index]["status"] = status
        _save_data(data)

        if status == "approved":
            send_telegram_message(
                f"✅ Отзыв подтверждён:\n{data[index]['text']}\n\nОтвет:\n{data[index]['reply']}"
            )
