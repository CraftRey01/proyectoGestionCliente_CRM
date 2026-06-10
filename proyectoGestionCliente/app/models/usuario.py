from app.db import Base
from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(60), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    rol = Column(String(30), nullable=False)
    estado = Column(String(20), default="activo")
    habilitado = Column(SmallInteger, default=1)

    oportunidades = relationship("Oportunidad", back_populates="usuario")
    ventas = relationship("Venta", back_populates="usuario")
    atenciones = relationship("AtencionCliente", back_populates="usuario")
    notificaciones = relationship("Notificacion", back_populates="usuario")
