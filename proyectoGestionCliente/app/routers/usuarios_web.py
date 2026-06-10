from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, services

router = APIRouter(tags=["Usuarios Web"])
templates = Jinja2Templates(directory="app/templates")


# lista de usuarios
@router.get("/", response_class=HTMLResponse)
def vista_lista_usuarios(request: Request, db: Session = Depends(get_db)):
    usuarios = services.get_usuarios(db)

    return templates.TemplateResponse(
        request=request, name="usuarios/lista.html", context={"usuarios": usuarios}
    )


# formulario crear usuario
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_usuario(request: Request):

    return templates.TemplateResponse(request=request, name="usuarios/crear.html")


# crear usuario
@router.post("/nuevo")
def web_create_usuario(
    id_usuario: int = Form(...),
    nombre_usuario: str = Form(...),
    contrasena: str = Form(...),
    rol: str = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db),
):

    nuevo_usuario = schemas.UsuarioCreate(
        id_usuario=id_usuario,
        nombre_usuario=nombre_usuario,
        contrasena=contrasena,
        rol=rol,
        estado=estado,
        habilitado=1,
    )

    services.create_usuario(db, nuevo_usuario)

    return RedirectResponse(url="/usuarios/", status_code=303)


# formulario editar usuario
@router.get("/editar/{id_usuario}", response_class=HTMLResponse)
def vista_editar_usuario(
    id_usuario: int, request: Request, db: Session = Depends(get_db)
):
    usuario = services.get_usuario(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return templates.TemplateResponse(
        request=request, name="usuarios/editar.html", context={"usuario": usuario}
    )


# editar usuario
@router.post("/editar/{id_usuario}")
def web_update_usuario(
    id_usuario: int,
    id_usuario_form: int = Form(...),
    nombre_usuario: str = Form(...),
    contrasena: str = Form(""),
    rol: str = Form(...),
    estado: str = Form(...),
    db: Session = Depends(get_db),
):

    usuario_actual = services.get_usuario(db, id_usuario)
    if not usuario_actual:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar si el ID está siendo modificado
    if id_usuario_form != id_usuario and services.get_usuario(db, id_usuario_form):
        raise HTTPException(status_code=400, detail="El ID de usuario ya existe")

    if not contrasena:
        contrasena = usuario_actual.contrasena

    usuario_data = schemas.UsuarioUpdate(
        id_usuario=id_usuario_form,
        nombre_usuario=nombre_usuario,
        contrasena=contrasena,
        rol=rol,
        estado=estado,
        habilitado=1,
    )
    services.update_usuario(db, id_usuario, usuario_data)
    return RedirectResponse(url="/usuarios/", status_code=303)


# eliminar usuario
@router.get("/eliminar/{id_usuario}")
def web_delete_usuario(id_usuario: int, db: Session = Depends(get_db)):
    services.delete_usuario(db, id_usuario)
    return RedirectResponse(url="/usuarios/", status_code=303)


# restaurar usuario
@router.get("/restaurar/{id_usuario}")
def web_restore_usuario(id_usuario: int, db: Session = Depends(get_db)):
    services.restore_usuario(db, id_usuario)

    return RedirectResponse(url="/usuarios/", status_code=303)
