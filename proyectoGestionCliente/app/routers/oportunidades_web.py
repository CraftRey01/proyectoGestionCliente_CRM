# app/routers/oportunidad_web.py

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from decimal import Decimal

from app.db import get_db
from app import services, schemas

router = APIRouter(tags=["Oportunidades Web"])

templates = Jinja2Templates(directory="app/templates")


# =========================================================
# LISTAR OPORTUNIDADES
# =========================================================
@router.get("/", response_class=HTMLResponse)
def vista_lista_oportunidades(request: Request, db: Session = Depends(get_db)):

    oportunidades = services.get_oportunidades(db)

    return templates.TemplateResponse(
        request=request,
        name="oportunidades/lista.html",
        context={"oportunidades": oportunidades},
    )


# =========================================================
# FORMULARIO NUEVO
# =========================================================
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_oportunidad(request: Request, db: Session = Depends(get_db)):

    clientes = services.get_clientes(db)
    usuarios = services.get_usuarios(db)

    return templates.TemplateResponse(
        request=request,
        name="oportunidades/crear.html",
        context={"clientes": clientes, "usuarios": usuarios},
    )


# =========================================================
# CREAR OPORTUNIDAD
# =========================================================
@router.post("/nuevo")
def web_create_oportunidad(
    id_oportunidad: int = Form(...),
    descripcion: str = Form(...),
    estado: str = Form(...),
    monto_estimado: Decimal = Form(...),
    id_cliente: int = Form(...),
    id_usuario: int = Form(...),
    db: Session = Depends(get_db),
):

    nueva_oportunidad = schemas.OportunidadCreate(
        id_oportunidad=id_oportunidad,
        descripcion=descripcion,
        estado=estado,
        monto_estimado=monto_estimado,
        id_cliente=id_cliente,
        id_usuario=id_usuario,
        habilitado=1,
    )

    services.create_oportunidad(db, nueva_oportunidad)

    return RedirectResponse(url="/oportunidades/", status_code=303)


# =========================================================
# FORMULARIO EDITAR
# =========================================================
@router.get("/editar/{id_oportunidad}", response_class=HTMLResponse)
def vista_editar_oportunidad(
    id_oportunidad: int, request: Request, db: Session = Depends(get_db)
):

    oportunidad = services.get_oportunidad(db, id_oportunidad)

    if not oportunidad:
        raise HTTPException(status_code=404, detail="Oportunidad no encontrada")

    clientes = services.get_clientes(db)
    usuarios = services.get_usuarios(db)

    return templates.TemplateResponse(
        request=request,
        name="oportunidades/editar.html",
        context={
            "oportunidad": oportunidad,
            "clientes": clientes,
            "usuarios": usuarios,
        },
    )


# =========================================================
# ACTUALIZAR OPORTUNIDAD
# =========================================================
@router.post("/editar/{id_oportunidad}")
def web_update_oportunidad(
    id_oportunidad: int,
    descripcion: str = Form(...),
    estado: str = Form(...),
    monto_estimado: Decimal = Form(...),
    id_cliente: int = Form(...),
    id_usuario: int = Form(...),
    db: Session = Depends(get_db),
):

    oportunidad_data = schemas.OportunidadCreate(
        id_oportunidad=id_oportunidad,
        descripcion=descripcion,
        estado=estado,
        monto_estimado=monto_estimado,
        id_cliente=id_cliente,
        id_usuario=id_usuario,
        habilitado=1,
    )

    services.update_oportunidad(db, id_oportunidad, oportunidad_data)

    return RedirectResponse(url="/oportunidades/", status_code=303)


# =========================================================
# ELIMINAR OPORTUNIDAD
# =========================================================
@router.get("/eliminar/{id_oportunidad}")
def web_delete_oportunidad(id_oportunidad: int, db: Session = Depends(get_db)):

    services.delete_oportunidad(db, id_oportunidad)

    return RedirectResponse(url="/oportunidades/", status_code=303)


@router.get("/restaurar/{id_oportunidad}")
def web_restore_oportunidad(id_oportunidad: int, db: Session = Depends(get_db)):
    services.restore_oportunidad(db, id_oportunidad)

    return RedirectResponse(url="/oportunidades/", status_code=303)


# =========================================================
# AUTOMATIZAR OPORTUNIDADES
# =========================================================
@router.get("/automatizar")
def web_automatizar_oportunidad(db: Session = Depends(get_db)):
    try:
        services.automate_next_oportunidad(db)
    except Exception:
        pass

    return RedirectResponse(url="/oportunidades/", status_code=303)
