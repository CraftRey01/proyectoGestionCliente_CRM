from app.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class ReporteAnalisis(Base):
    __tablename__ = "reporte_analisis"

    id_reporte = Column(Integer, ForeignKey("reporte.id_reporte"), primary_key=True)
    id_venta = Column(Integer, ForeignKey("venta.id_venta"), primary_key=True, nullable=True)
    id_campania = Column(Integer, ForeignKey("campania.id_campania"), primary_key=True, nullable=True)

    reporte = relationship("Reporte", back_populates="analisis")
    venta = relationship("Venta", back_populates="reportes")
    campania = relationship("Campania", back_populates="reportes")
