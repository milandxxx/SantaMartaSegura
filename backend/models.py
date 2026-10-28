from sqlalchemy import Column, Integer, String, Text, Float
from database import Base

class Lugar(Base):
    __tablename__ = "lugares"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, index=True)
    categoria = Column(String(50), default="playa")
    imagen = Column(Text, nullable=True, default="")
    precio = Column(Integer, default=0)
    seguridad = Column(String(20), default="verde")
    detalle = Column(Text, nullable=True, default="")

class Emergencia(Base):
    __tablename__ = "emergencias"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(50), nullable=False)