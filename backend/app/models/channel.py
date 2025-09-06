# backend/app/models/channel.py
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base # Get Base from the central source

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    telegram_channel_id = Column(BigInteger, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="channels")
    # ADDED: A channel can have multiple plans associated with it.
    plans = relationship("Plan", back_populates="channel")