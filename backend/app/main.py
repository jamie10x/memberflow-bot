# backend/app/main.py
from fastapi import FastAPI
from .api.api import api_router

app = FastAPI(
    title="MemberFlow API",
    description="The backend API for the MemberFlow Telegram subscription bot.",
    version="0.1.0"
)

# FIX: Include ONLY the master api_router. It contains all the others.
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the MemberFlow API!"}