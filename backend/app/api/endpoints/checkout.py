# backend/app/api/endpoints/checkout.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

# FIX: Changed to specific imports
from ...crud import crud_subscriber, crud_subscription
from ...schemas import subscription as subscription_schema
from ...schemas import subscriber as subscriber_schema
from .. import deps

router = APIRouter()

class PurchaseRequest(BaseModel):
    plan_id: int
    telegram_id: int
    username: str | None = None

@router.post("/purchase", response_model=subscription_schema.Subscription)
def process_purchase(
        purchase_in: PurchaseRequest,
        db: Session = Depends(deps.get_db)
):
    """
    Simulates a successful purchase of a plan.
    """
    subscriber_data = subscriber_schema.SubscriberCreate(
        telegram_id=purchase_in.telegram_id,
        username=purchase_in.username
    )
    # FIX: Call the crud function directly
    subscriber = crud_subscriber.get_or_create_subscriber(db, subscriber_in=subscriber_data)

    try:
        # FIX: Call the crud function directly
        subscription = crud_subscription.create_subscription(
            db=db,
            subscriber_id=subscriber.id,
            plan_id=purchase_in.plan_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return subscription