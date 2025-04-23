import os
import json
from typing import Literal
from services.telegram_notify import send_telegram_message_with_buttons

REVIEWS_PATH = "data/reviews.json"
os.makedirs("data", exist_ok=True)

# Создаём файл, если его нет (при первом запуске)
if not os.path.exists(REVIEWS_PATH):
    with open(REVIEWS_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_reviews():
    with open(REVIEWS_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_reviews(reviews):
    with open(REVIEWS_PATH, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

def save_review(text: str, reply: str):
    reviews = load_reviews()
    new_review = {"text": text, "reply": reply, "status": "new"}
    reviews.append(new_review)
    save_reviews(reviews)

    # Отправка уведомления с кнопками
    send_telegram_message_with_buttons(text, reply, len(reviews) - 1)

def update_review_status(index: int, status: Literal["approved", "rejected"]):
    reviews = load_reviews()
    if 0 <= index < len(reviews):
        reviews[index]["status"] = status
        save_reviews(reviews)

def get_all_reviews(status_filter: str = "all"):
    reviews = load_reviews()
    if status_filter == "all":
        return list(enumerate(reviews))
    return [(i, r) for i, r in enumerate(reviews) if r.get("status") == status_filter]

