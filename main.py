from fastapi import FastAPI
from router import review_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ozon-gpt-bot is alive!"}

app.include_router(review_router, prefix="/review")