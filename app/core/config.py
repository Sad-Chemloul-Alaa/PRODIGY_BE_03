from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    SECRET_KEY: str | None = None  
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    CONNECT_ARGS: dict = {"check_same_thread": False}

    class Config:
        env_file = ".env"

settings = Settings()
