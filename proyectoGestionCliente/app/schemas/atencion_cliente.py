from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AtencionClienteBase(BaseModel):
    id_atencion: Optional[int] = None
    fecha_registro: Optional[datetime] = None
    tipo_solicitud: Optional[str] = None
    descripcion: Optional[str] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None
    id_cliente: Optional[int] = None
    id_usuario: Optional[int] = None
    habilitado: Optional[int] = 1

class AtencionClienteCreate(AtencionClienteBase):
    id_atencion: int

class AtencionCliente(AtencionClienteBase):
    id_atencion: int

    class Config:
        from_attributes = True
