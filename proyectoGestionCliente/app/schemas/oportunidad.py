from pydantic import BaseModel
from typing import Optional


class OportunidadBase(BaseModel):
    id_oportunidad: Optional[int] = None
    descripcion: Optional[str] = None
    monto_estimado: Optional[float] = None
    estado: Optional[str] = None
    id_cliente: Optional[int] = None
    id_usuario: Optional[int] = None
    habilitado: Optional[int] = 1

class OportunidadCreate(OportunidadBase):
    id_oportunidad: int

class Oportunidad(OportunidadBase):
    id_oportunidad: int

    class Config:
        from_attributes = True
