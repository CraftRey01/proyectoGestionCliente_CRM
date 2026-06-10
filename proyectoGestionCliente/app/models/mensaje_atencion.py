# app/models/mensaje_atencion.py

from app.db import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import SmallInteger
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class MensajeAtencion(Base):

    __tablename__ = "mensaje_atencion"

    id_mensaje = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_atencion = Column(
        Integer,
        ForeignKey("atencion_cliente.id_atencion")
    )

    remitente = Column(String(20))

    mensaje = Column(Text)

    fecha = Column(
        DateTime,
        server_default=func.now()
    )

    habilitado = Column(
        SmallInteger,
        default=1
    )

    atencion = relationship(
        "AtencionCliente",
        back_populates="mensajes"
    )