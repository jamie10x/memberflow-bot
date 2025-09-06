# backend/app/models/payment.py
import enum
from sqlalchemy import Column, Integer, String, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False)

    # FIX: Added plan_id to link the payment directly to the plan being purchased.
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)

    boc_hash = Column(String, unique=True, index=True, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USDT")
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)

    subscriber = relationship("Subscriber")
    subscription = relationship("Subscription")
    plan = relationship("Plan")