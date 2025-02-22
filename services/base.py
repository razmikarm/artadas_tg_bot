import httpx
from fastapi import HTTPException
from app.config import settings


async def fetch_base_data(endpoint: str, method: str, data: dict, token: str | None = None):
    """Fetch data from the base API using JWT auth."""
    if token:
        headers = {"Authorization": f"Bearer {token}"}
    else:
        headers = {}

    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{settings.BASE_API_URL}{endpoint}", data, headers)
        if method.upper() == "GET" and response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch user data")
        return response.json()
