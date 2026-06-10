from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FacturaBase(BaseModel):
    id_factura: Optional[int] = None
    numero_factura: Optional[str] = None
    fecha_emision: Optional[datetime] = None
    estado: Optional[str] = None
    total: Optional[float] = None
    id_venta: Optional[int] = None
    habilitado: Optional[int] = 1


class FacturaCreate(FacturaBase):
    id_factura: int


class Factura(FacturaBase):
    id_factura: int

    class Config:
        from_attributes = True
