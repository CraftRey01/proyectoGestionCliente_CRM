from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.db import create_table, SessionLocal
from app.services.notificacion import count_notificaciones_enviadas
from app.schedulers.reporte_scheduler import iniciar_scheduler, detener_scheduler

# ROUTERS
from app.routers import (
    auth_web,
    clientes_web,
    campanias_web,
    oportunidades_web,
    cotizaciones_web,
    ventas_web,
    pedidos_web,
    facturas_web,
    notificaciones_web,
    reportes_web,
    atencion_cliente_web,
    usuarios_web,
)

app = FastAPI(title="SISTEMA CRM")

# CREAR TABLAS
create_table()

# STATIC
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# RESTRICCIONES DE ACCESO POR ROL
# Define qué roles tienen permitido el ingreso a cada módulo
PERMISOS_RUTAS = {
    # ROLES
    "/clientes": [
        "administrador",
        "gerencia",
        "vendedor",
        "areacomercial",
        "atencioncliente",
    ],
    # A QUE TIENE ACCESO
    "/campanias": ["administrador", "gerencia", "areacomercial"],
    "/oportunidades": ["administrador", "gerencia", "vendedor", "areacomercial"],
    "/cotizaciones": ["administrador", "gerencia", "vendedor", "areacomercial"],
    "/ventas": ["administrador", "gerencia", "vendedor", "areacomercial"],
    "/pedidos": ["administrador", "gerencia", "vendedor", "areacomercial"],
    "/facturas": ["administrador", "gerencia", "vendedor", "areacomercial"],
    "/atencion_cliente/chat": ["administrador", "gerencia", "atencioncliente", "soporte", "agente"],
    "/atencion_cliente/enviar": ["administrador", "gerencia", "atencioncliente", "soporte", "agente"],
    "/atencion_cliente/eliminar": ["administrador", "soporte"],
    "/atencion_cliente/restaurar": ["administrador", "soporte"],
    "/atencion_cliente": ["administrador", "gerencia", "atencioncliente", "vendedor", "areacomercial"],
    "/reportes": ["administrador", "gerencia"],
    "/usuarios": ["administrador"],
}


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path
    open_paths = ["/login", "/logout", "/api/roles"]

    if path.startswith("/static") or path.startswith("/api/usuarios"):
        return await call_next(request)

    if path in open_paths:
        return await call_next(request)

    request.state.notification_count = 0
    user = request.session.get("user")

    if user is not None:
        # 1. CONTROL DE ACCESO PERIMETRAL (Seguridad basada en Roles)
        user_role = user.get("rol", "").lower()

        # Evaluamos si la ruta actual coincide con algún prefijo restringido
        for prefix, roles_permitidos in PERMISOS_RUTAS.items():
            if path.startswith(prefix):
                if user_role not in roles_permitidos:
                    # En lugar de colapsar la app con un error crudo, devolvemos una alerta visual amigable
                    return HTMLResponse(
                        content=f"""
                        <!DOCTYPE html>
                        <html lang="es">
                        <head>
                            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                        </head>
                        <body class="bg-light d-flex align-items-center justify-content-center vh-100">
                            <div class="card p-5 text-center shadow-sm" style="max-width: 500px;">
                                <h1 class="text-danger fw-bold display-4">⚠️ 403</h1>
                                <h3 class="my-3 text-dark">Acceso Restringido</h3>
                                <p class="text-muted">Tu rol actual (<strong>{user.get("rol")}</strong>) no cuenta con las autorizaciones necesarias para visualizar este módulo operativo.</p>
                                <a href="/inicio" class="btn btn-primary mt-3">Regresar al Inicio</a>
                            </div>
                        </body>
                        </html>
                        """,
                        status_code=403,
                    )

        db = SessionLocal()
        try:
            request.state.notification_count = count_notificaciones_enviadas(db) or 0
        finally:
            db.close()
    else:
        return RedirectResponse(url="/login")

    return await call_next(request)


# SessionMiddleware DEBE añadirse al final para ejecutarse primero
app.add_middleware(SessionMiddleware, secret_key="super-secreto-1234567890")


@app.on_event("startup")
def startup_event():
    iniciar_scheduler()


@app.on_event("shutdown")
def shutdown_event():
    detener_scheduler()


# RAIZ
@app.get("/")
def raiz():
    return RedirectResponse(url="/login")


# ROUTERS
app.include_router(auth_web.router)
app.include_router(clientes_web.router, prefix="/clientes")
app.include_router(campanias_web.router, prefix="/campanias")
app.include_router(oportunidades_web.router, prefix="/oportunidades")
app.include_router(cotizaciones_web.router, prefix="/cotizaciones")
app.include_router(ventas_web.router, prefix="/ventas")
app.include_router(pedidos_web.router, prefix="/pedidos")
app.include_router(facturas_web.router, prefix="/facturas")
app.include_router(atencion_cliente_web.router, prefix="/atencion_cliente")
app.include_router(usuarios_web.router, prefix="/usuarios")
app.include_router(notificaciones_web.router, prefix="/notificaciones")
app.include_router(reportes_web.router, prefix="/reportes")
