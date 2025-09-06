# backend/app/crud/crud_subscriber.py
from sqlalchemy.orm import Session
from ..models import subscriber as subscriber_model
from ..schemas import subscriber as subscriber_schema

def get_subscriber_by_id(db: Session, subscriber_id: int) -> subscriber_model.Subscriber | None:
    """
    Finds a subscriber by their internal database ID.
    """
    return db.query(subscriber_model.Subscriber).filter(subscriber_model.Subscriber.id == subscriber_id).first()

def get_or_create_subscriber(db: Session, subscriber_in: subscriber_schema.SubscriberCreate) -> subscriber_model.Subscriber:
    """
    Finds a subscriber by telegram_id. If not found, creates a new one.
    """
    subscriber = db.query(subscriber_model.Subscriber).filter(subscriber_model.Subscriber.telegram_id == subscriber_in.telegram_id).first()
    if not subscriber:
        subscriber = subscriber_model.Subscriber(
            telegram_id=subscriber_in.telegram_id,
            username=subscriber_in.username
        )
        db.add(subscriber)
        db.commit()
        db.refresh(subscriber)
    return subscriber