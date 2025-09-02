# backend/app/api/endpoints/dashboard.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ...crud import crud_plan, crud_channel, crud_payment_gateway
from ...schemas import plan as plan_schema
from ...schemas import channel as channel_schema
from ...schemas import payment_gateway as gateway_schema
from ..deps import get_db
from ..auth import get_current_user
from ...models.user import User as UserModel

router = APIRouter()

# --- GET Endpoints ---
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

@router.get("/payment-settings", response_model=gateway_schema.PaymentGateway | None)
def read_my_payment_settings(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Get the payment settings for the currently authenticated user."""
    return crud_payment_gateway.get_gateway_by_user_id(db=db, user_id=current_user.id)

# --- POST Endpoints ---
@router.post("/plans", response_model=plan_schema.Plan, status_code=status.HTTP_201_CREATED)
def create_my_plan(
        plan_in: plan_schema.PlanCreate,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Create a new plan for the currently authenticated user."""
    return crud_plan.create_user_plan(db=db, plan=plan_in, user_id=current_user.id)

@router.post("/payment-settings", response_model=gateway_schema.PaymentGateway)
def setup_payment_gateway(
        gateway_in: gateway_schema.PaymentGatewayCreate,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    """Set or update the payment gateway for the authenticated user."""
    return crud_payment_gateway.create_or_update_gateway(
        db=db, user_id=current_user.id, gateway_obj=gateway_in
    )