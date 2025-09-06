# backend/app/crud/crud_payment.py
from decimal import Decimal

from sqlalchemy.orm import Session

from ..models import payment as payment_model


def create_pending_payment(db: Session, subscriber_id: int, plan_id: int, boc_hash: str, amount: Decimal) -> payment_model.Payment:
    db_payment = payment_model.Payment(
        subscriber_id=subscriber_id,
        plan_id=plan_id,
        boc_hash=boc_hash,
        amount=amount,
        status=payment_model.PaymentStatus.PENDING
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment_by_boc_hash(db: Session, boc_hash: str) -> payment_model.Payment | None:
    return db.query(payment_model.Payment).filter(payment_model.Payment.boc_hash == boc_hash).first()

def update_payment_status(db: Session, payment: payment_model.Payment, status: payment_model.PaymentStatus, subscription_id: int | None = None):
    payment.status = status
    if subscription_id:
        payment.subscription_id = subscription_id
    db.commit()
    return payment