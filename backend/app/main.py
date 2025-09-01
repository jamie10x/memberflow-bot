# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.app.api.api import api_router

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MemberFlow API",
    description="The backend API for the MemberFlow Telegram subscription bot.",
    version="0.1.0"
)


# --- Add a middleware to log all incoming request headers ---
@app.middleware("http")
async def log_headers(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    logger.info("Headers:")
    for header, value in request.headers.items():
        logger.info(f"  {header}: {value}")
    response = await call_next(request)
    return response
# --- End of logging middleware ---


# --- CORS Middleware (Make it extra permissive for debugging) ---
origins = [
    "*",
    "https://c55919e87a0e.ngrok-free.app",
    "http://192.168.200.104:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow credentials (important for some auth flows)
    allow_methods=["*"],     # Allow all methods
    allow_headers=["*"],     # Allow all headers, including our custom one
)
# --- End of CORS Middleware ---


app.include_router(api_router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the MemberFlow API!"}