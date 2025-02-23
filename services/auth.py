import jwt
import time
import httpx
from aiogram.types import User

from app.config import settings
from services.redis import redis_client


async def fetch_jwt_token(user_data: User) -> dict:
    headers = {"X-Internal-API-Key": settings.INTERNAL_API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.AUTH_API_URL}/api/auth/bot_login", headers=headers, json=user_data.model_dump()
        )
        return response.json()


# Get or refresh JWT token from Redis
async def get_access_token(user: User) -> str:
    user_id = user.id
    redis_key = f"access_token:{user_id}"
    jwt_token = await redis_client.get(redis_key)
    if jwt_token:
        return jwt_token.decode("utf-8")

    # If no token, fetch a new one
    new_token = await fetch_jwt_token(user)
    access_token = new_token["access_token"]
    expires_at = jwt.decode(access_token, options={"verify_signature": False}).get("exp")
    await redis_client.set(redis_key, access_token, ex=expires_at - int(time.time()))

    return access_token
