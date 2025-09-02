# backend/app/crud/crud_payment_gateway.py
from sqlalchemy.orm import Session
from ..models import payment_gateway as gateway_model
from ..schemas import payment_gateway as gateway_schema

def create_or_update_gateway(db: Session, user_id: int, gateway_obj: gateway_schema.PaymentGatewayCreate) -> gateway_model.PaymentGateway:
    """
    Creates a new payment gateway setting for a user, or updates the existing one.
    """
    db_gateway = db.query(gateway_model.PaymentGateway).filter(gateway_model.PaymentGateway.user_id == user_id).first()

    if db_gateway:
        # Update existing
        db_gateway.gateway_type = gateway_obj.gateway_type
        db_gateway.credentials = gateway_obj.credentials
    else:
        # Create new
        db_gateway = gateway_model.PaymentGateway(**gateway_obj.model_dump(), user_id=user_id)
        db.add(db_gateway)

    db.commit()
    db.refresh(db_gateway)
    return db_gateway

def get_gateway_by_user_id(db: Session, user_id: int) -> gateway_model.PaymentGateway | None:
    """
    Retrieves the payment gateway setting for a specific user.
    """
    return db.query(gateway_model.PaymentGateway).filter(gateway_model.PaymentGateway.user_id == user_id).first()