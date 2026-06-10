from sqlalchemy.orm import Session
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate


def create_factura(db: Session, data: FacturaCreate):

    nueva = Factura(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def get_facturas(db: Session):

    return (
        db.query(Factura)
        .order_by(Factura.habilitado.desc(), Factura.id_factura.asc())
        .all()
    )


def get_factura(db: Session, factura_id: int):

    return (
        db.query(Factura)
        .filter(Factura.id_factura == factura_id, Factura.habilitado == 1)
        .first()
    )


def update_factura(db: Session, factura_id: int, data: FacturaCreate):

    factura = (
        db.query(Factura)
        .filter(Factura.id_factura == factura_id, Factura.habilitado == 1)
        .first()
    )

    if not factura:
        return None

    for key, value in data.model_dump().items():
        setattr(factura, key, value)

    db.commit()
    db.refresh(factura)

    return factura


def delete_factura(db: Session, factura_id: int):

    factura = db.query(Factura).filter(Factura.id_factura == factura_id).first()

    if not factura:
        return None

    factura.habilitado = 0

    db.commit()
    db.refresh(factura)

    return factura


def get_facturas_eliminadas(db: Session):
    return (
        db.query(Factura)
        .filter(Factura.habilitado == 0)
        .order_by(Factura.id_factura)
        .all()
    )


def restore_factura(db: Session, factura_id: int):
    factura = db.query(Factura).filter(Factura.id_factura == factura_id).first()

    if not factura:
        return None

    factura.habilitado = 1

    db.commit()
    db.refresh(factura)

    return factura
