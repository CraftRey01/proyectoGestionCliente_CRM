from app.db import Base
from sqlalchemy import Column, Integer, String, Date, Text, SmallInteger
from sqlalchemy.orm import relationship


class Campania(Base):
    __tablename__ = "campania"

    id_campania = Column(Integer, primary_key=True, index=True)
    nombre_campania = Column(String)
    tipo_campania = Column(String)
    fecha_inicio = Column(Date)
    fecha_finalizacion = Column(Date)
    resultado_obtenido = Column(Text)
    habilitado = Column(SmallInteger, default=1)

    clientes = relationship("ClienteCampania", back_populates="campania")
    reportes = relationship("ReporteAnalisis", back_populates="campania")
