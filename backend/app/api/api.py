# backend/app/api/api.py
from fastapi import APIRouter
from backend.app.api.endpoints import user, channel, plan, checkout, dashboard

api_router = APIRouter()

# Root user endpoints (e.g., POST /users/)
api_router.include_router(user.router, prefix="/users", tags=["users"])

# Endpoints for bot/admin actions, identified by Telegram ID
api_router.include_router(channel.router, prefix="/users/{telegram_id}/channels", tags=["bot-actions"])
api_router.include_router(plan.router, prefix="/users/{telegram_id}/plans", tags=["bot-actions"])

# Endpoints for the authenticated user's dashboard (Mini App)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

# Customer-facing checkout endpoints
api_router.include_router(checkout.router, prefix="/checkout", tags=["checkout"])