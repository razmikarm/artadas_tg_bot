from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    REDIS_URL: str
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


settings = Settings()
