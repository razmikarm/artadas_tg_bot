import httpx
from fastapi import HTTPException
from app.config import settings


async def get_jwt_token(user_data: dict):
    """Get JWT token from the auth service."""

    # Mocking data
    # return {
    #     "access_token": "asdasfDSFSFASDasfdsdfsdKLJlkjlkJzxcZXC"
    # }

    headers = {"X-Internal-API-Key": settings.INTERNAL_API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.AUTH_API_URL}/api/auth/bot_login", headers=headers, json=user_data)
        return response.json()["access_token"]
