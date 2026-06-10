from sqlalchemy.orm import Session
from app.models.atencion_cliente import AtencionCliente
from app.schemas.atencion_cliente import AtencionClienteCreate
from app.models.cliente import Cliente
from sqlalchemy import or_


def create_atencion_cliente(db: Session, data: AtencionClienteCreate):

    nueva = AtencionCliente(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def get_atenciones_cliente(db: Session):

    return (
        db.query(AtencionCliente)
        .order_by(AtencionCliente.habilitado.desc(), AtencionCliente.id_atencion.asc())
        .all()
    )


def get_atencion_cliente(db: Session, atencion_id: int):

    return (
        db.query(AtencionCliente)
        .filter(
            AtencionCliente.id_atencion == atencion_id, AtencionCliente.habilitado == 1
        )
        .first()
    )


def update_atencion_cliente(db: Session, atencion_id: int, data: AtencionClienteCreate):

    atencion = (
        db.query(AtencionCliente)
        .filter(
            AtencionCliente.id_atencion == atencion_id, AtencionCliente.habilitado == 1
        )
        .first()
    )

    if not atencion:
        return None

    for key, value in data.model_dump(exclude={"id_atencion"}).items():
        setattr(atencion, key, value)

    db.commit()
    db.refresh(atencion)

    return atencion


def delete_atencion_cliente(db: Session, atencion_id: int):

    atencion = (
        db.query(AtencionCliente)
        .filter(AtencionCliente.id_atencion == atencion_id)
        .first()
    )

    if not atencion:
        return None

    atencion.habilitado = 0

    db.commit()
    db.refresh(atencion)

    return atencion


def get_atenciones_activas(db: Session):
    return (
        db.query(AtencionCliente)
        .filter(AtencionCliente.habilitado == 1)
        .order_by(AtencionCliente.id_atencion)
        .all()
    )


def search_atenciones(db: Session, q: str):
    if not q:
        return get_atenciones_activas(db)

    q_str = f"%{q}%"
    # intentar búsqueda por id si es numérico
    try:
        q_int = int(q)
    except Exception:
        q_int = None

    query = db.query(AtencionCliente).join(Cliente)

    if q_int is not None:
        query = query.filter(
            or_(Cliente.nombre_cliente.ilike(q_str), Cliente.id_cliente == q_int)
        )
    else:
        query = query.filter(Cliente.nombre_cliente.ilike(q_str))

    return query.order_by(AtencionCliente.habilitado.desc(), AtencionCliente.id_atencion.asc()).all()


def get_atenciones_eliminadas(db: Session):
    return (
        db.query(AtencionCliente)
        .filter(AtencionCliente.habilitado == 0)
        .order_by(AtencionCliente.id_atencion)
        .all()
    )


def restore_atencion_cliente(db: Session, atencion_id: int):
    atencion = (
        db.query(AtencionCliente)
        .filter(AtencionCliente.id_atencion == atencion_id)
        .first()
    )

    if not atencion:
        return None

    atencion.habilitado = 1

    db.commit()
    db.refresh(atencion)

    return atencion
