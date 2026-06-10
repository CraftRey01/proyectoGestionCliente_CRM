# app/routers/factura_web.pyf

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime

from app.db import get_db
from app import services, schemas

router = APIRouter(tags=["Facturas Web"])
templates = Jinja2Templates(directory="app/templates")


# LISTAR FACTURAS
@router.get("/", response_class=HTMLResponse)
def vista_lista_facturas(
    request: Request,
    db: Session = Depends(get_db),
):

    facturas = services.get_facturas(db)

    facturas_eliminadas = services.get_facturas_eliminadas(db)

    return templates.TemplateResponse(
        request=request,
        name="facturas/lista.html",
        context={
            "facturas": facturas,
            "facturas_eliminadas": facturas_eliminadas,
        },
    )


# FORMULARIO NUEVO
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_factura(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="facturas/crear.html",
    )


# CREAR FACTURA
@router.post("/nuevo")
def web_create_factura(
    id_factura: int = Form(...),
    numero_factura: str = Form(...),
    total: Decimal = Form(...),
    id_venta: int = Form(...),
    estado: str = Form(None),
    db: Session = Depends(get_db),
):

    nueva_factura = schemas.FacturaCreate(
        id_factura=id_factura,
        numero_factura=numero_factura,
        fecha_emision=datetime.now(),
        estado=estado,
        total=total,
        id_venta=id_venta,
        habilitado=1,
    )

    services.create_factura(db, nueva_factura)

    return RedirectResponse(
        url="/facturas/",
        status_code=303,
    )


# FORMULARIO EDITAR
@router.get("/editar/{id_factura}", response_class=HTMLResponse)
def vista_editar_factura(
    id_factura: int,
    request: Request,
    db: Session = Depends(get_db),
):

    factura = services.get_factura(db, id_factura)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada",
        )

    return templates.TemplateResponse(
        request=request,
        name="facturas/editar.html",
        context={"factura": factura},
    )


# ACTUALIZAR FACTURA
@router.post("/editar/{id_factura}")
def web_update_factura(
    id_factura: int,
    numero_factura: str = Form(...),
    fecha_emision: str = Form(...),
    estado: str = Form(None),
    total: Decimal = Form(...),
    id_venta: int = Form(...),
    db: Session = Depends(get_db),
):

    factura_data = schemas.FacturaCreate(
        id_factura=id_factura,
        numero_factura=numero_factura,
        fecha_emision=datetime.fromisoformat(fecha_emision),
        estado=estado,
        total=total,
        id_venta=id_venta,
        habilitado=1,
    )

    services.update_factura(
        db,
        id_factura,
        factura_data,
    )

    return RedirectResponse(
        url="/facturas/",
        status_code=303,
    )


# ELIMINAR FACTURA
@router.get("/eliminar/{id_factura}")
def web_delete_factura(
    id_factura: int,
    db: Session = Depends(get_db),
):

    services.delete_factura(db, id_factura)

    return RedirectResponse(
        url="/facturas/",
        status_code=303,
    )


# RESTAURAR FACTURA
@router.get("/restaurar/{id_factura}")
def restaurar_factura(
    id_factura: int,
    db: Session = Depends(get_db),
):

    services.restore_factura(db, id_factura)

    return RedirectResponse(
        url="/facturas/",
        status_code=303,
    )
