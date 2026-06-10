from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReporteBase(BaseModel):
    id_reporte: Optional[int] = None
    tipo_reporte: Optional[str] = None
    periodo: Optional[str] = None
    fecha_generacion: Optional[datetime] = None
    formato: Optional[str] = None
    resumen: Optional[str] = None
    tipo_grafico: Optional[str] = None
    habilitado: Optional[int] = 1

class ReporteCreate(ReporteBase):
    pass

class Reporte(ReporteBase):
    id_reporte: int

    class Config:
        from_attributes = True
