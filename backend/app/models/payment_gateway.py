# backend/app/models/payment_gateway.py
import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base

class GatewayType(str, enum.Enum):
    TON_WALLET = "ton_wallet"
    STRIPE = "stripe"
    PADDLE = "paddle"

class PaymentGateway(Base):
    __tablename__ = "payment_gateways"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    gateway_type = Column(Enum(GatewayType), nullable=False)

    # A flexible JSON field to store credentials
    # For TON: {'wallet_address': 'UQA...'}
    # For Stripe: {'account_id': 'acct_...'}
    credentials = Column(JSON, nullable=False)

    user = relationship("User")