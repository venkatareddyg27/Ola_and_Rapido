from dotenv import load_dotenv
 
load_dotenv()
 
from pydantic_settings import (

    BaseSettings,

    SettingsConfigDict

)
class Settings(BaseSettings):
 
    # =====================================================

    # APP

    # =====================================================
 
    APP_NAME: str
 
    APP_VERSION: str
 
    DEBUG: bool = True
 
 
    # =====================================================

    # DATABASE

    # =====================================================
 
    DATABASE_URL: str
 
 
    # =====================================================

    # JWT

    # =====================================================
 
    SECRET_KEY: str = "secret"
 
    ALGORITHM: str = "HS256"
 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
 
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
 
 
    # =====================================================

    # REDIS

    # =====================================================
 
    REDIS_URL: str = "redis://localhost:6379"
 
    REDIS_HOST: str = "localhost"
 
    REDIS_PORT: int = 6379
 
    REDIS_DB: int = 0
 
 
    # =====================================================

    # OTP

    # =====================================================
 
    OTP_EXPIRY_SECONDS: int = 600
 
    OTP_RATE_LIMIT: int = 3
 
    OTP_RATE_LIMIT_WINDOW: int = 3600

    # =====================================================

    # ENV FILE

    # =====================================================
 
    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore"

    )
 
 
settings = Settings()
 