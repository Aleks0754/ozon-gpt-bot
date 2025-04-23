
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from services.review_storage import get_all_reviews, update_review_status
from services.telegram_notify import send_telegram_message

router = APIRouter()

@router.get("/moderation")
def moderation_page():
    with open("moderation.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@router.get("/moderation/data")
def get_data():
    reviews = get_all_reviews()
    formatted = [{"index": i, **r} for i, r in reviews]
    return JSONResponse(content=formatted)

@router.post("/moderation/approve")
def approve(index: int = Form(...)):
    update_review_status(index, "approved")
    return RedirectResponse(url="/moderation", status_code=302)

@router.post("/moderation/reject")
def reject(index: int = Form(...)):
    update_review_status(index, "rejected")
    return RedirectResponse(url="/moderation", status_code=302)
