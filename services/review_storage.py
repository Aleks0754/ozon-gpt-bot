
import json
from typing import Literal
from services.telegram_notify import send_telegram_message

REVIEW_FILE = "data/reviews.json"

def _load_reviews():
    try:
        with open(REVIEW_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def _save_reviews(reviews):
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

def save_review(text: str, reply: str):
    reviews = _load_reviews()
    review = {"text": text, "reply": reply, "status": "pending"}
    reviews.append(review)
    _save_reviews(reviews)
    send_telegram_message(
        f"📮 Новый отзыв:
{text}

🤖 Сгенерированный ответ:
{reply}"
    )

def get_all_reviews(status: Literal["all", "pending", "approved", "rejected"] = "all"):
    reviews = _load_reviews()
    if status == "all":
        return reviews
    return [r for r in reviews if r["status"] == status]

def update_review_status(index: int, status: Literal["approved", "rejected"]):
    reviews = _load_reviews()
    if 0 <= index < len(reviews):
        reviews[index]["status"] = status
        _save_reviews(reviews)
