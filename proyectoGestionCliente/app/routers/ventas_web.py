# app/routers/venta_web.py

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from app.db import get_db
from app import schemas, services

router = APIRouter(tags=["Ventas Web"])

templates = Jinja2Templates(directory="app/templates")


# =========================================================
# LISTAR VENTAS
# =========================================================
@router.get("/", response_class=HTMLResponse)
def vista_lista_ventas(request: Request, db: Session = Depends(get_db)):

    ventas = services.get_ventas(db)

    return templates.TemplateResponse(
        request=request, name="ventas/lista.html", context={"ventas": ventas}
    )


# =========================================================
# FORMULARIO NUEVO
# =========================================================
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_venta(request: Request, db: Session = Depends(get_db)):

    clientes = services.get_clientes(db)
    usuarios = services.get_usuarios(db)
    cotizaciones = services.get_cotizaciones(db)

    return templates.TemplateResponse(
        request=request,
        name="ventas/crear.html",
        context={
            "clientes": clientes,
            "usuarios": usuarios,
            "cotizaciones": cotizaciones,
        },
    )


# =========================================================
# CREAR VENTA
# =========================================================
@router.post("/nuevo")
def web_create_venta(
    id_venta: int = Form(...),
    fecha_venta: str = Form(None),
    estado_venta: str = Form(...),
    monto_total: Decimal = Form(...),
    id_cliente: int = Form(...),
    id_usuario: int = Form(...),
    id_cotizacion: int = Form(None),
    db: Session = Depends(get_db),
):

    fecha = datetime.now()
    if fecha_venta:
        try:
            fecha = datetime.fromisoformat(fecha_venta)
        except ValueError:
            fecha = datetime.now()

    nueva_venta = schemas.VentaCreate(
        id_venta=id_venta,
        fecha_venta=fecha,
        estado_venta=estado_venta,
        monto_total=monto_total,
        id_cliente=id_cliente,
        id_usuario=id_usuario,
        id_cotizacion=id_cotizacion,
        habilitado=1,
    )

    services.create_venta(db, nueva_venta)

    return RedirectResponse(url="/ventas/", status_code=303)


# =========================================================
# FORMULARIO EDITAR
# =========================================================
@router.get("/editar/{id_venta}", response_class=HTMLResponse)
def vista_editar_venta(id_venta: int, request: Request, db: Session = Depends(get_db)):

    venta = services.get_venta(db, id_venta)

    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    clientes = services.get_clientes(db)
    usuarios = services.get_usuarios(db)
    cotizaciones = services.get_cotizaciones(db)

    return templates.TemplateResponse(
        request=request,
        name="ventas/editar.html",
        context={
            "venta": venta,
            "clientes": clientes,
            "usuarios": usuarios,
            "cotizaciones": cotizaciones,
        },
    )


# =========================================================
# ACTUALIZAR VENTA
# =========================================================
@router.post("/editar/{id_venta}")
def web_update_venta(
    id_venta: int,
    fecha_venta: str = Form(...),
    estado_venta: str = Form(...),
    monto_total: Decimal = Form(...),
    id_cliente: int = Form(...),
    id_usuario: int = Form(...),
    id_cotizacion: int = Form(None),
    db: Session = Depends(get_db),
):

    venta_data = schemas.VentaCreate(
        id_venta=id_venta,
        fecha_venta=datetime.fromisoformat(fecha_venta),
        estado_venta=estado_venta,
        monto_total=monto_total,
        id_cliente=id_cliente,
        id_usuario=id_usuario,
        id_cotizacion=id_cotizacion,
        habilitado=1,
    )

    services.update_venta(db, id_venta, venta_data)

    return RedirectResponse(url="/ventas/", status_code=303)


# =========================================================
# ELIMINAR VENTA
# =========================================================
@router.get("/eliminar/{id_venta}")
def web_delete_venta(id_venta: int, db: Session = Depends(get_db)):

    services.delete_venta(db, id_venta)

    return RedirectResponse(url="/ventas/", status_code=303)


# =========================================================
# RESTAURAR VENTA
# =========================================================
@router.get("/restaurar/{id_venta}")
def web_restore_venta(id_venta: int, db: Session = Depends(get_db)):

    services.restore_venta(db, id_venta)

    return RedirectResponse(url="/ventas/", status_code=303)


# =========================================================
# AUTOMATIZAR VENTAS
# =========================================================
@router.get("/automatizar")
def web_automatizar_venta(db: Session = Depends(get_db)):

    try:
        services.automate_next_venta(db)
    except Exception:
        pass

    return RedirectResponse(url="/ventas/", status_code=303)
