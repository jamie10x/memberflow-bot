# backend/app/api/endpoints/plan.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# FIX: Changed to specific imports
from ...crud import crud_plan
from ...schemas import plan as plan_schema
from .. import deps

router = APIRouter()

@router.post("/", response_model=plan_schema.Plan)
def create_plan_for_user(
        user_id: int,  # FIX: Get user_id from the path
        plan_in: plan_schema.PlanCreate,
        db: Session = Depends(deps.get_db)
):
    """
    Create a new plan for a user.
    """
    # FIX: Pass the user_id from the path
    return crud_plan.create_user_plan(db=db, plan=plan_in, user_id=user_id)

@router.get("/", response_model=list[plan_schema.Plan])
def read_user_plans(
        user_id: int, # FIX: Get user_id from the path
        db: Session = Depends(deps.get_db)
):
    """
    Get all plans for a specific user.
    """
    return crud_plan.get_user_plans(db=db, user_id=user_id)