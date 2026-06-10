from pydantic import BaseModel
from typing import Optional


class UsuarioCreate(BaseModel):
    id_usuario: Optional[int] = None
    nombre_usuario: Optional[str] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = "activo"
    habilitado: Optional[int] = 1


class UsuarioUpdate(BaseModel):
    id_usuario: Optional[int] = None
    nombre_usuario: Optional[str] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = "activo"
    habilitado: Optional[int] = 1


class UsuarioBase(BaseModel):
    id_usuario: Optional[int] = None
    nombre_usuario: Optional[str] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = "activo"
    habilitado: Optional[int] = 1


class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True
