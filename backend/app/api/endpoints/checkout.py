# backend/app/api/endpoints/checkout.py
import time

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from .. import deps
from ...core.config import settings
from ...crud import (crud_subscriber, crud_subscription, crud_payment, crud_plan, crud_payment_gateway)
from ...models import payment as payment_model
from ...schemas import subscriber as subscriber_schema
from ...schemas import subscription as subscription_schema
from ...services.telegram_service import telegram_service
from ...services.ton_service import TONService

router = APIRouter()

# DTOs
class InitPaymentRequest(BaseModel):
    plan_id: int
    telegram_id: int
    username: str | None = None

class InitPaymentResponse(BaseModel):
    boc_hash: str # This is our unique memo
    to_wallet: str
    amount: str
    memo: str

class VerifyPaymentRequest(BaseModel):
    boc_hash: str


# Create an instance of the TON Service
ton_service = TONService(api_key=settings.TONCENTER_API_KEY)


@router.post("/init-ton-payment", response_model=InitPaymentResponse)
def init_ton_payment(
        request: InitPaymentRequest,
        db: Session = Depends(deps.get_db)
):
    # ... (this endpoint remains exactly the same)
    subscriber_data = subscriber_schema.SubscriberCreate(telegram_id=request.telegram_id, username=request.username)
    subscriber = crud_subscriber.get_or_create_subscriber(db, subscriber_in=subscriber_data)
    plan = crud_plan.get_plan_by_id(db, plan_id=request.plan_id)
    if not plan: raise HTTPException(status_code=404, detail="Plan not found")
    creator_gateway = crud_payment_gateway.get_gateway_by_user_id(db, user_id=plan.user_id)
    if not creator_gateway or not creator_gateway.credentials.get("wallet_address"):
        raise HTTPException(status_code=500, detail="Creator has not configured a payment address.")
    memo = f"memberflow-{request.plan_id}-{subscriber.id}-{int(time.time())}"
    crud_payment.create_pending_payment(db, subscriber_id=subscriber.id, plan_id=plan.id, boc_hash=memo, amount=plan.price)
    return InitPaymentResponse(
        boc_hash=memo,
        to_wallet=creator_gateway.credentials["wallet_address"],
        # NOTE: For Jettons like USDT, the decimals can vary (usually 6).
        # We'll assume 6 decimals for nano-USDT. For TON coin itself, it's 9.
        amount=str(int(plan.price * 1_000_000)),
        memo=memo
    )


@router.post("/verify-ton-payment", response_model=subscription_schema.Subscription)
async def verify_ton_payment(
        request: VerifyPaymentRequest,
        db: Session = Depends(deps.get_db)
):
    pending_payment = crud_payment.get_payment_by_boc_hash(db, boc_hash=request.boc_hash)
    if not pending_payment or pending_payment.status != payment_model.PaymentStatus.PENDING:
        raise HTTPException(status_code=404, detail="Payment record not found or already processed.")

    # MODIFIED: Eagerly load the channel relationship for the plan to avoid an extra query
    plan = crud_plan.get_plan_by_id(db, plan_id=pending_payment.plan_id, options=[joinedload("channel")])
    if not plan or not plan.channel:
        raise HTTPException(status_code=500, detail="Configuration error: The purchased plan is not linked to a channel.")

    creator_gateway = crud_payment_gateway.get_gateway_by_user_id(db, user_id=plan.user_id)

    # --- REAL ON-CHAIN VERIFICATION ---
    payment_verified = await ton_service.find_and_verify_transaction(
        recipient_address=creator_gateway.credentials["wallet_address"],
        expected_amount=int(plan.price * 1_000_000), # Amount in nano-USDT
        expected_memo=request.boc_hash
    )

    if not payment_verified:
        crud_payment.update_payment_status(db, payment=pending_payment, status=payment_model.PaymentStatus.FAILED)
        raise HTTPException(status_code=400, detail="Payment could not be confirmed on the blockchain. Please try again or contact support if you have already paid.")
    # --- END OF VERIFICATION ---

    subscription = crud_subscription.create_subscription_from_payment(db, payment=pending_payment)
    crud_payment.update_payment_status(db, payment=pending_payment, status=payment_model.PaymentStatus.COMPLETED, subscription_id=subscription.id)

    # --- Grant Access Logic ---
    subscriber = crud_subscriber.get_subscriber_by_id(db, subscriber_id=subscription.subscriber_id)

    # MODIFIED: No longer need to fetch a list of channels. We use the specific one from the plan.
    channel_to_join = plan.channel

    if subscriber and channel_to_join:
        invite_link = await telegram_service.create_invite_link(chat_id=channel_to_join.telegram_channel_id)
        if invite_link:
            message_text = (
                f"🎉 Thank you for your subscription!\n\n"
                f"Here is your personal invite link to join **{channel_to_join.title}**:\n{invite_link}"
            )
            await telegram_service.send_dm(chat_id=subscriber.telegram_id, text=message_text)

    return subscription