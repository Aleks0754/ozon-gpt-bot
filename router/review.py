from fastapi import APIRouter
from pydantic import BaseModel
from services.gpt_reply import generate_reply
from services.review_storage import save_review

review_router = APIRouter()

class ReviewRequest(BaseModel):
    text: str

@ review_router.post ("/reply")
async def reply_to_review(request: ReviewRequest):
    reply = generate_reply(request.text)
    save_review(request.text, reply)
    
    return {"reply": reply}	
