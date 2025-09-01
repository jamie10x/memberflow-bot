# backend/app/crud/crud_plan.py
from sqlalchemy.orm import Session
from ..models import plan as plan_model
from ..schemas import plan as plan_schema

def create_user_plan(db: Session, plan: plan_schema.PlanCreate, user_id: int) -> plan_model.Plan:
    """
    Create a new plan for a specific user.
    """
    db_plan = plan_model.Plan(**plan.model_dump(), user_id=user_id)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_user_plans(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[plan_model.Plan]:
    """
    Retrieve all plans for a specific user.
    """
    return db.query(plan_model.Plan).filter(plan_model.Plan.user_id == user_id).offset(skip).limit(limit).all()