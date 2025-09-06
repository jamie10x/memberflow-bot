# backend/app/api/endpoints/dashboard.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from decimal import Decimal

from ...crud import crud_plan, crud_channel, crud_payment_gateway, crud_subscription
from ...schemas import plan as plan_schema
from ...schemas import channel as channel_schema
from ...schemas import payment_gateway as gateway_schema
from ...schemas import subscription as subscription_schema
from ..deps import get_db
from ..auth import get_current_user
from ...models.user import User as UserModel
from ...models import plan as plan_model

router = APIRouter()

# Define a Pydantic model for the analytics response shape
class DashboardAnalytics(BaseModel):
    mrr: Decimal
    active_subscriptions: int
    subscribers: List[subscription_schema.Subscription]

# --- Analytics ---
@router.get("/analytics", response_model=DashboardAnalytics)
def read_my_analytics(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """
    Get key analytics and a list of active subscribers for the current user.
    """
    subscriptions = crud_subscription.get_active_subscriptions_by_creator(db, creator_id=current_user.id)

    mrr = Decimal(0)
    for sub in subscriptions:
        if sub.plan.interval == plan_model.PlanInterval.month:
            mrr += sub.plan.price
        elif sub.plan.interval == plan_model.PlanInterval.year:
            mrr += sub.plan.price / 12

    return DashboardAnalytics(
        mrr=round(mrr, 2),
        active_subscriptions=len(subscriptions),
        subscribers=subscriptions
    )

# --- Plans ---
@router.get("/plans", response_model=List[plan_schema.Plan])
def read_my_plans(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return crud_plan.get_user_plans(db=db, user_id=current_user.id)

@router.post("/plans", response_model=plan_schema.Plan, status_code=status.HTTP_201_CREATED)
def create_my_plan(plan_in: plan_schema.PlanCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    # MODIFIED: Validate that the channel_id provided belongs to the current user.
    user_channels = crud_channel.get_user_channels(db=db, user_id=current_user.id)
    if plan_in.channel_id not in [c.id for c in user_channels]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create plans for channels you own."
        )
    return crud_plan.create_user_plan(db=db, plan=plan_in, user_id=current_user.id)

@router.put("/plans/{plan_id}", response_model=plan_schema.Plan)
def update_my_plan(plan_id: int, plan_in: plan_schema.PlanCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    plan = crud_plan.get_plan_by_id(db, plan_id=plan_id)
    if not plan or plan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Plan not found or you do not have permission to edit it.")

    # MODIFIED: Also validate the channel on update.
    user_channels = crud_channel.get_user_channels(db=db, user_id=current_user.id)
    if plan_in.channel_id not in [c.id for c in user_channels]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only assign plans to channels you own."
        )

    return crud_plan.update_plan(db=db, plan=plan, plan_in=plan_in)

@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_plan(plan_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    plan = crud_plan.get_plan_by_id(db, plan_id=plan_id)
    if not plan or plan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Plan not found or you do not have permission to delete it.")
    # Add a check here to ensure no active subscriptions exist for this plan before deleting.
    # For MVP, we will allow deletion.
    crud_plan.delete_plan(db=db, plan_id=plan_id)
    return None

# --- Channels ---
@router.get("/channels", response_model=List[channel_schema.Channel])
def read_my_channels(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return crud_channel.get_user_channels(db=db, user_id=current_user.id)

# --- Payment Settings ---
@router.get("/payment-settings", response_model=gateway_schema.PaymentGateway | None)
def read_my_payment_settings(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return crud_payment_gateway.get_gateway_by_user_id(db=db, user_id=current_user.id)

@router.post("/payment-settings", response_model=gateway_schema.PaymentGateway)
def setup_payment_gateway(gateway_in: gateway_schema.PaymentGatewayCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return crud_payment_gateway.create_or_update_gateway(db=db, user_id=current_user.id, gateway_obj=gateway_in)