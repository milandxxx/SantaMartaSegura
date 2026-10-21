from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Alerta
from schemas import AlertaResponse, AlertaCreate, StandardResponse

router = APIRouter(prefix="/api/alertas", tags=["alertas"])

@router.get("", response_model=StandardResponse)
def get_all_alertas(db: Session = Depends(get_db)):
    alertas = db.query(Alerta).order_by(Alerta.id.desc()).all()
    return {"status": True, "respuesta": [AlertaResponse.model_validate(a) for a in alertas]}

@router.post("", response_model=StandardResponse)
def create_alerta(alerta: AlertaCreate, db: Session = Depends(get_db)):
    db_alerta = Alerta(**alerta.model_dump())
    db.add(db_alerta)
    db.commit()
    db.refresh(db_alerta)
    return {"status": True, "respuesta": AlertaResponse.model_validate(db_alerta)}

@router.delete("/{alerta_id}", response_model=StandardResponse)
def delete_alerta(alerta_id: int, db: Session = Depends(get_db)):
    db_alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    if not db_alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    db.delete(db_alerta)
    db.commit()
    return {"status": True, "respuesta": {"message": "Alerta eliminada correctamente"}}