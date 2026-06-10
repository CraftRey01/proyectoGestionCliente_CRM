from datetime import date, timedelta
import random

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.campania import Campania
from app.schemas.campania import CampaniaCreate
from app.models.cliente_campania import ClienteCampania
from app.models.cliente import Cliente


def create_campania(db: Session, data: CampaniaCreate):

    nueva = Campania(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def get_campanias(db: Session):
    return (
        db.query(Campania)
        .order_by(Campania.habilitado.desc(), Campania.id_campania.asc())
        .all()
    )


def get_campania(db: Session, campania_id: int):

    return (
        db.query(Campania)
        .filter(Campania.id_campania == campania_id, Campania.habilitado == 1)
        .first()
    )


def update_campania(db: Session, campania_id: int, data: CampaniaCreate):

    campania = (
        db.query(Campania)
        .filter(Campania.id_campania == campania_id, Campania.habilitado == 1)
        .first()
    )

    if not campania:
        return None

    for key, value in data.model_dump(exclude={"id_campania"}).items():
        setattr(campania, key, value)

    db.commit()
    db.refresh(campania)

    return campania


def delete_campania(db: Session, campania_id: int):

    campania = db.query(Campania).filter(Campania.id_campania == campania_id).first()

    if not campania:
        return None

    campania.habilitado = 0

    db.commit()
    db.refresh(campania)

    return campania


def restore_campania(db: Session, campania_id: int):
    campania = db.query(Campania).filter(Campania.id_campania == campania_id).first()

    if not campania:
        return None

    campania.habilitado = 1

    db.commit()
    db.refresh(campania)

    return campania


def set_clients_for_campania(db: Session, campania_id: int, client_ids: list):
    """Reemplaza las asociaciones cliente<->campania con la lista suministrada.

    client_ids: lista de enteros (id_cliente)
    """
    # eliminar asociaciones previas
    db.query(ClienteCampania).filter(ClienteCampania.id_campania == campania_id).delete()

    # agregar nuevas asociaciones (si existen clientes)
    if client_ids:
        # opcional: validar que existan los clientes
        valid_ids = [c.id_cliente for c in db.query(Cliente).filter(Cliente.id_cliente.in_(client_ids)).all()]
        for cid in valid_ids:
            assoc = ClienteCampania(id_cliente=cid, id_campania=campania_id)
            db.add(assoc)

    db.commit()

    return True


def automate_campania(db: Session, campania_id: int):
    """Genera un reporte simple asociado a la campaña y devuelve el id del reporte creado."""
    from app.models.reporte import Reporte
    from app.models.reporte_analisis import ReporteAnalisis

    camp = db.query(Campania).filter(Campania.id_campania == campania_id).first()
    if not camp:
        return None

    # contar clientes asignados
    cliente_count = db.query(ClienteCampania).filter(ClienteCampania.id_campania == campania_id).count()

    resumen = f"Automatización de campaña '{camp.nombre_campania}': {cliente_count} clientes asignados."

    reporte = Reporte(
        tipo_reporte='campania',
        periodo=str(camp.fecha_inicio) + ' - ' + str(camp.fecha_finalizacion),
        formato='texto',
        resumen=resumen,
        tipo_grafico='none',
        habilitado=1,
    )

    db.add(reporte)
    db.commit()
    db.refresh(reporte)

    # crear enlace en reporte_analisis
    analisis = ReporteAnalisis(id_reporte=reporte.id_reporte, id_campania=campania_id)
    db.add(analisis)
    db.commit()

    return reporte.id_reporte


def _generate_next_campaign_data(index: int):
    """Genera nombres y tipos personalizados y aleatorios para campañas.

    Produce nombres más naturales para CRM (ej.:
    'Registro Webinars Ciberseguridad', 'Preventa Lanzamiento Móvil Corporativo',
    'Renovación Tecnológica Empresas').
    """
    # Plantillas y componentes
    verbs = [
        "Registro",
        "Preventa",
        "Renovación",
        "Lanzamiento",
        "Programa",
        "Campaña",
        "Oferta",
    ]

    actions = [
        "Webinars",
        "Lanzamiento",
        "Campaña",
        "Serie",
        "Evento",
        "Roadshow",
    ]

    subjects = [
        "Ciberseguridad",
        "Móvil",
        "Tecnológica",
        "Cloud",
        "Servidores",
        "Software",
        "Accesorios",
        "Infraestructura",
        "Redes",
        "IA",
    ]

    audiences = [
        "Empresas",
        "Corporativo",
        "PYMES",
        "Clientes",
        "Partners",
    ]

    tipos = ["Tecnologia", "Oficina", "Redes", "Movil", "Empresarial", "Promocional", "Corporativa", "Registro"]

    # Primeros nombres conocidos si aplica
    predefined = [
        ("Promo Laptops", "Tecnologia"),
        ("Promo Impresoras", "Oficina"),
        ("Promo Routers", "Redes"),
        ("Promo Monitores", "Tecnologia"),
        ("Promo Servidores", "Corporativa"),
        ("Promo Switches", "Redes"),
        ("Promo PCs", "Tecnologia"),
        ("Promo Tablets", "Movil"),
        ("Promo Accesorios", "Promocional"),
        ("Promo Software", "Empresarial"),
    ]

    if index < len(predefined):
        return predefined[index]

    # Usar una semilla derivada del índice para estabilidad y variedad
    rnd = random.Random(index + 2026)

    verb = rnd.choice(verbs)
    action = rnd.choice(actions)
    subject = rnd.choice(subjects)
    audience = rnd.choice(audiences)

    templates = [
        f"{verb} {action} {subject}",
        f"{verb} {subject} {audience}",
        f"{action} {subject} para {audience}",
        f"{verb} {action} {audience}",
    ]

    name = rnd.choice(templates)
    tipo = rnd.choice(tipos)

    return name, tipo


def automate_next_campania(db: Session):
    """Crea una nueva campaña automática con datos secuenciales y lógicos."""
    max_id = db.query(func.coalesce(func.max(Campania.id_campania), 0)).scalar() or 0
    nuevo_id = max_id + 1
    last_campania = db.query(Campania).order_by(Campania.id_campania.desc()).first()
    base_start = last_campania.fecha_inicio if last_campania and last_campania.fecha_inicio else date.today()
    nombre, tipo = _generate_next_campaign_data(nuevo_id - 1)

    fecha_inicio = base_start + timedelta(days=7 * nuevo_id)
    fecha_finalizacion = fecha_inicio + timedelta(days=30)
    resultado_obtenido = (
        f"Campaña {nuevo_id} enfocada en {tipo.lower()}, con oferta personalizada y campaña automática basada en los anteriores registros."
    )

    nueva = Campania(
        id_campania=nuevo_id,
        nombre_campania=nombre,
        tipo_campania=tipo,
        fecha_inicio=fecha_inicio,
        fecha_finalizacion=fecha_finalizacion,
        resultado_obtenido=resultado_obtenido,
        habilitado=1,
    )
    db.add(nueva)
    db.commit()

    client_ids = [c.id_cliente for c in db.query(Cliente).filter(Cliente.habilitado == 1).order_by(Cliente.id_cliente).all()]
    if client_ids:
        selected_clients = [client_ids[i % len(client_ids)] for i in range(3)]
        set_clients_for_campania(db, nuevo_id, selected_clients)

    return nuevo_id


def automate_all_campanias(db: Session, count: int = 3):
    """Alias para compatibilidad: crea varias campañas automáticas si se desea."""
    ids = []
    for _ in range(count):
        ids.append(automate_next_campania(db))
    return ids
