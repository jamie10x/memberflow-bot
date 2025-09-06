# backend/app/api/endpoints/public.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...crud import crud_plan
from ...schemas import plan as plan_schema
from ..deps import get_db

router = APIRouter()

@router.get("/plans/{plan_id}", response_model=plan_schema.Plan)
def get_public_plan_details(
        plan_id: int,
        db: Session = Depends(get_db)
):
    """
    Public endpoint to get the details of a specific plan by its ID.
    """
    plan = crud_plan.get_plan_by_id(db=db, plan_id=plan_id) # We will create this CRUD function
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return plan