from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DEFAULT_ADMIN_EMAIL: str
    DEFAULT_ADMIN_PASSWORD: str

    RATE_LIMIT_DEFAULT: int = 60
    RATE_LIMIT_AUTH: int = 5
    RATE_LIMIT_STREAM: int = 20
    
    model_config = ConfigDict(env_file=".env")


settings = Settings() 