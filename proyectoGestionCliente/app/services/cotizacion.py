from sqlalchemy.orm import Session
from app.models.cotizacion import Cotizacion
from app.schemas.cotizacion import CotizacionCreate


def create_cotizacion(db: Session, data: CotizacionCreate):

    nueva = Cotizacion(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def get_cotizaciones(db: Session):

    return (
        db.query(Cotizacion)
        .order_by(Cotizacion.habilitado.desc(), Cotizacion.id_cotizacion.asc())
        .all()
    )


def get_cotizacion(db: Session, cotizacion_id: int):

    return (
        db.query(Cotizacion)
        .filter(Cotizacion.id_cotizacion == cotizacion_id, Cotizacion.habilitado == 1)
        .first()
    )


def update_cotizacion(db: Session, cotizacion_id: int, data: CotizacionCreate):

    cotizacion = (
        db.query(Cotizacion)
        .filter(Cotizacion.id_cotizacion == cotizacion_id, Cotizacion.habilitado == 1)
        .first()
    )

    if not cotizacion:
        return None

    for key, value in data.model_dump().items():
        setattr(cotizacion, key, value)

    db.commit()
    db.refresh(cotizacion)

    return cotizacion


def delete_cotizacion(db: Session, cotizacion_id: int):

    cotizacion = (
        db.query(Cotizacion).filter(Cotizacion.id_cotizacion == cotizacion_id).first()
    )

    if not cotizacion:
        return None

    cotizacion.habilitado = 0

    db.commit()
    db.refresh(cotizacion)

    return cotizacion


def get_cotizaciones_eliminadas(db: Session):
    return (
        db.query(Cotizacion)
        .filter(Cotizacion.habilitado == 0)
        .order_by(Cotizacion.id_cotizacion)
        .all()
    )


def restore_cotizacion(db: Session, cotizacion_id: int):
    cotizacion = (
        db.query(Cotizacion).filter(Cotizacion.id_cotizacion == cotizacion_id).first()
    )

    if not cotizacion:
        return None

    cotizacion.habilitado = 1

    db.commit()
    db.refresh(cotizacion)

    return cotizacion
