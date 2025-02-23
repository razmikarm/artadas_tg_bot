import httpx
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.config import settings

router = APIRouter()


@router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def tma_proxy_router(full_path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{settings.MINI_APP_URL}/{full_path}",
            headers=request.headers.raw,
            content=await request.body(),
        )
        return StreamingResponse(
            response.aiter_raw(),
            status_code=response.status_code,
            headers=dict(response.headers),
        )
