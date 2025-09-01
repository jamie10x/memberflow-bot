# backend/app/schemas/subscriber.py
from pydantic import BaseModel, ConfigDict

class SubscriberBase(BaseModel):
    telegram_id: int
    username: str | None = None

class SubscriberCreate(SubscriberBase):
    pass

class Subscriber(SubscriberBase):
    id: int
    model_config = ConfigDict(from_attributes=True)