# backend/app/main.py
from fastapi import FastAPI
from .api.endpoints import user  # Import the new user router

# Create an instance of the FastAPI class
app = FastAPI(
    title="MemberFlow API",
    description="The backend API for the MemberFlow Telegram subscription bot.",
    version="0.1.0"
)

# Include the user router with a prefix and tags
app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"status": "ok", "message": "Welcome to the MemberFlow API!"}