# backend/app/models/subscriber.py
from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import relationship

from ..core.database import Base

class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, unique=False, nullable=True) # Usernames can change, so not unique

    subscriptions = relationship("Subscription", back_populates="subscriber")