from pydantic import BaseModel
from typing import Optional
from datetime import date

class CampaniaBase(BaseModel):
    id_campania: Optional[int] = None
    nombre_campania: Optional[str] = None
    tipo_campania: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_finalizacion: Optional[date] = None
    resultado_obtenido: Optional[str] = None
    habilitado: Optional[int] = 1    

class CampaniaCreate(CampaniaBase):
    id_campania: int

class Campania(CampaniaBase):
    id_campania: int

    class Config:
        from_attributes = True
