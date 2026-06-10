# app/routers/cotizacion_web.py

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import date

from app.db import get_db
from app import services, schemas

router = APIRouter(tags=["Cotizaciones Web"])

templates = Jinja2Templates(directory="app/templates")


# =========================================================
# LISTAR COTIZACIONES
# =========================================================
@router.get("/", response_class=HTMLResponse)
def vista_lista_cotizaciones(request: Request, db: Session = Depends(get_db)):

    cotizaciones = services.get_cotizaciones(db)

    cotizaciones_eliminadas = services.get_cotizaciones_eliminadas(db)

    return templates.TemplateResponse(
        request=request,
        name="cotizaciones/lista.html",
        context={
            "cotizaciones": cotizaciones,
            "cotizaciones_eliminadas": cotizaciones_eliminadas,
        },
    )


# =========================================================
# FORMULARIO NUEVO
# =========================================================
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_cotizacion(request: Request, db: Session = Depends(get_db)):

    clientes = services.get_clientes(db)

    return templates.TemplateResponse(
        request=request, name="cotizaciones/crear.html", context={"clientes": clientes}
    )


# =========================================================
# CREAR COTIZACIÓN
# =========================================================
@router.post("/nuevo")
def web_create_cotizacion(
    id_cotizacion: int = Form(...),
    monto_estimado: Decimal = Form(...),
    estado: str = Form(...),
    id_cliente: int = Form(...),
    db: Session = Depends(get_db),
):

    nueva_cotizacion = schemas.CotizacionCreate(
        id_cotizacion=id_cotizacion,
        fecha_cotizacion=date.today(),
        monto_estimado=monto_estimado,
        estado=estado,
        id_cliente=id_cliente,
        habilitado=1,
    )

    services.create_cotizacion(db, nueva_cotizacion)
    return RedirectResponse(url="/cotizaciones/", status_code=303)


# =========================================================
# FORMULARIO EDITAR
# =========================================================
@router.get("/editar/{id_cotizacion}", response_class=HTMLResponse)
def vista_editar_cotizacion(
    id_cotizacion: int, request: Request, db: Session = Depends(get_db)
):

    cotizacion = services.get_cotizacion(db, id_cotizacion)

    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")

    clientes = services.get_clientes(db)

    return templates.TemplateResponse(
        request=request,
        name="cotizaciones/editar.html",
        context={"cotizacion": cotizacion, "clientes": clientes},
    )


# =========================================================
# ACTUALIZAR COTIZACIÓN
# =========================================================
@router.post("/editar/{id_cotizacion}")
def web_update_cotizacion(
    id_cotizacion: int,
    fecha_cotizacion: str = Form(...),
    monto_estimado: Decimal = Form(...),
    estado: str = Form(...),
    id_cliente: int = Form(...),
    db: Session = Depends(get_db),
):

    cotizacion_data = schemas.CotizacionCreate(
        id_cotizacion=id_cotizacion,
        fecha_cotizacion=date.fromisoformat(fecha_cotizacion),
        monto_estimado=monto_estimado,
        estado=estado,
        id_cliente=id_cliente,
        habilitado=1,
    )

    services.update_cotizacion(db, id_cotizacion, cotizacion_data)

    return RedirectResponse(url="/cotizaciones/", status_code=303)


# =========================================================
# ELIMINAR COTIZACIÓN
# =========================================================
@router.get("/eliminar/{id_cotizacion}")
def web_delete_cotizacion(id_cotizacion: int, db: Session = Depends(get_db)):

    services.delete_cotizacion(db, id_cotizacion)

    return RedirectResponse(url="/cotizaciones/", status_code=303)


# RESTAURAR COTIZACIÓN
@router.get("/restaurar/{id_cotizacion}")
def web_restore_cotizacion(id_cotizacion: int, db: Session = Depends(get_db)):

    services.restore_cotizacion(db, id_cotizacion)

    return RedirectResponse(url="/cotizaciones/", status_code=303)
