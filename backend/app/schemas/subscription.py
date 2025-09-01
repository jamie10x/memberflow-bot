# backend/app/schemas/subscription.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..models.subscription import SubscriptionStatus

class SubscriptionBase(BaseModel):
    subscriber_id: int
    plan_id: int
    status: SubscriptionStatus

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    start_date: datetime
    expires_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)