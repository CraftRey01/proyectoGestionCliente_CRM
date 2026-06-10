# app/routers/notificacion_web.py

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import get_db
from app import services, schemas

router = APIRouter(tags=["Notificaciones Web"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def vista_lista_notificaciones(request: Request, db: Session = Depends(get_db)):
    notificaciones = services.get_notificaciones(db)
    notificaciones_enviadas = services.get_notificaciones_by_estado(db, "enviado")
    notificaciones_activas = [n for n in notificaciones if n.habilitado == 1]
    notificaciones_enviadas_activas = [
        n for n in notificaciones_enviadas if n.habilitado == 1
    ]
    notificaciones_pendientes = [
        n for n in notificaciones_activas if n.estado != "enviado"
    ]

    notificaciones_eliminadas = services.get_notificaciones_eliminadas(db)
    notificacion_count = len(notificaciones_enviadas_activas)

    return templates.TemplateResponse(
        request=request,
        name="notificaciones/lista.html",
        context={
            "notificaciones": notificaciones_activas,
            "notificaciones_enviadas": notificaciones_enviadas_activas,
            "notificacion_count": notificacion_count,
            "notificaciones_pendientes": notificaciones_pendientes,
            "notificaciones_eliminadas": notificaciones_eliminadas,
        },
    )


@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_notificacion(request: Request, db: Session = Depends(get_db)):
    notificacion_count = services.count_notificaciones_enviadas(db)

    return templates.TemplateResponse(
        request=request,
        name="notificaciones/crear.html",
        context={"notificacion_count": notificacion_count},
    )


@router.post("/nuevo")
def web_create_notificacion(
    id_notificacion: int = Form(...),
    mensaje: str = Form(...),
    tipo_notificacion: str = Form(...),
    fecha_envio: str | None = Form(None),
    estado: str = Form(...),
    id_usuario: int = Form(...),
    db: Session = Depends(get_db),
):

    nueva_notificacion = schemas.NotificacionCreate(
        id_notificacion=id_notificacion,
        mensaje=mensaje,
        tipo_notificacion=tipo_notificacion,
        fecha_envio=(
            datetime.fromisoformat(fecha_envio) if fecha_envio else datetime.now()
        ),
        estado=estado,
        id_usuario=id_usuario,
        habilitado=1,
    )

    services.create_notificacion(db, nueva_notificacion)

    return RedirectResponse(
        url="/notificaciones/",
        status_code=303,
    )


@router.get("/restaurar/{id_notificacion}")
def web_restore_notificacion(
    id_notificacion: int,
    db: Session = Depends(get_db),
):

    services.restore_notificacion(db, id_notificacion)

    return RedirectResponse(
        url="/notificaciones/",
        status_code=303,
    )


@router.get("/editar/{id_notificacion}", response_class=HTMLResponse)
def vista_editar_notificacion(
    id_notificacion: int,
    request: Request,
    db: Session = Depends(get_db),
):

    notificacion = services.get_notificacion(db, id_notificacion)

    if not notificacion:
        raise HTTPException(
            status_code=404,
            detail="Notificación no encontrada",
        )

    notificacion_count = services.count_notificaciones_enviadas(db)

    return templates.TemplateResponse(
        request=request,
        name="notificaciones/editar.html",
        context={
            "notificacion": notificacion,
            "notificacion_count": notificacion_count,
        },
    )


@router.post("/editar/{id_notificacion}")
def web_update_notificacion(
    id_notificacion: int,
    mensaje: str = Form(...),
    tipo_notificacion: str = Form(...),
    fecha_envio: str = Form(...),
    estado: str = Form(...),
    id_usuario: int = Form(...),
    db: Session = Depends(get_db),
):

    notificacion_data = schemas.NotificacionCreate(
        id_notificacion=id_notificacion,
        mensaje=mensaje,
        tipo_notificacion=tipo_notificacion,
        fecha_envio=datetime.fromisoformat(fecha_envio),
        estado=estado,
        id_usuario=id_usuario,
        habilitado=1,
    )

    services.update_notificacion(
        db,
        id_notificacion,
        notificacion_data,
    )

    return RedirectResponse(
        url="/notificaciones/",
        status_code=303,
    )


@router.get("/eliminar/{id_notificacion}")
def web_delete_notificacion(
    id_notificacion: int,
    db: Session = Depends(get_db),
):

    services.delete_notificacion(db, id_notificacion)

    return RedirectResponse(
        url="/notificaciones/",
        status_code=303,
    )


@router.get("/restaurar/{id_notificacion}")
def web_restore_notificacion(
    id_notificacion: int,
    db: Session = Depends(get_db),
):

    services.restore_notificacion(db, id_notificacion)

    return RedirectResponse(
        url="/notificaciones/",
        status_code=303,
    )
