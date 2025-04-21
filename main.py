from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from router.review import review_router
import os

app = FastAPI()

app.include_router(review_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def serve_home():
    file_path = "static/index.html"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    raise HTTPException(status_code=404, detail="index.html not found")
