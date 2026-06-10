from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship


class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True, index=True)
    fecha_pedido = Column(DateTime, server_default=func.now())
    estado = Column(String)
    id_venta = Column(Integer, ForeignKey("venta.id_venta"), unique=True)
    habilitado = Column(SmallInteger, default=1)

    venta = relationship("Venta", back_populates="pedido")
