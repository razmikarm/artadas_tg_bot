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
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            content=await request.body(),
        )

        # Remove content-encoding to prevent FastAPI from trying to decompress
        headers = dict(response.headers)
        headers.pop("content-encoding", None)

        return StreamingResponse(
            response.aiter_bytes(),
            status_code=response.status_code,
            headers=headers,
        )
