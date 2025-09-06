# bot/app/handlers/user_handlers.py
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
import logging

from bot.app.core.config import settings # Import settings
from bot.app.keyboards.user_keyboards import get_dashboard_keyboard
from bot.app.services.api_client import api_client

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Handler for the /start command.
    Creates a user account via the API and then greets them.
    """
    user = message.from_user
    logging.info(f"User {user.id} ({user.username}) started the bot.")

    try:
        response = await api_client.create_user(
            telegram_id=user.id,
            username=user.username
        )

        if response.status_code == 201: # 201 Created
            logging.info(f"Successfully created new user in backend for {user.id}")
            await message.answer(
                f"Hello, {user.full_name}! 👋\n\n"
                "Welcome to MemberFlow! Your account has been created.\n\n"
                "Now, let's get you set up. Please add me as an Admin to the private channel you want to manage."
            )
        elif response.status_code == 400: # 400 Bad Request (user already exists)
            logging.info(f"User {user.id} already exists in backend.")
            await message.answer(
                f"Welcome back, {user.full_name}! 👋\n\n"
                "It looks like you already have an account. To manage your channels or create plans, use the /dashboard command."
            )
        else:
            logging.error(f"Failed to create user {user.id}. API response: {response.status_code} - {response.text}")
            await message.answer("Sorry, something went wrong on our end. Please try again later.")

    except Exception as e:
        logging.exception(f"An exception occurred while trying to create user {user.id}: {e}")
        await message.answer("Sorry, I couldn't connect to our services. Please try again in a moment.")


@user_router.message(Command("dashboard"))
async def cmd_dashboard(message: types.Message):
    """
    Handler for the /dashboard command.
    Replies with a button to open the Mini App dashboard.
    """
    # MODIFIED: URL is now loaded from config instead of being hardcoded.
    await message.answer(
        "Welcome to your MemberFlow dashboard! Here you can manage your plans, view subscribers, and track your revenue.",
        reply_markup=get_dashboard_keyboard(webapp_url=settings.MINI_APP_URL)
    )