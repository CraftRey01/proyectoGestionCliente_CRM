from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


class VentaBase(BaseModel):
    id_venta: Optional[int] = None
    fecha_venta: Optional[datetime] = None
    estado_venta: Optional[str] = None
    monto_total: Optional[Decimal] = None
    id_cliente: Optional[int] = None
    id_usuario: Optional[int] = None
    id_cotizacion: Optional[int] = None
    habilitado: Optional[int] = 1


class VentaCreate(VentaBase):
    id_venta: int


class Venta(VentaBase):
    id_venta: int

    class Config:
        from_attributes = True
