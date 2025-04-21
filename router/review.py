from fastapi import APIRouter
from pydantic import BaseModel
from services.gpt_reply import generate_reply
from services.telegram_notify import send_telegram_message

review_router = APIRouter()

class ReviewRequest(BaseModel):
    text: str

@review_router.post("/reply")
async def reply_to_review(request: ReviewRequest):
    reply = generate_reply(request.text)

    send_telegram_message(
        f"📩 Новый отзыв:\n{request.text}\n\n🤖 Сгенерированный ответ:\n{reply}"
    )

    return {"reply": reply}
