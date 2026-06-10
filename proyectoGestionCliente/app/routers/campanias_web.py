# app/routers/campanias_web.py

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
import unicodedata
from typing import List, Optional

from app.db import get_db
from app import services, schemas

router = APIRouter(tags=["Campanias Web"])

templates = Jinja2Templates(directory="app/templates")


def _normalize_role(role: str) -> str:
    if not role:
        return ""
    normalized = unicodedata.normalize("NFKD", role).encode("ascii", "ignore").decode("ascii")
    return "".join(normalized.split()).lower()


def _get_user_role(request: Request) -> str:
    return _normalize_role(request.session.get("user", {}).get("rol", ""))


def _mask_phone(phone: str) -> str:
    if not phone:
        return ""
    visible = phone[:4]
    hidden = "*" * max(0, len(phone) - 4)
    return f"{visible}{hidden}"


def _mask_email(email: str) -> str:
    if not email or "@" not in email:
        return email or ""
    local, domain = email.split("@", 1)
    visible = local[:3]
    hidden = "*" * max(0, len(local) - 3)
    return f"{visible}{hidden}@{domain}"


# =========================================================
# LISTAR CAMPAÑAS
# =========================================================
@router.get("/", response_class=HTMLResponse)
def vista_lista_campanias(request: Request, db: Session = Depends(get_db)):

    campanias = services.get_campanias(db)
    user_role = _get_user_role(request)
    
    # Contar clientes por campaña y calcular métricas
    campanias_activas = [c for c in campanias if c.habilitado == 1]
    campanias_eliminadas = [c for c in campanias if c.habilitado == 0]
    
    # Agrupar por tipo
    tipos = {}
    for camp in campanias_activas:
        tipo = (camp.tipo_campania or "Sin tipo").lower()
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    context = {
        "campanias": campanias,
        "campanias_activas": campanias_activas,
        "campanias_eliminadas": campanias_eliminadas,
        "total_activas": len(campanias_activas),
        "tipos": tipos,
        "user_role": user_role,
        "can_view_clients": user_role in ["administrador", "gerencia", "areacomercial"],
        "mask_phone": _mask_phone,
        "mask_email": _mask_email,
    }

    return templates.TemplateResponse(
        request=request, name="campanias/lista.html", context=context
    )


# =========================================================
# OBTENER CLIENTES DE CAMPAÑA (API JSON)
# =========================================================
@router.get("/api/clientes/{id_campania}")
def api_clientes_campania(id_campania: int, request: Request, db: Session = Depends(get_db)):
    user_role = _get_user_role(request)
    
    if user_role not in ["administrador", "gerencia", "areacomercial"]:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    campania = services.get_campania(db, id_campania)
    if not campania:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")
    
    can_view_full = user_role in ["administrador", "gerencia"]
    
    clientes_data = []
    for cc in campania.clientes:
        cliente = cc.cliente
        clientes_data.append({
            "nombre": cliente.nombre_cliente,
            "telefono": cliente.telefono if can_view_full else _mask_phone(cliente.telefono),
            "correo": cliente.correo if can_view_full else _mask_email(cliente.correo),
            "segmento": cliente.segmento_cliente or "Nuevo",
        })
    
    return JSONResponse(content={"clientes": clientes_data})


# =========================================================
# FORMULARIO NUEVO
# =========================================================
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_campania(request: Request, db: Session = Depends(get_db)):

    # pasar lista de clientes activos para selección múltiple
    clientes = services.get_clientes(db)

    return templates.TemplateResponse(request=request, name="campanias/crear.html", context={"clientes": clientes, "selected_client_ids": []})


# =========================================================
# CREAR CAMPAÑA
# =========================================================
@router.post("/nuevo")
def web_create_campania(
    id_campania: int = Form(...),
    nombre_campania: str = Form(...),
    tipo_campania: str = Form(...),
    fecha_inicio: str = Form(...),
    fecha_finalizacion: str = Form(...),
    resultado_obtenido: str = Form(...),
    clientes: Optional[List[int]] = Form(None),
    db: Session = Depends(get_db),
):

    nueva_campania = schemas.CampaniaCreate(
        id_campania=id_campania,
        nombre_campania=nombre_campania,
        tipo_campania=tipo_campania,
        fecha_inicio=date.fromisoformat(fecha_inicio),
        fecha_finalizacion=date.fromisoformat(fecha_finalizacion),
        resultado_obtenido=resultado_obtenido,
        habilitado=1,
    )

    services.create_campania(db, nueva_campania)

    # si se enviaron clientes, asociarlos
    try:
        creada = services.get_campania(db, id_campania)
        if creada and clientes:
            services.set_clients_for_campania(db, creada.id_campania, clientes)
    except Exception:
        pass

    return RedirectResponse(url="/campanias/", status_code=303)


# =========================================================
# FORMULARIO EDITAR
# =========================================================
@router.get("/editar/{id_campania}", response_class=HTMLResponse)
def vista_editar_campania(
    id_campania: int, request: Request, db: Session = Depends(get_db)
):
    campania = services.get_campania(db, id_campania)

    if not campania:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")

    # preparar lista de clientes y marcar los ya asociados
    clientes = services.get_clientes(db)
    selected = [cc.id_cliente for cc in campania.clientes] if campania and campania.clientes else []

    return templates.TemplateResponse(
        request=request, name="campanias/editar.html", context={"campania": campania, "clientes": clientes, "selected_client_ids": selected}
    )


# =========================================================
# ACTUALIZAR CAMPAÑA
# =========================================================
@router.post("/editar/{id_campania}")
def web_update_campania(
    id_campania: int,
    nombre_campania: str = Form(...),
    tipo_campania: str = Form(...),
    fecha_inicio: str = Form(...),
    fecha_finalizacion: str = Form(...),
    resultado_obtenido: str = Form(...),
    clientes: Optional[List[int]] = Form(None),
    db: Session = Depends(get_db),
):

    campania_data = schemas.CampaniaCreate(
        id_campania=id_campania,
        nombre_campania=nombre_campania,
        tipo_campania=tipo_campania,
        fecha_inicio=date.fromisoformat(fecha_inicio),
        fecha_finalizacion=date.fromisoformat(fecha_finalizacion),
        resultado_obtenido=resultado_obtenido,
        habilitado=1,
    )

    services.update_campania(db, id_campania, campania_data)

    # actualizar asociaciones de clientes (reemplaza las previas)
    try:
        services.set_clients_for_campania(db, id_campania, clientes or [])
    except Exception:
        pass

    return RedirectResponse(url="/campanias/", status_code=303)


# =========================================================
# ELIMINAR CAMPAÑA
# =========================================================
@router.get("/eliminar/{id_campania}")
def web_delete_campania(id_campania: int, db: Session = Depends(get_db)):

    services.delete_campania(db, id_campania)

    return RedirectResponse(url="/campanias/", status_code=303)


# =========================================================
# RESTAURAR CAMPAÑA
# =========================================================
@router.get("/restaurar/{id_campania}")
def web_restore_campania(id_campania: int, db: Session = Depends(get_db)):
    services.restore_campania(db, id_campania)

    return RedirectResponse(url="/campanias/", status_code=303)


@router.get('/automatizar')
def web_automatizar_siguiente_campania(db: Session = Depends(get_db)):
    try:
        services.automate_next_campania(db)
    except Exception:
        pass

    return RedirectResponse(url="/campanias/", status_code=303)
