# core/config.py
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator
import secrets
from functools import lru_cache


class Settings(BaseSettings):
    # Basic API Settings
    PROJECT_NAME: str = "Assets Management API"
    PROJECT_DESCRIPTION: str = "API for Assets Management"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"

    # Server Settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False

    # Security Settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # Database Settings
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = []

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

    # Redis Settings
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None
    REDIS_PASSWORD: Optional[str] = None

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Rate Limiting
    RATE_LIMIT_MAX_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # File Upload
    MAX_UPLOAD_SIZE: int = 5_242_880  # 5MB in bytes
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    # Cache Settings
    CACHE_TTL: int = 3600  # 1 hour in seconds
    
    # Root Account
    ROOT_ACCOUNT_USERNAME: str
    ROOT_ACCOUNT_PASSWORD: str
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        

# Create a cached instance of settings
@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Export settings instance
settings = get_settings()
