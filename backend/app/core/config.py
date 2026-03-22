from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "WardrobeIQ"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database
    DATABASE_URL: str = "mysql+pymysql://wardrobeiq:wardrobeiq@db:3306/wardrobeiq"

    # Image storage
    UPLOAD_DIR: str = "/app/uploads"
    MAX_IMAGE_SIZE_PX: int = 800

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
