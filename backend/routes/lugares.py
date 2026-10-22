from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Lugar
from schemas import LugarResponse, LugarCreate, LugarUpdate, StandardResponse

router = APIRouter(prefix="/api/lugares", tags=["lugares"])

@router.get("", response_model=StandardResponse)
def get_all_lugares(db: Session = Depends(get_db)):
    lugares = db.query(Lugar).order_by(Lugar.id).all()
    return {"status": True, "respuesta": [LugarResponse.model_validate(l) for l in lugares]}

@router.get("/{lugar_id}", response_model=StandardResponse)
def get_lugar(lugar_id: int, db: Session = Depends(get_db)):
    lugar = db.query(Lugar).filter(Lugar.id == lugar_id).first()
    if not lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    return {"status": True, "respuesta": LugarResponse.model_validate(lugar)}

@router.post("", response_model=StandardResponse)
def create_lugar(lugar: LugarCreate, db: Session = Depends(get_db)):
    db_lugar = Lugar(**lugar.model_dump())
    db.add(db_lugar)
    db.commit()
    db.refresh(db_lugar)
    return {"status": True, "respuesta": LugarResponse.model_validate(db_lugar)}

@router.put("/{lugar_id}", response_model=StandardResponse)
def update_lugar(lugar_id: int, lugar_update: LugarUpdate, db: Session = Depends(get_db)):
    db_lugar = db.query(Lugar).filter(Lugar.id == lugar_id).first()
    if not db_lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    
    update_data = lugar_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_lugar, field, value)
    
    db.commit()
    db.refresh(db_lugar)
    return {"status": True, "respuesta": LugarResponse.model_validate(db_lugar)}

@router.delete("/{lugar_id}", response_model=StandardResponse)
def delete_lugar(lugar_id: int, db: Session = Depends(get_db)):
    db_lugar = db.query(Lugar).filter(Lugar.id == lugar_id).first()
    if not db_lugar:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")
    
    db.delete(db_lugar)
    db.commit()
    return {"status": True, "respuesta": {"message": "Lugar eliminado correctamente"}}