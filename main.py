from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from router.review import review_router
from router.moderation import moderation_router
from services.telegram_polling import start_polling

app = FastAPI()
start_polling()

app.include_router(review_router)
app.include_router(moderation_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_home():
    return FileResponse("static/index.html")

@app.get("/moderation", response_class=HTMLResponse)
def serve_moderation():
    return FileResponse("static/moderation.html")
