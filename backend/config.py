import os
from functools import lru_cache
from typing import List

class Settings:
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./santamarta.db")
    
    # Admin
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    ADMIN_TOKEN_SECRET: str = os.getenv("ADMIN_TOKEN_SECRET", "super-secret-key-change-in-production")
    ADMIN_TOKEN_EXPIRE_HOURS: int = 24
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:8080", "http://localhost:8081", "*"]
    
    # App
    APP_NAME: str = "Santa Marta Seguro API"
    DEBUG: bool = True

@lru_cache()
def get_settings():
    return Settings()