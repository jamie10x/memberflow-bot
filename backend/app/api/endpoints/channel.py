# backend/app/api/endpoints/channel.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...crud import crud_channel, crud_user
from ...schemas import channel as channel_schema
from .. import deps

router = APIRouter()

@router.post("/", response_model=channel_schema.Channel)
def create_channel_for_user(
        telegram_id: int,  # Get the user's Telegram ID from the path
        channel_in: channel_schema.ChannelCreate,
        db: Session = Depends(deps.get_db)
):
    """
    Create a new channel and link it to a user via their Telegram ID.
    """
    # First, find the internal user record based on the provided telegram_id
    user = crud_user.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with Telegram ID {telegram_id} not found. Please /start the bot first."
        )

    # Now, create the channel using the found user's internal ID
    return crud_channel.create_user_channel(db=db, channel=channel_in, user_id=user.id)

@router.get("/", response_model=list[channel_schema.Channel])
def read_user_channels(
        telegram_id: int, # Get the user's Telegram ID from the path
        db: Session = Depends(deps.get_db)
):
    """
    Get all channels for a specific user via their Telegram ID.
    """
    # First, find the internal user record
    user = crud_user.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with Telegram ID {telegram_id} not found."
        )

    # Now, retrieve the channels using the found user's internal ID
    return crud_channel.get_user_channels(db=db, user_id=user.id)