from functools import lru_cache
from typing import List

class Settings:
    # Base de datos PostgreSQL
    # Formato: postgresql://usuario:contraseña@host:puerto/nombre_bd
    # Para desarrollo local con PostgreSQL:
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/santamarta"
    
    # Admin
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_TOKEN_SECRET: str = "super-secret-key-change-in-production"
    ADMIN_TOKEN_EXPIRE_HOURS: int = 24
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:8080", "http://localhost:8081", "*"]
    
    # App
    APP_NAME: str = "Santa Marta Seguro API"
    DEBUG: bool = True

@lru_cache()
def get_settings():
    return Settings()