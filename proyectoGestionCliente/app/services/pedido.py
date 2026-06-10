import random
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.models.venta import Venta
from app.schemas.pedido import PedidoCreate


def create_pedido(db: Session, data: PedidoCreate):

    nuevo = Pedido(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


def get_pedidos(db: Session):
    return (
        db.query(Pedido)
        .order_by(Pedido.habilitado.desc(), Pedido.id_pedido.asc())
        .all()
    )


def get_pedido(db: Session, pedido_id: int):

    return (
        db.query(Pedido)
        .filter(Pedido.id_pedido == pedido_id, Pedido.habilitado == 1)
        .first()
    )


def update_pedido(db: Session, pedido_id: int, data: PedidoCreate):

    pedido = (
        db.query(Pedido)
        .filter(Pedido.id_pedido == pedido_id, Pedido.habilitado == 1)
        .first()
    )

    if not pedido:
        return None

    for key, value in data.model_dump().items():
        setattr(pedido, key, value)

    db.commit()
    db.refresh(pedido)

    return pedido


def delete_pedido(db: Session, pedido_id: int):

    pedido = db.query(Pedido).filter(Pedido.id_pedido == pedido_id).first()

    if not pedido:
        return None

    pedido.habilitado = 0

    db.commit()
    db.refresh(pedido)

    return pedido


def restore_pedido(db: Session, pedido_id: int):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == pedido_id).first()

    if not pedido:
        return None

    pedido.habilitado = 1

    db.commit()
    db.refresh(pedido)

    return pedido


def automate_next_pedido(db: Session):
    max_id = db.query(func.coalesce(func.max(Pedido.id_pedido), 0)).scalar() or 0
    nuevo_id = max_id + 1

    venta = (
        db.query(Venta)
        .filter(Venta.habilitado == 1, Venta.pedido == None)
        .order_by(Venta.id_venta.asc())
        .first()
    )

    if not venta:
        return None

    estados = ["confirmada", "pendiente", "cancelada"]
    estado = random.choice(estados)

    nuevo = Pedido(
        id_pedido=nuevo_id,
        fecha_pedido=datetime.now(),
        estado=estado,
        id_venta=venta.id_venta,
        habilitado=1,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo_id
