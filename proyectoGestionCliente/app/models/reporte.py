from app.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship


class Reporte(Base):
    __tablename__ = "reporte"

    id_reporte = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo_reporte = Column(String)
    periodo = Column(String)
    fecha_generacion = Column(DateTime, server_default=func.now())
    formato = Column(String)
    resumen = Column(Text)
    tipo_grafico = Column(String)
    habilitado = Column(SmallInteger, default=1)

    analisis = relationship("ReporteAnalisis", back_populates="reporte")
