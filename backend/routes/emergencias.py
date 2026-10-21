from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Emergencia
from schemas import EmergenciaResponse, EmergenciaCreate, StandardResponse

router = APIRouter(prefix="/api/emergencias", tags=["emergencias"])

@router.get("", response_model=StandardResponse)
def get_all_emergencias(db: Session = Depends(get_db)):
    emergencias = db.query(Emergencia).order_by(Emergencia.id).all()
    return {"status": True, "respuesta": [EmergenciaResponse.model_validate(e) for e in emergencias]}

@router.post("", response_model=StandardResponse)
def create_emergencia(emergencia: EmergenciaCreate, db: Session = Depends(get_db)):
    db_emergencia = Emergencia(**emergencia.model_dump())
    db.add(db_emergencia)
    db.commit()
    db.refresh(db_emergencia)
    return {"status": True, "respuesta": EmergenciaResponse.model_validate(db_emergencia)}

@router.put("/{emergencia_id}", response_model=StandardResponse)
def update_emergencia(emergencia_id: int, emergencia: EmergenciaCreate, db: Session = Depends(get_db)):
    db_emergencia = db.query(Emergencia).filter(Emergencia.id == emergencia_id).first()
    if not db_emergencia:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")
    
    db_emergencia.nombre = emergencia.nombre
    db_emergencia.telefono = emergencia.telefono
    db.commit()
    db.refresh(db_emergencia)
    return {"status": True, "respuesta": EmergenciaResponse.model_validate(db_emergencia)}

@router.delete("/{emergencia_id}", response_model=StandardResponse)
def delete_emergencia(emergencia_id: int, db: Session = Depends(get_db)):
    db_emergencia = db.query(Emergencia).filter(Emergencia.id == emergencia_id).first()
    if not db_emergencia:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")
    db.delete(db_emergencia)
    db.commit()
    return {"status": True, "respuesta": {"message": "Emergencia eliminada correctamente"}}