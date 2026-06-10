# app/routers/pedido_web.py

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import get_db
from app import services, schemas

router = APIRouter(tags=["Pedidos Web"])

templates = Jinja2Templates(directory="app/templates")


# =========================
# LISTAR PEDIDOS
# =========================
@router.get("/", response_class=HTMLResponse)
def vista_lista_pedidos(request: Request, db: Session = Depends(get_db)):
    pedidos = services.get_pedidos(db)

    return templates.TemplateResponse(
        request=request, name="pedidos/lista.html", context={"pedidos": pedidos}
    )


# =========================
# FORMULARIO NUEVO
# =========================
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_pedido(request: Request):

    return templates.TemplateResponse(request=request, name="pedidos/crear.html")


# =========================
# CREAR PEDIDO
# =========================
@router.post("/nuevo")
def web_create_pedido(
    id_pedido: int = Form(...),
    fecha_pedido: str = Form(...),
    estado: str = Form(...),
    id_venta: int = Form(...),
    db: Session = Depends(get_db),
):

    nuevo_pedido = schemas.PedidoCreate(
        id_pedido=id_pedido,
        fecha_pedido=datetime.fromisoformat(fecha_pedido),
        estado=estado,
        id_venta=id_venta,
        habilitado=1,
    )

    services.create_pedido(db, nuevo_pedido)
    return RedirectResponse(url="/pedidos/", status_code=303)


# =========================
# RESTAURAR PEDIDO
# =========================
@router.get("/restaurar/{id_pedido}")
def web_restore_pedido(id_pedido: int, db: Session = Depends(get_db)):

    services.restore_pedido(db, id_pedido)

    return RedirectResponse(url="/pedidos/", status_code=303)


# =========================
# FORMULARIO EDITAR
# =========================
@router.get("/editar/{id_pedido}", response_class=HTMLResponse)
def vista_editar_pedido(
    id_pedido: int, request: Request, db: Session = Depends(get_db)
):

    pedido = services.get_pedido(db, id_pedido)

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    ventas = services.get_ventas(db)

    return templates.TemplateResponse(
        request=request,
        name="pedidos/editar.html",
        context={"pedido": pedido, "ventas": ventas},
    )


# =========================
# ACTUALIZAR PEDIDO
# =========================
@router.post("/editar/{id_pedido}")
def web_update_pedido(
    id_pedido: int,
    fecha_pedido: str = Form(...),
    estado: str = Form(...),
    id_venta: int = Form(...),
    db: Session = Depends(get_db),
):

    pedido_data = schemas.PedidoCreate(
        id_pedido=id_pedido,
        fecha_pedido=datetime.fromisoformat(fecha_pedido),
        estado=estado,
        id_venta=id_venta,
        habilitado=1,
    )

    services.update_pedido(db, id_pedido, pedido_data)

    return RedirectResponse(url="/pedidos/", status_code=303)


# =========================
# ELIMINAR PEDIDO
# =========================
@router.get("/eliminar/{id_pedido}")
def web_delete_pedido(id_pedido: int, db: Session = Depends(get_db)):

    services.delete_pedido(db, id_pedido)

    return RedirectResponse(url="/pedidos/", status_code=303)


# =========================
# AUTOMATIZAR PEDIDO
# =========================
@router.get("/automatizar")
def web_automatizar_pedido(db: Session = Depends(get_db)):

    try:
        services.automate_next_pedido(db)
    except Exception:
        pass

    return RedirectResponse(url="/pedidos/", status_code=303)
