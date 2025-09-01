# backend/app/crud/crud_subscription.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..models import subscription as subscription_model
from ..models import plan as plan_model # We need the plan to calculate the expiry
from ..schemas import subscription as subscription_schema

def create_subscription(db: Session, subscriber_id: int, plan_id: int) -> subscription_model.Subscription:
    """
    Creates a new subscription for a subscriber to a specific plan
    and calculates the expiration date.
    """
    # 1. Fetch the plan to get its interval
    plan = db.query(plan_model.Plan).filter(plan_model.Plan.id == plan_id).first()
    if not plan:
        # This should ideally not happen if the plan_id is validated,
        # but it's good practice to handle it.
        raise ValueError(f"Plan with id {plan_id} not found.")

    # 2. Calculate the expiration date
    now = datetime.utcnow()
    if plan.interval == plan_model.PlanInterval.month:
        expires_at = now + timedelta(days=30) # Simple 30 days for now
    elif plan.interval == plan_model.PlanInterval.year:
        expires_at = now + timedelta(days=365) # Simple 365 days for now
    else:
        # Handle unexpected interval
        raise ValueError(f"Unknown plan interval: {plan.interval}")

    # 3. Create the subscription record
    db_subscription = subscription_model.Subscription(
        subscriber_id=subscriber_id,
        plan_id=plan_id,
        status=subscription_model.SubscriptionStatus.ACTIVE, # It's active upon creation
        start_date=now,
        expires_at=expires_at
    )

    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription