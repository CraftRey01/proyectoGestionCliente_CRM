from sqlalchemy.orm import Session
from app.models.cliente import Cliente


# =====================================
# CREAR
# =====================================
def create_cliente(db: Session, cliente):

    nuevo_cliente = Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


# =====================================
# LISTAR
# =====================================
def get_clientes(db: Session):

    return (
        db.query(Cliente)
        .order_by(Cliente.habilitado.desc(), Cliente.id_cliente.asc())
        .all()
    )


# =====================================
# OBTENER UNO
# =====================================
def get_cliente(db: Session, id_cliente: int):
    return db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()


# =====================================
# ACTUALIZAR
# =====================================
def update_cliente(db: Session, id_cliente: int, cliente_data):

    cliente = get_cliente(db, id_cliente)
    if cliente:
        if (
            cliente_data.id_cliente is not None
            and cliente_data.id_cliente != id_cliente
        ):
            cliente.id_cliente = cliente_data.id_cliente
        cliente.nombre_cliente = cliente_data.nombre_cliente
        cliente.telefono = cliente_data.telefono
        cliente.correo = cliente_data.correo
        cliente.fecha_registro = cliente_data.fecha_registro
        cliente.segmento_cliente = cliente_data.segmento_cliente
        cliente.foto_cliente = cliente_data.foto_cliente
        db.commit()
        db.refresh(cliente)
    return cliente


# =====================================
# DELETE LOGICO
# =====================================
def delete_cliente(db: Session, id_cliente: int):

    cliente = get_cliente(db, id_cliente)
    if cliente:
        cliente.habilitado = 0
        db.commit()


# =====================================
# RESTAURAR
# =====================================
def restore_cliente(db: Session, id_cliente: int):
    cliente = get_cliente(db, id_cliente)
    if cliente:
        cliente.habilitado = 1
        db.commit()
