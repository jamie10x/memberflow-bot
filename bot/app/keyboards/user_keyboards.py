# bot/app/keyboards/user_keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def get_dashboard_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard with a button to open the dashboard Mini App.
    """
    # WebAppInfo is a special object that tells Telegram this button should open a Mini App
    web_app_info = WebAppInfo(url=webapp_url)

    dashboard_button = InlineKeyboardButton(
        text="🚀 Open Dashboard",
        web_app=web_app_info
    )

    # InlineKeyboardMarkup is the container for our button
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[dashboard_button]]
    )
    return keyboard