import os
import json
from typing import Literal
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()

# === Telegram уведомления ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

def send_telegram_message_with_buttons(text: str, reply: str, index: int):
    if not TELEGRAM_TOKEN or not TELEGRAM_USER_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": f"✉️ Новый отзыв:\n{text}\n\n🗣 Ответ:\n{reply}",
        "reply_markup": json.dumps({
            "inline_keyboard": [[
                {"text": "✅ Одобрить", "callback_data": f"approve:{index}"},
                {"text": "❌ Отклонить", "callback_data": f"reject:{index}"}
            ]]
        })
    }
    requests.post(url, data=payload)

# === Работа с отзывами ===
REVIEWS_PATH = "data/reviews.json"
os.makedirs("data", exist_ok=True)

def load_reviews():
    if not os.path.exists(REVIEWS_PATH):
        return []
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

# === Маршруты ===
@app.get("/api/reviews")
def api_reviews(status: str = "all"):
    return JSONResponse(get_all_reviews(status))

@app.post("/api/reviews/{index}/approve")
def approve(index: int):
    update_review_status(index, "approved")
    return {"status": "ok"}

@app.post("/api/reviews/{index}/reject")
def reject(index: int):
    update_review_status(index, "rejected")
    return {"status": "ok"}

@app.get("/moderation")
def moderation_page():
    with open("moderation.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# Подключение static, если понадобится
app.mount("/static", StaticFiles(directory="static"), name="static")
