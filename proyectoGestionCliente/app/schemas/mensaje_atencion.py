from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MensajeAtencionBase(BaseModel):
    id_atencion: Optional[int] = None
    remitente: Optional[str] = None
    mensaje: Optional[str] = None
    fecha: Optional[datetime] = None
    habilitado: Optional[int] = 1


class MensajeAtencionCreate(MensajeAtencionBase):
    id_atencion: int
    remitente: str
    mensaje: str


class MensajeAtencion(MensajeAtencionBase):
    id_mensaje: int

    class Config:
        from_attributes = True

