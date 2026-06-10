from sqlalchemy.orm import Session

from app.models.mensaje_atencion import MensajeAtencion
from app.models.atencion_cliente import AtencionCliente
from app.schemas.mensaje_atencion import MensajeAtencionCreate


def create_mensaje(db: Session, data: MensajeAtencionCreate) -> MensajeAtencion:
    nuevo = MensajeAtencion(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def get_mensajes_por_atencion(db: Session, id_atencion: int):
    return (
        db.query(MensajeAtencion)
        .filter(MensajeAtencion.id_atencion == id_atencion, MensajeAtencion.habilitado == 1)
        .order_by(MensajeAtencion.fecha.asc())
        .all()
    )


def get_atencion_for_chat(db: Session, id_atencion: int) -> AtencionCliente | None:
    return (
        db.query(AtencionCliente)
        .filter(AtencionCliente.id_atencion == id_atencion, AtencionCliente.habilitado == 1)
        .first()
    )


def delete_mensaje(db: Session, id_mensaje: int) -> None:
    mensaje = db.query(MensajeAtencion).filter(MensajeAtencion.id_mensaje == id_mensaje).first()
    if mensaje:
        mensaje.habilitado = 0  # type: ignore[assignment]
        db.commit()


def update_mensaje(db: Session, id_mensaje: int, nuevo_texto: str):
    mensaje = db.query(MensajeAtencion).filter(MensajeAtencion.id_mensaje == id_mensaje).first()
    if mensaje:
        mensaje.mensaje = nuevo_texto
        db.commit()
        db.refresh(mensaje)
    return mensaje

