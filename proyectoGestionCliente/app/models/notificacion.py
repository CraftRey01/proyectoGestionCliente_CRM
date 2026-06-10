from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger, ForeignKey
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship


class Notificacion(Base):
    __tablename__ = "notificacion"

    id_notificacion = Column(Integer, primary_key=True, index=True)
    fecha_envio = Column(DateTime, server_default=func.now())
    tipo_notificacion = Column(String)
    mensaje = Column(Text)
    estado = Column(String)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    habilitado = Column(SmallInteger, default=1)

    usuario = relationship("Usuario", back_populates="notificaciones")
