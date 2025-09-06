# backend/app/schemas/plan.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from ..models.plan import PlanInterval

class PlanBase(BaseModel):
    name: str
    price: Decimal
    currency: str
    interval: PlanInterval
    # ADDED: channel_id is now a required field when creating/reading a plan.
    channel_id: int

class PlanCreate(PlanBase):
    pass

class Plan(PlanBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)