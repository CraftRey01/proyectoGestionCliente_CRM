from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate


def create_notificacion(db: Session, data: NotificacionCreate):

    nueva = Notificacion(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def get_notificaciones(db: Session):

    return (
        db.query(Notificacion)
        .order_by(Notificacion.habilitado.desc(), Notificacion.id_notificacion.asc())
        .all()
    )


def get_notificacion(db: Session, notificacion_id: int):

    return (
        db.query(Notificacion)
        .filter(
            Notificacion.id_notificacion == notificacion_id,
            Notificacion.habilitado == 1,
        )
        .first()
    )


def update_notificacion(db: Session, notificacion_id: int, data: NotificacionCreate):

    notificacion = (
        db.query(Notificacion)
        .filter(
            Notificacion.id_notificacion == notificacion_id,
            Notificacion.habilitado == 1,
        )
        .first()
    )

    if not notificacion:
        return None

    for key, value in data.model_dump().items():
        setattr(notificacion, key, value)

    db.commit()
    db.refresh(notificacion)

    return notificacion


def delete_notificacion(db: Session, notificacion_id: int):

    notificacion = (
        db.query(Notificacion)
        .filter(Notificacion.id_notificacion == notificacion_id)
        .first()
    )

    if not notificacion:
        return None

    notificacion.habilitado = 0

    db.commit()
    db.refresh(notificacion)

    return notificacion


def get_notificaciones_eliminadas(db: Session):

    return db.query(Notificacion).filter(Notificacion.habilitado == 0).all()


def restore_notificacion(db: Session, notificacion_id: int):

    notificacion = (
        db.query(Notificacion)
        .filter(Notificacion.id_notificacion == notificacion_id)
        .first()
    )

    if not notificacion:
        return None

    notificacion.habilitado = 1

    db.commit()
    db.refresh(notificacion)

    return notificacion


def get_notificaciones_by_estado(db: Session, estado: str):

    return (
        db.query(Notificacion)
        .filter(Notificacion.habilitado == 1, Notificacion.estado == estado)
        .all()
    )


def count_notificaciones_enviadas(db: Session):

    return (
        db.query(func.count(Notificacion.id_notificacion))
        .filter(Notificacion.habilitado == 1, Notificacion.estado == "enviado")
        .scalar()
    )
