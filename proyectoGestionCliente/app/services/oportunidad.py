import random

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.oportunidad import Oportunidad
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.schemas.oportunidad import OportunidadCreate


def create_oportunidad(db: Session, data: OportunidadCreate):

    nueva = Oportunidad(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def get_oportunidades(db: Session):
    return (
        db.query(Oportunidad)
        .order_by(Oportunidad.habilitado.desc(), Oportunidad.id_oportunidad.asc())
        .all()
    )


def get_oportunidad(db: Session, oportunidad_id: int):

    return (
        db.query(Oportunidad)
        .filter(
            Oportunidad.id_oportunidad == oportunidad_id, Oportunidad.habilitado == 1
        )
        .first()
    )


def update_oportunidad(db: Session, oportunidad_id: int, data: OportunidadCreate):

    oportunidad = (
        db.query(Oportunidad)
        .filter(
            Oportunidad.id_oportunidad == oportunidad_id, Oportunidad.habilitado == 1
        )
        .first()
    )

    if not oportunidad:
        return None

    for key, value in data.model_dump().items():
        setattr(oportunidad, key, value)

    db.commit()
    db.refresh(oportunidad)

    return oportunidad


def delete_oportunidad(db: Session, oportunidad_id: int):

    oportunidad = (
        db.query(Oportunidad)
        .filter(Oportunidad.id_oportunidad == oportunidad_id)
        .first()
    )

    if not oportunidad:
        return None

    oportunidad.habilitado = 0

    db.commit()
    db.refresh(oportunidad)

    return oportunidad


def restore_oportunidad(db: Session, oportunidad_id: int):
    oportunidad = (
        db.query(Oportunidad)
        .filter(Oportunidad.id_oportunidad == oportunidad_id)
        .first()
    )

    if not oportunidad:
        return None

    oportunidad.habilitado = 1

    db.commit()
    db.refresh(oportunidad)

    return oportunidad


def _generate_random_descripcion(index: int):
    productos = [
        "laptops",
        "impresoras",
        "routers",
        "monitores",
        "servidores",
        "switches",
        "PCs",
        "tablets",
        "accesorios",
        "software",
        "cables",
        "sistemas",
        "displays",
        "sensores",
        "teclados",
        "móviles",
        "impresoras 3D",
        "cámaras",
    ]
    acciones = [
        "Venta de",
        "Oferta de",
        "Propuesta de",
        "Cotización de",
        "Solicitud de",
        "Promoción de",
    ]
    rnd = random.Random(index + 2026)
    descripcion = f"{rnd.choice(acciones)} {rnd.choice(productos)}"
    return descripcion


def automate_next_oportunidad(db: Session):
    max_id = db.query(func.coalesce(func.max(Oportunidad.id_oportunidad), 0)).scalar() or 0
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

    if not cliente or not usuario:
        return None

    estados = ["abierta", "en proceso", "cerrada", "perdida"]
    estado = random.choice(estados)
    monto = round(random.uniform(1000.0, 20000.0), 2)
    descripcion = _generate_random_descripcion(nuevo_id)

    existente = (
        db.query(Oportunidad)
        .filter(Oportunidad.descripcion == descripcion)
        .first()
    )
    if existente:
        descripcion = f"{descripcion} #{nuevo_id}"

    nueva = Oportunidad(
        id_oportunidad=nuevo_id,
        descripcion=descripcion,
        monto_estimado=monto,
        estado=estado,
        id_cliente=cliente.id_cliente,
        id_usuario=usuario.id_usuario,
        habilitado=1,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nuevo_id
