# backend/app/schemas/user.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# --- User Schemas ---

# Base properties shared by all user-related schemas
class UserBase(BaseModel):
    telegram_id: int
    username: str | None = None  # The `| None` makes it optional

# Properties required when creating a new user via the API
class UserCreate(UserBase):
    pass # No new fields needed for creation

# Properties that are present when reading a user from the database
class User(UserBase):
    id: int
    created_at: datetime

    # This tells Pydantic to read the data even if it's not a dict, but an ORM model
    model_config = ConfigDict(from_attributes=True)