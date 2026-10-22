import hashlib
import hmac
import time
import os
from typing import Optional
from fastapi import HTTPException, Depends, Header
from config import get_settings

settings = get_settings()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed)

def create_token() -> str:
    timestamp = str(int(time.time()) + settings.ADMIN_TOKEN_EXPIRE_HOURS * 3600)
    message = f"{timestamp}:{settings.ADMIN_TOKEN_SECRET}"
    signature = hmac.new(
        settings.ADMIN_TOKEN_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{timestamp}.{signature}"

def verify_token(token: str) -> bool:
    try:
        timestamp_str, signature = token.split(".")
        timestamp = int(timestamp_str)
        if timestamp < time.time():
            return False
        message = f"{timestamp_str}:{settings.ADMIN_TOKEN_SECRET}"
        expected = hmac.new(
            settings.ADMIN_TOKEN_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)
    except Exception:
        return False

def get_admin_password_hash() -> str:
    return hash_password(settings.ADMIN_PASSWORD)

async def get_current_admin(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autenticado")
    token = authorization.split(" ")[1]
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return "admin"