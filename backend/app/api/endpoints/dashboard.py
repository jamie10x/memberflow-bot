# backend/app/api/endpoints/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...crud import crud_plan, crud_channel
from ...schemas import plan as plan_schema
from ...schemas import channel as channel_schema
from ..deps import get_db
from ..auth import get_current_user
from ...models.user import User as UserModel

router = APIRouter()

@router.get("/plans", response_model=list[plan_schema.Plan])
def read_my_plans(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Get all plans for the currently authenticated user."""
    return crud_plan.get_user_plans(db=db, user_id=current_user.id)

@router.get("/channels", response_model=list[channel_schema.Channel])
def read_my_channels(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Get all channels for the currently authenticated user."""
    return crud_channel.get_user_channels(db=db, user_id=current_user.id)