
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import json
import os

router = APIRouter()

LOG_PATH = "review_log.json"

def load_log():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_log(data):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@router.get("/moderation")
def moderation_page():
    with open("moderation.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@router.get("/moderation/data")
def get_data():
    return load_log()

@router.post("/moderation/approve")
def approve(index: int = Form(...)):
    log = load_log()
    item = log[index]
    from services.telegram_notify import send_telegram_message
    send_telegram_message(f"✅ Одобрено:\n{item['text']}\n\nОтвет:\n{item['reply']}")
    return RedirectResponse(url="/moderation", status_code=302)
