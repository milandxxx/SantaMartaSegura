from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# Lugares
class LugarBase(BaseModel):
    nombre: str
    categoria: str = "playa"
    imagen: str = ""
    precio: int = 0
    seguridad: str = "verde"
    detalle: str = ""

class LugarCreate(LugarBase):
    pass

class LugarUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    imagen: Optional[str] = None
    precio: Optional[int] = None
    seguridad: Optional[str] = None
    detalle: Optional[str] = None

class LugarResponse(LugarBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Alertas
class AlertaBase(BaseModel):
    tipo: str
    titulo: str
    mensaje: str

class AlertaCreate(AlertaBase):
    pass

class AlertaResponse(AlertaBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Emergencias
class EmergenciaBase(BaseModel):
    nombre: str
    telefono: str

class EmergenciaCreate(EmergenciaBase):
    pass

class EmergenciaResponse(EmergenciaBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Auth
class AdminLogin(BaseModel):
    password: str

class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Respuesta estándar
class StandardResponse(BaseModel):
    status: bool
    respuesta: List | dict | None = None
    error: str | None = None