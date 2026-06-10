from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.usuario import Usuario
from app.services.metrica import obtener_metricas

router = APIRouter(tags=["Autenticación"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def vista_login(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url="/inicio")

    return templates.TemplateResponse(request=request, name="login.html", context={})


@router.post("/login")
def login(
    request: Request,
    nombre_usuario: str = Form(...),
    contrasena: str = Form(...),
    rol: str = Form(...),
    db: Session = Depends(get_db),
):

    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

    if not usuario:

        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": "Usuario no existe"}
        )

    if usuario.contrasena != contrasena:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Contraseña incorrecta"},
        )

    # Validar que el rol seleccionado es uno de los roles del usuario
    roles_disponibles = (
        [r.strip() for r in usuario.rol.split(",")] if usuario.rol else []
    )
    if rol not in roles_disponibles:
        return templates.TemplateResponse(
            request=request, name="login.html", context={"error": "Rol inválido"}
        )

    request.session["user"] = {
        "id_usuario": usuario.id_usuario,
        "nombre_usuario": usuario.nombre_usuario,
        "rol": rol,
    }

    return RedirectResponse(url="/inicio", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")


@router.get("/api/roles")
def obtener_todos_roles(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    roles_set = set()

    for usuario in usuarios:
        if usuario.rol:
            roles = [rol.strip() for rol in usuario.rol.split(",")]
            roles_set.update(roles)

    roles_lista = sorted(list(roles_set))
    return JSONResponse(status_code=200, content={"roles": roles_lista})


def obtener_perfil_personalizado(rol: str):
    roles = {
        "administrador": {
            "edad": 40,
            "nivel_educacion": "Maestría",
            "redes_sociales": ["LinkedIn", "Correo electrónico"],
            "labores": "Gestionar usuarios, roles y seguridad del sistema.",
            "herramientas": "Computadora de escritorio, dashboard CRM y herramientas administrativas.",
            "dispositivo": "PC de escritorio y laptop corporativa.",
            "objetivo": "Mantener control y seguridad operativa.",
            "idioma": "Español / Inglés",
        },
        "gerencia": {
            "edad": 38,
            "nivel_educacion": "Maestría",
            "redes_sociales": ["Correo electrónico", "WhatsApp"],
            "labores": "Supervisar ventas, campañas y generar reportes estratégicos.",
            "herramientas": "Laptop, CRM, herramientas de análisis y reportes.",
            "dispositivo": "Portátil y smartphone.",
            "objetivo": "Aumentar el rendimiento comercial y la toma de decisiones.",
            "idioma": "Español / Inglés",
        },
        "vendedor": {
            "edad": 29,
            "nivel_educacion": "Técnico / Bachiller",
            "redes_sociales": ["WhatsApp", "Correo electrónico"],
            "labores": "Registrar clientes, gestionar oportunidades y cerrar ventas.",
            "herramientas": "Móvil, laptop y CRM móvil.",
            "dispositivo": "Smartphone y laptop.",
            "objetivo": "Cumplir metas de venta y seguimiento al cliente.",
            "idioma": "Español / Inglés",
        },
        "areacomercial": {
            "edad": 30,
            "nivel_educacion": "Profesional",
            "redes_sociales": ["WhatsApp", "Instagram"],
            "labores": "Planificar campañas, segmentar clientes y fidelizar prospectos.",
            "herramientas": "CRM, herramientas de marketing y móvil.",
            "dispositivo": "Smartphone y laptop.",
            "objetivo": "Mejorar la relación comercial y el alcance de campañas.",
            "idioma": "Español / Inglés",
        },
        "atencioncliente": {
            "edad": 27,
            "nivel_educacion": "Técnico",
            "redes_sociales": ["WhatsApp", "Redes sociales"],
            "labores": "Atender consultas, reclamos y seguimiento de solicitudes.",
            "herramientas": "Móvil, CRM y chat de atención.",
            "dispositivo": "Smartphone y PC.",
            "objetivo": "Aumentar la satisfacción del cliente.",
            "idioma": "Español / Inglés",
        },
    }

    return roles.get(
        rol.lower(),
        {
            "edad": "N/A",
            "nivel_educacion": "N/A",
            "redes_sociales": ["Correo electrónico"],
            "labores": "Gestionar tareas del sistema según el rol.",
            "herramientas": "CRM y herramientas de trabajo estándar.",
            "dispositivo": "Computadora o smartphone.",
            "objetivo": "Cumplir con las responsabilidades asignadas.",
            "idioma": "Español / Inglés",
        },
    )


@router.get("/perfil", response_class=HTMLResponse)
def vista_perfil(request: Request):
    usuario = request.session.get("user", {})
    perfil_data = obtener_perfil_personalizado(usuario.get("rol", ""))
    return templates.TemplateResponse(
        request=request,
        name="inicio/perfil.html",
        context={"usuario": usuario, "perfil_data": perfil_data},
    )


@router.get("/configuracion", response_class=HTMLResponse)
def vista_configuracion(request: Request):
    usuario = request.session.get("user", {})
    return templates.TemplateResponse(
        request=request, name="inicio/configuracion.html", context={"usuario": usuario}
    )


@router.get("/inicio", response_class=HTMLResponse)
def vista_inicio(request: Request, db: Session = Depends(get_db)):
    usuario_sesion = request.session.get("user")
    if not usuario_sesion:
        return RedirectResponse(url="/login")

    user_role = usuario_sesion.get("rol")
    metricas = obtener_metricas(db)
    return templates.TemplateResponse(
        request=request,
        name="inicio/inicio.html",
        context={"metricas": metricas, "user_role": user_role},
    )
