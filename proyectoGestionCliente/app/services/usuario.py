from app import models
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from typing import Union


def create_usuario(db: Session, data: UsuarioCreate):

    nuevo = Usuario(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


def get_usuarios(db):
    return (
        db.query(models.Usuario)
        .order_by(models.Usuario.habilitado.desc(), models.Usuario.id_usuario.asc())
        .all()
    )


def get_usuario(db: Session, usuario_id: int):

    return (
        db.query(Usuario)
        .filter(Usuario.id_usuario == usuario_id, Usuario.habilitado == 1)
        .first()
    )


def update_usuario(
    db: Session, usuario_id: int, data: Union[UsuarioCreate, UsuarioUpdate]
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id_usuario == usuario_id, Usuario.habilitado == 1)
        .first()
    )

    if not usuario:
        return None

    # Permitir cambio de ID si es diferente
    if data.id_usuario is not None and data.id_usuario != usuario_id:
        usuario.id_usuario = data.id_usuario

    usuario.nombre_usuario = data.nombre_usuario
    usuario.contrasena = data.contrasena
    usuario.rol = data.rol
    usuario.estado = data.estado
    usuario.habilitado = data.habilitado

    db.commit()
    db.refresh(usuario)

    return usuario


def delete_usuario(db: Session, usuario_id: int):

    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    if not usuario:
        return None

    usuario.habilitado = 0

    db.commit()
    db.refresh(usuario)

    return usuario


def restore_usuario(db: Session, usuario_id: int):

    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    if not usuario:
        return None

    usuario.habilitado = 1

    db.commit()
    db.refresh(usuario)

    return usuario
