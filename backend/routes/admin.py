from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Lugar, Alerta, Emergencia
from schemas import AdminLogin, AdminToken, StandardResponse
from auth import verify_password, get_admin_password_hash, create_token, get_current_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/login", response_model=AdminToken)
def admin_login(login: AdminLogin):
    if not verify_password(login.password, get_admin_password_hash()):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    token = create_token()
    return {"access_token": token, "token_type": "bearer"}

@router.get("/stats", response_model=StandardResponse)
def admin_stats(admin: str = Depends(get_current_admin), db: Session = Depends(get_db)):
    stats = {
        "lugares_count": db.query(Lugar).count(),
        "alertas_count": db.query(Alerta).count(),
        "emergencias_count": db.query(Emergencia).count(),
    }
    return {"status": True, "respuesta": stats}

@router.get("/verify", response_model=StandardResponse)
def verify_admin(admin: str = Depends(get_current_admin)):
    return {"status": True, "respuesta": {"authenticated": True, "user": admin}}