# app/routers/reporte_web.py
from app import db
from app.schemas.reporte import Reporte
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import get_db
from app.schedulers.reporte_scheduler import generar_reporte_automatico
from app import services, schemas

router = APIRouter(tags=["Reportes Web"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def vista_lista_reportes(request: Request, db: Session = Depends(get_db)):
    
    reportes = services.get_reportes_activos(db)
    reportes_eliminados = services.get_reportes_eliminados(db)
    total_ventas = services.total_ventas(db)
    total_campanias = services.total_campanias(db)
    suma_ventas = services.suma_ventas(db)
    estados = services.ventas_por_estado(db)
    labels = [x[0] for x in estados]
    valores = [x[1] for x in estados]
    
    # Preparar datos para el gráfico: agrupar reportes por período
    reportes_por_periodo = {}
    for reporte in reportes:
        periodo = reporte.periodo or "Sin periodo"
        if periodo not in reportes_por_periodo:
            reportes_por_periodo[periodo] = 0
        reportes_por_periodo[periodo] += 1
    
    # Ordenar períodos
    periodos_ordenados = sorted(reportes_por_periodo.keys())
    conteos_reportes = [reportes_por_periodo[p] for p in periodos_ordenados]

    return templates.TemplateResponse(
        request=request,
        name="reportes/lista.html",
        context={
            "reportes": reportes,
            "reportes_eliminados": reportes_eliminados,
            "total_ventas": total_ventas,
            "total_campanias": total_campanias,
            "suma_ventas": suma_ventas,
            "labels": labels,
            "valores": valores,
            "periodos_ordenados": periodos_ordenados,
            "conteos_reportes": conteos_reportes,
        },
    )


@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_reporte(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="reportes/crear.html",
    )


@router.post("/nuevo")
def web_create_reporte(
    id_reporte: int | None = Form(None),
    tipo_reporte: str = Form(...),
    periodo: str = Form(...),
    fecha_generacion: str | None = Form(None),
    formato: str = Form(...),
    resumen: str = Form(...),
    tipo_grafico: str = Form(...),
    db: Session = Depends(get_db),
):

    nuevo_reporte = schemas.ReporteCreate(
        id_reporte=id_reporte,
        tipo_reporte=tipo_reporte,
        periodo=periodo,
        fecha_generacion=datetime.fromisoformat(fecha_generacion) if fecha_generacion else datetime.now(),
        formato=formato,
        resumen=resumen,
        tipo_grafico=tipo_grafico,
        habilitado=1,
    )

    services.create_reporte(db, nuevo_reporte)

    return RedirectResponse(
        url="/reportes/",
        status_code=303,
    )


@router.get("/automatizar")
def generar_reporte_ahora(
    db: Session = Depends(get_db),
):
    generar_reporte_automatico()
    return RedirectResponse(
        url="/reportes/",
        status_code=303,
    )


@router.get("/editar/{id_reporte}", response_class=HTMLResponse)
def vista_editar_reporte(
    id_reporte: int,
    request: Request,
    db: Session = Depends(get_db),
):

    reporte = services.get_reporte(db, id_reporte)

    if not reporte:
        raise HTTPException(
            status_code=404,
            detail="Reporte no encontrado",
        )

    return templates.TemplateResponse(
        request=request,
        name="reportes/editar.html",
        context={"reporte": reporte},
    )


@router.post("/editar/{id_reporte}")
def web_update_reporte(
    id_reporte: int,
    nuevo_id_reporte: int = Form(...),
    tipo_reporte: str = Form(...),
    periodo: str = Form(...),
    fecha_generacion: str = Form(...),
    formato: str = Form(...),
    resumen: str = Form(...),
    tipo_grafico: str = Form(...),
    db: Session = Depends(get_db),
):

    reporte_data = schemas.ReporteCreate(
        id_reporte=nuevo_id_reporte,
        tipo_reporte=tipo_reporte,
        periodo=periodo,
        fecha_generacion=datetime.fromisoformat(fecha_generacion),
        formato=formato,
        resumen=resumen,
        tipo_grafico=tipo_grafico,
        habilitado=1,
    )

    services.update_reporte(
        db,
        id_reporte,
        reporte_data,
    )

    return RedirectResponse(
        url="/reportes/",
        status_code=303,
    )

@router.get("/eliminar/{id_reporte}")
def eliminar_reporte(
    id_reporte: int,
    db: Session = Depends(get_db)
):

    services.delete_reporte(
        db,
        id_reporte
    )

    return RedirectResponse(
        url="/reportes/",
        status_code=303
    )

@router.get("/restaurar/{id_reporte}")
def restaurar_reporte(
    id_reporte: int,
    db: Session = Depends(get_db)
):

    services.restore_reporte(
        db,
        id_reporte
    )

    return RedirectResponse(
        url="/reportes/",
        status_code=303
    )

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_reportes(
    request: Request,
    db: Session = Depends(get_db),
):
    todos_reportes = services.get_reportes(db)
    reportes_por_periodo = {}
    for reporte in todos_reportes:
        periodo = reporte.periodo or "Sin periodo"
    if periodo not in reportes_por_periodo:
        reportes_por_periodo[periodo] = 0
    reportes_por_periodo[periodo] += 1

    total_ventas = services.total_ventas(db)
    total_campanias = services.total_campanias(db)
    suma_ventas = services.suma_ventas(db)
    estados = services.ventas_por_estado(db)
    labels = [x[0] for x in estados]
    valores = [x[1] for x in estados]
    return templates.TemplateResponse(
        request=request,
        name="reportes/dashboard.html",
        context={
            "total_ventas": total_ventas,
            "total_campanias": total_campanias,
            "suma_ventas": suma_ventas,
            "labels": labels,
            "valores": valores,
        },
    )
