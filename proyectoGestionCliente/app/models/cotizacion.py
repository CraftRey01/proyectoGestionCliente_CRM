from app.db import Base
from sqlalchemy import Column, Integer, String, Date, Numeric, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship


class Cotizacion(Base):
    __tablename__ = "cotizacion"

    id_cotizacion = Column(Integer, primary_key=True, index=True)
    fecha_cotizacion = Column(Date)
    monto_estimado = Column(Numeric(10, 2))
    estado = Column(String)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))
    habilitado = Column(SmallInteger, default=1)

    cliente = relationship("Cliente", back_populates="cotizaciones")
    venta = relationship("Venta", back_populates="cotizacion", uselist=False)
