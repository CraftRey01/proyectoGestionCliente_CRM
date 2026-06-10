from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClienteBase(BaseModel):
    id_cliente: Optional[int] = None
    foto_cliente: Optional[str] = None
    nombre_cliente: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    fecha_registro: Optional[date] = None
    segmento_cliente: Optional[str] = "Nuevo"
    habilitado: Optional[int] = 1    

class ClienteCreate(ClienteBase):
    id_cliente: int

class Cliente(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True
