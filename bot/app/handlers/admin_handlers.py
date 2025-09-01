# bot/app/handlers/admin_handlers.py
import logging
from aiogram import Router, types

# We will use the pre-built transition objects provided by the filter itself
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, PROMOTED_TRANSITION

from ..services.api_client import api_client

admin_router = Router()


# The filter is now a single, pre-built object passed into the decorator
@admin_router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=PROMOTED_TRANSITION
    )
)
async def bot_added_as_admin(event: types.ChatMemberUpdated):
    """
    Handles the event when the bot is promoted to an admin in a channel.
    """
    user_telegram_id = event.from_user.id
    channel_telegram_id = event.chat.id
    channel_title = event.chat.title
    logging.info(f"Bot was promoted to admin in channel {channel_telegram_id} ('{channel_title}') by user {user_telegram_id}.")

    # --- API Integration ---
    try:
        response = await api_client.link_channel(
            user_telegram_id=user_telegram_id,
            channel_id=channel_telegram_id,
            title=channel_title
        )

        if response.status_code == 200:
            logging.info(f"Successfully linked channel {channel_telegram_id} to user {user_telegram_id} in backend.")
            # Send a confirmation message to the user in their private chat
            await event.bot.send_message(
                chat_id=user_telegram_id,
                text=f"✅ Great! I've successfully connected to your channel: **{channel_title}**.\n\n"
                     "You're all set! Now you can create subscription plans by using the /dashboard command."
            )
        else:
            # Note: We check for 404 specifically, in case the user hasn't /start'ed the bot yet.
            if response.status_code == 404:
                error_detail = "It seems you haven't started a chat with me yet. Please send me a /start message first."
            else:
                error_detail = response.text

            logging.error(f"Failed to link channel {channel_telegram_id}. API response: {response.status_code} - {error_detail}")
            await event.bot.send_message(
                chat_id=user_telegram_id,
                text=f"❌ I was added to **{channel_title}**, but I couldn't link it to your account. {error_detail}"
            )

    except Exception as e:
        logging.exception(f"An exception occurred while linking channel {channel_telegram_id}: {e}")