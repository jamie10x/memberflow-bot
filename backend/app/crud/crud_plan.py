# backend/app/crud/crud_plan.py
from sqlalchemy.orm import Session, Query
from typing import List, Optional
from ..models import plan as plan_model
from ..schemas import plan as plan_schema

def get_plan_by_id(db: Session, plan_id: int, options: Optional[List] = None) -> plan_model.Plan | None:
    # MODIFIED: Allow passing query options for eager loading
    query: Query = db.query(plan_model.Plan)
    if options:
        query = query.options(*options)
    return query.filter(plan_model.Plan.id == plan_id).first()

def create_user_plan(db: Session, plan: plan_schema.PlanCreate, user_id: int) -> plan_model.Plan:
    db_plan = plan_model.Plan(**plan.model_dump(), user_id=user_id)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_user_plans(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[plan_model.Plan]:
    return db.query(plan_model.Plan).filter(plan_model.Plan.user_id == user_id).offset(skip).limit(limit).all()

def update_plan(db: Session, plan: plan_model.Plan, plan_in: plan_schema.PlanCreate) -> plan_model.Plan:
    """Updates a plan's details."""
    plan_data = plan_in.model_dump()
    for key, value in plan_data.items():
        setattr(plan, key, value)
    db.commit()
    db.refresh(plan)
    return plan

def delete_plan(db: Session, plan_id: int):
    """Deletes a plan."""
    plan = db.query(plan_model.Plan).get(plan_id)
    if plan:
        db.delete(plan)
        db.commit()
    return None