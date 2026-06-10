import random
import threading
import time
from datetime import datetime, timedelta

from app.db import SessionLocal
from app.schemas.reporte import ReporteCreate
from app.services.reporte import (
    create_reporte,
    total_ventas,
    total_campanias,
    suma_ventas,
)

_scheduler_thread = None
_stop_event = threading.Event()


def _calcular_segundos_hasta_proximo_dia():
    ahora = datetime.now()
    manana = (ahora + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return max(0, (manana - ahora).total_seconds())


def generar_reporte_automatico():
    db = SessionLocal()
    try:
        ventas = total_ventas(db) or 0
        monto = suma_ventas(db) or 0
        campanias = total_campanias(db) or 0

        # Variar el contenido del reporte automático (tipo + mes/año + resumen)
        now = datetime.now()
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
        ]
        mes_nombre = random.choice(meses)
        anio = random.choice([now.year - 1, now.year, now.year + 1])
        periodo = f"{mes_nombre} {anio}"

        tipos = ["Ventas", "Campañas", "Clientes", "Oportunidades", "Atención"]
        tipo_sel = random.choice(tipos)

        if tipo_sel == "Ventas":
            tipo_grafico = "Barras"
            tipo_reporte = "Ventas"
            resumen = f"Ventas del mes ({periodo}). Ventas totales: {ventas}. Monto total: Bs. {monto:.2f}."
        elif tipo_sel == "Campañas":
            tipo_grafico = "Torta"
            tipo_reporte = "Campañas"
            resumen = f"Rendimiento de campañas en ({periodo}). Total campañas: {campanias}."
        elif tipo_sel == "Clientes":
            tipo_grafico = "Torta"
            tipo_reporte = "Clientes"
            resumen = f"Análisis de clientes en ({periodo}). Nuevos clientes: {max(campanias, 5)}. Retención y actividad en el mes." 
        elif tipo_sel == "Oportunidades":
            tipo_grafico = "Lineas"
            tipo_reporte = "Oportunidades"
            resumen = f"Seguimiento de oportunidades en ({periodo}). Prospectos en proceso: {max(ventas, 3)}. Avance comercial destacado." 
        else:
            tipo_grafico = "Barras"
            tipo_reporte = "Atención"
            resumen = f"Volumen de reclamos y consultas en ({periodo}). Casos revisados: {max(campanias, 2)}. Resoluciones y seguimiento." 

        reporte = ReporteCreate(
            id_reporte=0,
            tipo_reporte=tipo_reporte,
            periodo=periodo,
            fecha_generacion=now,
            formato="Web",
            resumen=resumen,
            tipo_grafico=tipo_grafico,
            habilitado=1,
        )

        create_reporte(db, reporte)
    finally:
        db.close()


def _scheduler_loop():
    # Espera hasta la próxima medianoche para inicio diario
    time_to_wait = _calcular_segundos_hasta_proximo_dia()
    if _stop_event.wait(time_to_wait):
        return

    while not _stop_event.is_set():
        generar_reporte_automatico()
        if _stop_event.wait(24 * 3600):
            break


def iniciar_scheduler():
    global _scheduler_thread
    if _scheduler_thread is not None and _scheduler_thread.is_alive():
        return

    _stop_event.clear()
    _scheduler_thread = threading.Thread(target=_scheduler_loop, daemon=True)
    _scheduler_thread.start()


def detener_scheduler():
    _stop_event.set()
    if _scheduler_thread is not None:
        _scheduler_thread.join(timeout=5)
