import json
import logging
from fastapi import Request
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware as AiogramMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from services.auth import get_access_token


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, debug: bool):
        super().__init__(app)
        self.debug = debug
        self.logger = logging.getLogger("uvicorn")
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)

    async def dispatch(self, request: Request, call_next):
        # Log request details
        self.logger.debug(f"--> Request URL: {request.url}")
        self.logger.debug(f"--> Request method: {request.method}")
        self.logger.debug(f"--> Request headers: \n{json.dumps(dict(request.headers), indent=4)}")

        # Read and log request body
        try:
            data = await request.json()
            if data:
                self.logger.debug(f"--> Request body: \n{json.dumps(data, indent=4)}")
        except Exception as e:
            self.logger.debug("--> Request body: Empty or invalid")
            self.logger.warning(f"Failed to read request body: {e}")

        response = await call_next(request)

        # Log response details
        self.logger.debug(f"Response status code: {response.status_code}")
        return response


# Aiogram middleware for adding JWT token to events
class JWTMiddleware(AiogramMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if event:
            user = event.from_user
            access_token = await get_access_token(user)
            data["access_token"] = access_token  # Inject token into handler data
        return await handler(event, data)
