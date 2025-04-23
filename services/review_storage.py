import json
import os
from services.telegram_notify import send_telegram_message

REVIEW_FILE = "reviews.json"

def load_reviews():
    if not os.path.exists(REVIEW_FILE):
        return []
    with open(REVIEW_FILE, "r") as f:
        return json.load(f)

def save_reviews(reviews):
    with open(REVIEW_FILE, "w") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

def save_review(text, reply):
    reviews = load_reviews()
    review = {
        "text": text,
        "reply": reply,
        "status": "pending"
    }
    reviews.append(review)
    save_reviews(reviews)
    send_telegram_message(f"📩 Новый отзыв:\n{text}\n\n🤖 Ответ:\n{reply}")

def get_all_reviews(status=None):
    reviews = load_reviews()
    if status:
        return [r for r in reviews if r.get("status") == status]
    return reviews

def update_review_status(index, status):
    reviews = load_reviews()
    if 0 <= index < len(reviews):
        reviews[index]["status"] = status
        save_reviews(reviews)
