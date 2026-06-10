from app.db import Base
from sqlalchemy import Column, Integer, String, Numeric, Text, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship


class Oportunidad(Base):
    __tablename__ = "oportunidad"

    id_oportunidad = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text)
    monto_estimado = Column(Numeric(10, 2))
    estado = Column(String)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    habilitado = Column(SmallInteger, default=1)

    cliente = relationship("Cliente", back_populates="oportunidades")
    usuario = relationship("Usuario", back_populates="oportunidades")
