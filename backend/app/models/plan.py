# backend/app/models/plan.py
import enum
from sqlalchemy import Column, Integer, String, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base

class PlanInterval(enum.Enum):
    month = "month"
    year = "year"

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    interval = Column(Enum(PlanInterval), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    # FIX: Changed 'owner' to 'user' to match the User model's 'back_populates'
    user = relationship("User", back_populates="plans")