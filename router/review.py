from fastapi import APIRouter
from pydantic import BaseModel
from services.gpt_reply import generate_reply

review_router = APIRouter()

class ReviewRequest(BaseModel):
    text: str

@review_router.post("/reply")
def reply_to_review(request: ReviewRequest):
    return {"reply": generate_reply(request.text)}