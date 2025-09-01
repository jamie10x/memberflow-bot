# backend/app/models/subscription.py
import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    INCOMPLETE = "incomplete" # For payments that haven't finalized

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)

    status = Column(Enum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.INCOMPLETE)

    start_date = Column(DateTime(timezone=True), server_default=func.now())
    # This will be crucial for checking access
    expires_at = Column(DateTime(timezone=True), nullable=True)

    subscriber = relationship("Subscriber", back_populates="subscriptions")
    plan = relationship("Plan") # We don't need a back-reference from Plan for now