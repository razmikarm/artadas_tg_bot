import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiogram import Dispatcher, Bot, types

from app.config import settings
from app.handlers import router
from app.middleware import LoggingMiddleware

from services.auth import get_jwt_token

log = logging.getLogger("uvicorn")
log.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup logic here
    log.info("Starting up...")
    log.debug(f"Setting Webhook URL: {settings.WEBHOOK_URL}")
    await bot.set_webhook(f"{settings.WEBHOOK_URL}/webhook")
    yield  # Control returns to the application during runtime

    # Perform any shutdown logic here if needed
    await bot.delete_webhook()


# Initialize FastAPI app and aiogram bot
app = FastAPI(lifespan=lifespan, debug=settings.DEBUG, docs_url=None, redoc_url=None)
dp = Dispatcher()
dp.include_router(router)
bot = Bot(token=settings.TG_BOT_TOKEN)


@app.post("/webhook")
async def telegram_webhook(update: dict):
    try:
        telegram_update = types.Update.model_validate(update)
        jwt_token = await get_jwt_token(telegram_update.message.from_user.model_dump())
        message_copy = telegram_update.message.model_copy(update={"auth_jwt_token": jwt_token})
        telegram_update_copy = telegram_update.model_copy(update={"message": message_copy})
        await dp.feed_update(bot, telegram_update_copy)
    except Exception as e:
        # Log the error
        print(f"Error processing update: {e}")
    return {"status": "ok"}


app.add_middleware(LoggingMiddleware, debug=settings.DEBUG)
