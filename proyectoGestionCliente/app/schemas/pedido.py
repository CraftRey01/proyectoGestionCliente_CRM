from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PedidoBase(BaseModel):
    id_pedido: Optional[int] = None
    fecha_pedido: Optional[datetime] = None
    estado: Optional[str] = None
    id_venta: Optional[int] = None
    habilitado: Optional[int] = 1


class PedidoCreate(PedidoBase):
    id_pedido: int


class Pedido(PedidoBase):
    id_pedido: int

    class Config:
        from_attributes = True
