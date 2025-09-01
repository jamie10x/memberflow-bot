# bot/app/services/api_client.py
import httpx
from ..core.config import settings

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def create_user(self, telegram_id: int, username: str | None) -> httpx.Response:
        """
        Sends a request to the backend to create a new user.
        """
        url = f"{self.base_url}/users/"
        payload = {"telegram_id": telegram_id, "username": username}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            return response

    async def link_channel(self, user_telegram_id: int, channel_id: int, title: str) -> httpx.Response:
        """
        Sends a request to the backend to link a channel to a user.
        """
        # FIX: The URL uses telegram_id in the path now
        url = f"{self.base_url}/users/{user_telegram_id}/channels/"
        payload = {"telegram_channel_id": channel_id, "title": title}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            return response

# Create a single, reusable instance of the client
api_client = APIClient(base_url=settings.BACKEND_API_URL)