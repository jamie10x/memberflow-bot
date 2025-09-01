# backend/app/crud/crud_channel.py
from sqlalchemy.orm import Session
from ..models import channel as channel_model
from ..schemas import channel as channel_schema

def create_user_channel(db: Session, channel: channel_schema.ChannelCreate, user_id: int) -> channel_model.Channel:
    db_channel = channel_model.Channel(**channel.model_dump(), user_id=user_id)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def get_user_channels(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[channel_model.Channel]:
    return db.query(channel_model.Channel).filter(channel_model.Channel.user_id == user_id).offset(skip).limit(limit).all()