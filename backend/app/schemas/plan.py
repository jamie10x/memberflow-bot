# backend/app/schemas/plan.py
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from ..models.plan import PlanInterval

class PlanBase(BaseModel):
    name: str
    price: Decimal
    currency: str
    interval: PlanInterval

class PlanCreate(PlanBase):
    # FIX: user_id is not needed here because it comes from the path.
    pass

class Plan(PlanBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)