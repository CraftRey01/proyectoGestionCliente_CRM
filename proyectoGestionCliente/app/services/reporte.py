from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.reporte import Reporte
from app.models.venta import Venta
from app.models.campania import Campania

from app.schemas.reporte import ReporteCreate


def create_reporte(db: Session, data: ReporteCreate):

    valores = data.model_dump()
    if valores.get("id_reporte") in (None, 0):
        valores.pop("id_reporte", None)

    nuevo = Reporte(**valores)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# TODOS
def get_reportes(db: Session):
    return (
        db.query(Reporte)
        .order_by(Reporte.habilitado.desc(), Reporte.id_reporte.asc())
        .all()
    )


# ACTIVOS
def get_reportes_activos(db: Session):

    return (
        db.query(Reporte)
        .filter(Reporte.habilitado == 1)
        .order_by(Reporte.id_reporte.asc())
        .all()
    )


# ELIMINADOS
def get_reportes_eliminados(db: Session):

    return (
        db.query(Reporte)
        .filter(Reporte.habilitado == 0)
        .order_by(Reporte.id_reporte.asc())
        .all()
    )


def get_reporte(db: Session, reporte_id: int):

    return (
        db.query(Reporte)
        .filter(Reporte.id_reporte == reporte_id, Reporte.habilitado == 1)
        .first()
    )


def update_reporte(db: Session, reporte_id: int, data: ReporteCreate):

    reporte = (
        db.query(Reporte)
        .filter(Reporte.id_reporte == reporte_id, Reporte.habilitado == 1)
        .first()
    )

    if not reporte:
        return None

    for key, value in data.model_dump().items():
        setattr(reporte, key, value)

    db.commit()
    db.refresh(reporte)

    return reporte


# ELIMINAR
def delete_reporte(db: Session, reporte_id: int):

    reporte = db.query(Reporte).filter(Reporte.id_reporte == reporte_id).first()

    if not reporte:
        return None

    reporte.habilitado = 0

    db.commit()
    db.refresh(reporte)

    return reporte


# RESTAURAR
def restore_reporte(db: Session, reporte_id: int):

    reporte = db.query(Reporte).filter(Reporte.id_reporte == reporte_id).first()

    if not reporte:
        return None

    reporte.habilitado = 1

    db.commit()
    db.refresh(reporte)

    return reporte


# DASHBOARD


def total_ventas(db: Session):

    return db.query(func.count(Venta.id_venta)).scalar()


def total_campanias(db: Session):

    return db.query(func.count(Campania.id_campania)).scalar()


def suma_ventas(db: Session):

    return db.query(func.sum(Venta.monto_total)).scalar()


def ventas_por_estado(db: Session):

    return (
        db.query(Venta.estado_venta, func.count(Venta.id_venta))
        .group_by(Venta.estado_venta)
        .all()
    )
