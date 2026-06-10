from pydantic import BaseModel
from typing import Optional
from datetime import date


class CotizacionBase(BaseModel):
    id_cotizacion: Optional[int] = None
    fecha_cotizacion: Optional[date] = None
    monto_estimado: Optional[float] = None
    estado: Optional[str] = None
    id_cliente: Optional[int] = None
    habilitado: Optional[int] = 1


class CotizacionCreate(CotizacionBase):
    id_cotizacion: int


class Cotizacion(CotizacionBase):
    id_cotizacion: int

    class Config:
        from_attributes = True
