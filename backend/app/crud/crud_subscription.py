# backend/app/crud/crud_subscription.py

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session, joinedload

from ..models import payment as payment_model
from ..models import plan as plan_model
from ..models import subscription as subscription_model, Subscription


def create_subscription_from_payment(db: Session, payment: payment_model.Payment) -> subscription_model.Subscription:
    """
    Creates a new subscription based on a completed payment.
    """
    plan = db.query(plan_model.Plan).filter(plan_model.Plan.id == payment.plan_id).first()
    if not plan:
        raise ValueError(f"Plan with id {payment.plan_id} associated with payment not found.")

    now = datetime.now(timezone.utc)
    if plan.interval == plan_model.PlanInterval.month:
        expires_at = now + timedelta(days=30)
    elif plan.interval == plan_model.PlanInterval.year:
        expires_at = now + timedelta(days=365)
    else:
        raise ValueError(f"Unknown plan interval: {plan.interval}")

    db_subscription = subscription_model.Subscription(
        subscriber_id=payment.subscriber_id,
        plan_id=payment.plan_id,
        status=subscription_model.SubscriptionStatus.ACTIVE,
        start_date=now,
        expires_at=expires_at
    )

    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_active_subscriptions_by_creator(db: Session, creator_id: int) -> list[type[Subscription]]:
    """
    Fetches all active subscriptions for a given creator by joining through the plans table.
    It eagerly loads the related plan and subscriber data to prevent extra queries.
    """
    now = datetime.now(timezone.utc)
    return (
        db.query(subscription_model.Subscription)
        .join(plan_model.Plan)
        .filter(
            plan_model.Plan.user_id == creator_id,
            subscription_model.Subscription.status == subscription_model.SubscriptionStatus.ACTIVE,
            subscription_model.Subscription.expires_at > now
        )
        .options(
            joinedload(subscription_model.Subscription.plan),
            joinedload(subscription_model.Subscription.subscriber) # Eager load subscriber details
        )
        .order_by(subscription_model.Subscription.expires_at.desc())
        .all()
    )