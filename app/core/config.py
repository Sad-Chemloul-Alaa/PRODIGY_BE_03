from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    SECRET_KEY: str | None = None   # Optional now

    CONNECT_ARGS: dict = {"check_same_thread": False}

    class Config:
        env_file = ".env"

settings = Settings()
