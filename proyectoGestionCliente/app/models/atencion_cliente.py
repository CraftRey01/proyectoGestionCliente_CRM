from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, Text
from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship


class AtencionCliente(Base):
    __tablename__ = "atencion_cliente"

    id_atencion = Column(Integer, primary_key=True, index=True)
    fecha_registro = Column(DateTime, server_default=func.now())
    tipo_solicitud = Column(String(50))
    descripcion = Column(Text)
    prioridad = Column(String(20))
    estado = Column(String(30))
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    habilitado = Column(SmallInteger, default=1)

    cliente = relationship("Cliente", back_populates="atenciones")
    usuario = relationship("Usuario", back_populates="atenciones")
    mensajes = relationship(
    "MensajeAtencion",
    back_populates="atencion",
    cascade="all, delete-orphan"
)