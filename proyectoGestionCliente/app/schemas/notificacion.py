from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionBase(BaseModel):
    id_notificacion: Optional[int] = None
    fecha_envio: Optional[datetime] = None
    tipo_notificacion: Optional[str] = None
    mensaje: Optional[str] = None
    estado: Optional[str] = None
    id_usuario: Optional[int] = None
    habilitado: Optional[int] = 1

class NotificacionCreate(NotificacionBase):
    id_notificacion: int

class Notificacion(NotificacionBase):
    id_notificacion: int

    class Config:
        from_attributes = True
