# backend/app/api/api.py
from fastapi import APIRouter
from .endpoints import user, channel, plan, checkout

api_router = APIRouter()

# Root user endpoints (e.g., POST /users/)
api_router.include_router(user.router, prefix="/users", tags=["users"])

# Endpoints nested under a specific user, identified by their Telegram ID
api_router.include_router(channel.router, prefix="/users/{telegram_id}/channels", tags=["channels"])
api_router.include_router(plan.router, prefix="/users/{telegram_id}/plans", tags=["plans"])

# Customer-facing checkout endpoints
api_router.include_router(checkout.router, prefix="/checkout", tags=["checkout"])