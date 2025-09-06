# backend/app/services/telegram_service.py
import httpx
import logging
from ..core.config import settings

class TelegramService:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def create_invite_link(self, chat_id: int) -> str | None:
        """
        Creates a new single-use invite link for a given chat.
        """
        url = f"{self.api_url}/createChatInviteLink"
        payload = {
            "chat_id": chat_id,
            "member_limit": 1, # Crucial for security: one link, one user
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status() # Raise an exception for bad status codes
                data = response.json()
                if data.get("ok"):
                    return data["result"]["invite_link"]
                else:
                    logging.error(f"Telegram API error creating invite link: {data.get('description')}")
                    return None
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error creating invite link: {e.response.text}")
            return None
        except Exception as e:
            logging.exception(f"Exception in create_invite_link: {e}")
            return None

    async def send_dm(self, chat_id: int, text: str) -> bool:
        """
        Sends a direct message to a user.
        """
        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("ok", False)
        except Exception as e:
            logging.exception(f"Exception in send_dm: {e}")
            return False

# Create a single instance to be used throughout the app
telegram_service = TelegramService(bot_token=settings.BOT_TOKEN)