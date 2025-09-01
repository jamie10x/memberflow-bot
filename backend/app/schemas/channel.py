# backend/app/schemas/channel.py
from pydantic import BaseModel, ConfigDict

class ChannelBase(BaseModel):
    telegram_channel_id: int
    title: str

class ChannelCreate(ChannelBase):
    # FIX: We REMOVED user_id from here. It does not belong in the request body.
    pass

class Channel(ChannelBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)