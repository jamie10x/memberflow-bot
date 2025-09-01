# backend/app/api/endpoints/plan.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...crud import crud_plan, crud_user
from ...schemas import plan as plan_schema
from .. import deps

router = APIRouter()

@router.post("/", response_model=plan_schema.Plan)
def create_plan_for_user(
        telegram_id: int,  # Get the user's Telegram ID from the path
        plan_in: plan_schema.PlanCreate,
        db: Session = Depends(deps.get_db)
):
    """
    Create a new plan for a user via their Telegram ID.
    """
    user = crud_user.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with Telegram ID {telegram_id} not found. Please /start the bot first."
        )

    return crud_plan.create_user_plan(db=db, plan=plan_in, user_id=user.id)

@router.get("/", response_model=list[plan_schema.Plan])
def read_user_plans(
        telegram_id: int, # Get the user's Telegram ID from the path
        db: Session = Depends(deps.get_db)
):
    """
    Get all plans for a specific user via their Telegram ID.
    """
    user = crud_user.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with Telegram ID {telegram_id} not found."
        )

    return crud_plan.get_user_plans(db=db, user_id=user.id)