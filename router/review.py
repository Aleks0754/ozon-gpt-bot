from fastapi import APIRouter
from pydantic import BaseModel
from services.gpt_reply import generate_reply
from services.telegram_notify import send_telegram_message
from services.review_storage import save_review

router = APIRouter()

class ReviewRequest(BaseModel):
    text: str

@router.post("/reply")
async def reply_to_review(request: ReviewRequest):
    reply = generate_reply(request.text)
    save_review(request.text, reply)
    send_telegram_message(
        f"📮 Новый отзыв:\n{request.text}\n\n🤖\nСгенерированный ответ:\n{reply}"
    )
    return {"reply": reply}
