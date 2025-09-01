# backend/app/api/api.py
from fastapi import APIRouter
from .endpoints import user, channel, plan, checkout

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(channel.router, prefix="/users/{user_id}/channels", tags=["channels"])
api_router.include_router(plan.router, prefix="/users/{user_id}/plans", tags=["plans"])
api_router.include_router(checkout.router, prefix="/checkout", tags=["checkout"])