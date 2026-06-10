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


class Factura(Base):
    __tablename__ = "factura"

    id_factura = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String, unique=True)
    fecha_emision = Column(DateTime, server_default=func.now())
    estado = Column(String)
    total = Column(Numeric(10, 2))
    id_venta = Column(Integer, ForeignKey("venta.id_venta"), unique=True)
    habilitado = Column(SmallInteger, default=1)

    venta = relationship("Venta", back_populates="factura")
