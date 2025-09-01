# backend/app/api/auth.py
import logging
import json
import hmac
import hashlib
from urllib.parse import unquote, parse_qs

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from ..core.config import settings
from ..crud import crud_user
from ..models.user import User as UserModel
from . import deps


def validate_init_data(init_data: str, bot_token: str) -> bool:
    try:
        vals = {
            k: unquote(v)
            for k, v in [pair.split("=", 1) for pair in init_data.split("&")]
        }
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(vals.items()) if k != "hash"
        )
        secret_key = hmac.new(
            b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256
        ).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(computed_hash, vals.get("hash", ""))
    except Exception as e:
        logging.error(f"initData validation error: {e}")
        return False


def get_init_data_header(x_telegram_init_data: str = Header(None)):
    if x_telegram_init_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Telegram-Init-Data header",
        )
    return x_telegram_init_data


def get_current_user(
        db: Session = Depends(deps.get_db),
        init_data: str = Depends(get_init_data_header),
) -> UserModel:
    # Validate integrity & authenticity
    if not validate_init_data(unquote(init_data), settings.BOT_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed: invalid initData",
        )

    # Parse and extract the 'user' JSON blob
    parsed_data = parse_qs(unquote(init_data))
    user_data_str = parsed_data.get("user", [None])[0]
    if not user_data_str:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed: missing user data",
        )

    try:
        user_data = json.loads(user_data_str)
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing user JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed: corrupt user data",
        )

    telegram_id = user_data.get("id")
    if not telegram_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed: invalid user ID",
        )

    user = crud_user.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found—please /start the bot first.",
        )

    logging.info(f"Authenticated Telegram user: {user.telegram_id}")
    return user
