import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiogram import Dispatcher, Bot, types

from app.config import settings
from app.handlers import router
from app.middleware import LoggingMiddleware, JWTMiddleware
from services.tma import router as tma_router


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
        await dp.feed_update(bot, telegram_update)
    except Exception as e:
        # Log the error
        print(f"Error processing update: {e}")
    return {"status": "ok"}


dp.message.middleware(JWTMiddleware())
app.add_middleware(LoggingMiddleware, debug=settings.DEBUG)
app.include_router(tma_router, prefix="/tma")
