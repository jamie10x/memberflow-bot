# backend/app/api/endpoints/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Corrected imports
from ...schemas import user as user_schema
from ...crud import crud_user
from .. import deps

# APIRouter allows us to group related endpoints
router = APIRouter()

@router.post("/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_new_user(
        user_in: user_schema.UserCreate,
        db: Session = Depends(deps.get_db)
):
    """
    Create a new user.
    This is the primary endpoint for onboarding a creator.
    """
    # Check if a user with this telegram_id already exists
    existing_user = crud_user.get_user_by_telegram_id(db, telegram_id=user_in.telegram_id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this Telegram ID already exists."
        )

    # If not, create the new user
    user = crud_user.create_user(db=db, user=user_in)
    return user