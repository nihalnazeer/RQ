from pydantic import BaseSettings


class Settings(BaseSettings):
    # Default database is SQLite unless overridden in .env
    DATABASE_URL: str = "sqlite:///./inventory.db"
    DEBUG: bool = True

    class Config:
        env_file = ".env"     # loads environment variables if present
        env_file_encoding = "utf-8"


def get_settings():
    return Settings()
