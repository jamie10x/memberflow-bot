# backend/app/crud/crud_user.py
from sqlalchemy.orm import Session

# Correct, specific imports with aliases
from ..models import user as user_model
from ..schemas import user as user_schema


def get_user_by_telegram_id(db: Session, telegram_id: int) -> user_model.User | None:
    """
    Fetches a user from the database by their Telegram ID.
    """
    return db.query(user_model.User).filter(user_model.User.telegram_id == telegram_id).first()


def create_user(db: Session, user: user_schema.UserCreate) -> user_model.User:
    """
    Creates a new user in the database.
    """
    # Create a new User ORM object from the Pydantic schema data
    db_user = user_model.User(
        telegram_id=user.telegram_id,
        username=user.username
    )
    # Add the new user object to the session
    db.add(db_user)
    # Commit the changes to the database
    db.commit()
    # Refresh the object to get the database-generated values (like id, created_at)
    db.refresh(db_user)
    return db_user