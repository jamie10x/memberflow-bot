# backend/app/schemas/payment_gateway.py
from pydantic import BaseModel, ConfigDict
from ..models.payment_gateway import GatewayType

class PaymentGatewayBase(BaseModel):
    gateway_type: GatewayType
    credentials: dict

class PaymentGatewayCreate(PaymentGatewayBase):
    pass

class PaymentGateway(PaymentGatewayBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)