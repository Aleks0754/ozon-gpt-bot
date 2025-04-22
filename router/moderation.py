from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services.review_storage import get_all_reviews, update_review_status

moderation_router = APIRouter()

@router.get("/api/reviews")
def fetch_reviews():
    return JSONResponse(get_all_reviews())

@router.post("/api/reviews/{index}/approve")
def approve_review(index: int):
    update_review_status(index, "approved")
    return {"status": "ok"}

@router.post("/api/reviews/{index}/reject")
def reject_review(index: int):
    update_review_status(index, "rejected")
    return {"status": "ok"}
