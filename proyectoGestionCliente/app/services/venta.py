from datetime import datetime
import random

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.venta import Venta
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.models.cotizacion import Cotizacion
from app.schemas.venta import VentaCreate


def create_venta(db: Session, data: VentaCreate):

    nueva = Venta(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def get_ventas(db: Session):
    return db.query(Venta).order_by(Venta.habilitado.desc(), Venta.id_venta.asc()).all()


def get_venta(db: Session, venta_id: int):

    return (
        db.query(Venta)
        .filter(Venta.id_venta == venta_id, Venta.habilitado == 1)
        .first()
    )


def update_venta(db: Session, venta_id: int, data: VentaCreate):

    venta = (
        db.query(Venta)
        .filter(Venta.id_venta == venta_id, Venta.habilitado == 1)
        .first()
    )

    if not venta:
        return None

    for key, value in data.model_dump().items():
        setattr(venta, key, value)

    db.commit()
    db.refresh(venta)

    return venta


def delete_venta(db: Session, venta_id: int):

    venta = db.query(Venta).filter(Venta.id_venta == venta_id).first()

    if not venta:
        return None

    venta.habilitado = 0

    db.commit()
    db.refresh(venta)

    return venta


def get_ventas_eliminadas(db: Session):
    return db.query(Venta).filter(Venta.habilitado == 0).order_by(Venta.id_venta).all()


def restore_venta(db: Session, venta_id: int):
    venta = db.query(Venta).filter(Venta.id_venta == venta_id).first()

    if not venta:
        return None

    venta.habilitado = 1

    db.commit()
    db.refresh(venta)

    return venta


def automate_next_venta(db: Session):
    max_id = db.query(func.coalesce(func.max(Venta.id_venta), 0)).scalar() or 0
    nuevo_id = max_id + 1

    cliente = (
        db.query(Cliente)
        .filter(Cliente.habilitado == 1)
        .order_by(Cliente.id_cliente.asc())
        .first()
    )
    usuario = (
        db.query(Usuario)
        .filter(Usuario.habilitado == 1)
        .order_by(Usuario.id_usuario.asc())
        .first()
    )
    cotizacion = (
        db.query(Cotizacion)
        .filter(Cotizacion.habilitado == 1, Cotizacion.venta == None)
        .order_by(Cotizacion.id_cotizacion.asc())
        .first()
    )

    if not cliente or not usuario:
        return None

    estados = ["facturado", "pendiente", "cancelada"]
    estado = random.choice(estados)
    monto = round(random.uniform(500.0, 15000.0), 2)
    id_cotizacion = cotizacion.id_cotizacion if cotizacion else None

    nueva = Venta(
        id_venta=nuevo_id,
        fecha_venta=datetime.now(),
        estado_venta=estado,
        monto_total=monto,
        id_cliente=cliente.id_cliente,
        id_usuario=usuario.id_usuario,
        id_cotizacion=id_cotizacion,
        habilitado=1,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nuevo_id
