from app.db import Base
from sqlalchemy import Column, Integer, String, Date, SmallInteger
from sqlalchemy.orm import relationship


class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    foto_cliente = Column(String)
    nombre_cliente = Column(String)
    telefono = Column(String)
    correo = Column(String)
    fecha_registro = Column(Date)
    segmento_cliente = Column(String, default="Nuevo")
    habilitado = Column(SmallInteger, default=1)

    oportunidades = relationship("Oportunidad", back_populates="cliente")
    cotizaciones = relationship("Cotizacion", back_populates="cliente")
    ventas = relationship("Venta", back_populates="cliente")
    atenciones = relationship("AtencionCliente", back_populates="cliente")
    campanias = relationship("ClienteCampania", back_populates="cliente")
