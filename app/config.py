from pydantic import model_validator
from pydantic_settings import BaseSettings

from services.ngrok import get_ngrok_url


class Settings(BaseSettings):
    DEBUG: bool = False

    REDIS_URL: str
    NGROK_URL: str
    MINI_APP_URL: str
    AUTH_API_URL: str
    BASE_API_URL: str
    INTERNAL_API_KEY: str

    WEBHOOK_URL: str
    TG_BOT_TOKEN: str
    TG_FREE_GROUP_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @model_validator(mode="before")
    def set_default_value_if_empty(cls, values):
        if not values.get("WEBHOOK_URL"):
            values["WEBHOOK_URL"] = get_ngrok_url(values.get("NGROK_URL"))
        return values


settings = Settings()
