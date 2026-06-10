from app.db import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    SmallInteger,
    ForeignKey,
)
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship


class Venta(Base):
    __tablename__ = "venta"

    id_venta = Column(Integer, primary_key=True, index=True)
    fecha_venta = Column(DateTime, server_default=func.now())
    estado_venta = Column(String)
    monto_total = Column(Numeric(10, 2))
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    id_cotizacion = Column(Integer, ForeignKey("cotizacion.id_cotizacion"), unique=True)
    habilitado = Column(SmallInteger, default=1)

    cliente = relationship("Cliente", back_populates="ventas")
    usuario = relationship("Usuario", back_populates="ventas")
    cotizacion = relationship("Cotizacion", back_populates="venta")
    pedido = relationship("Pedido", back_populates="venta", uselist=False)
    factura = relationship("Factura", back_populates="venta", uselist=False)
    reportes = relationship("ReporteAnalisis", back_populates="venta")
