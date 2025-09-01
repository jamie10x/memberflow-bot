# backend/app/api/endpoints/channel.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...crud import crud_channel
from ...schemas import channel as channel_schema
from .. import deps

router = APIRouter()

@router.post("/", response_model=channel_schema.Channel)
def create_channel_for_user(
        user_id: int,  # This comes from the URL path, e.g., /users/1/channels/
        channel_in: channel_schema.ChannelCreate, # The body only contains channel info now
        db: Session = Depends(deps.get_db)
):
    """
    Create a new channel linked to a user.
    """
    return crud_channel.create_user_channel(db=db, channel=channel_in, user_id=user_id)

@router.get("/", response_model=list[channel_schema.Channel])
def read_user_channels(
        user_id: int,
        db: Session = Depends(deps.get_db)
):
    """
    Get all channels for a specific user.
    """
    return crud_channel.get_user_channels(db=db, user_id=user_id)