from pathlib import Path
from fastapi import APIRouter, Depends, Request, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
import unicodedata

from app.db import get_db
from app import services, schemas

router = APIRouter(tags=["Clientes Web"])

templates = Jinja2Templates(directory="app/templates")


def _normalize_role(role: str) -> str:
    if not role:
        return ""
    normalized = unicodedata.normalize("NFKD", role).encode("ascii", "ignore").decode("ascii")
    return "".join(normalized.split()).lower()


def _get_user_role(request: Request) -> str:
    return _normalize_role(request.session.get("user", {}).get("rol", ""))


def _assert_role(request: Request, allowed_roles: list[str]):
    if _get_user_role(request) not in allowed_roles:
        raise HTTPException(status_code=403, detail="No autorizado")


def _mask_phone(phone: str) -> str:
    if not phone:
        return ""
    visible = phone[:4]
    hidden = "*" * max(0, len(phone) - 4)
    return f"{visible}{hidden}"


def _mask_email(email: str) -> str:
    if not email or "@" not in email:
        return email or ""
    local, domain = email.split("@", 1)
    visible = local[:3]
    hidden = "*" * max(0, len(local) - 3)
    return f"{visible}{hidden}@{domain}"

STATIC_IMG_DIR = Path(__file__).resolve().parents[1] / "static" / "img"


async def save_upload_file(upload_file: UploadFile | None) -> str | None:
    if upload_file is None or upload_file.filename == "":
        return None

    filename = Path(upload_file.filename).name
    target_path = STATIC_IMG_DIR / filename
    content = await upload_file.read()
    target_path.write_bytes(content)
    return filename


@router.get("/", response_class=HTMLResponse)
def vista_lista_clientes(request: Request, db: Session = Depends(get_db)):

    clientes = services.get_clientes(db)
    user_role = _get_user_role(request)

    context = {
        "clientes": clientes,
        "user_role": user_role,
        "can_view_full": user_role in ["administrador", "gerencia"],
        "can_create": user_role in ["administrador", "atencioncliente", "vendedor"],
        "can_edit": user_role in ["administrador", "atencioncliente"],
        "can_delete": user_role == "administrador",
        "can_restore": user_role == "administrador",
        "mask_phone": _mask_phone,
        "mask_email": _mask_email,
    }

    return templates.TemplateResponse(
        request=request, name="clientes/lista.html", context=context
    )


# =========================================================
# FORMULARIO NUEVO
# =========================================================
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_cliente(request: Request):
    _assert_role(request, ["administrador", "atencioncliente", "vendedor"])

    return templates.TemplateResponse(
        request=request,
        name="clientes/crear.html",
        context={"fecha_registro": date.today().isoformat()},
    )


# =========================================================
# NUEVO CLIENTE
# =========================================================
@router.post("/nuevo")
async def web_create_cliente(
    request: Request,
    id_cliente: int = Form(...),
    nombre_cliente: str = Form(...),
    telefono: str = Form(...),
    correo: str = Form(...),
    fecha_registro: str = Form(...),
    segmento_cliente: str = Form("Nuevo"),
    foto_cliente: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    _assert_role(request, ["administrador", "atencioncliente", "vendedor"])
    if services.get_cliente(db, id_cliente):
        raise HTTPException(
            status_code=400, detail="El ID Cliente ya existe. Elige otro valor."
        )
    foto_filename = await save_upload_file(foto_cliente)
    nuevo_cliente = schemas.ClienteCreate(
        id_cliente=id_cliente,
        nombre_cliente=nombre_cliente,
        telefono=telefono,
        correo=correo,
        fecha_registro=date.fromisoformat(fecha_registro),
        segmento_cliente=segmento_cliente,
        foto_cliente=foto_filename,
        habilitado=1,
    )

    services.create_cliente(db, nuevo_cliente)
    return RedirectResponse(url="/clientes/", status_code=303)


# =========================================================
# FORMULARIO EDITAR
# =========================================================
@router.get("/editar/{id_cliente}", response_class=HTMLResponse)
def vista_editar_cliente(
    id_cliente: int, request: Request, db: Session = Depends(get_db)
):
    _assert_role(request, ["administrador", "atencioncliente"])
    cliente = services.get_cliente(db, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return templates.TemplateResponse(
        request=request, name="clientes/editar.html", context={"cliente": cliente}
    )


# =========================================================
# EDITAR CLIENTE
# =========================================================
@router.post("/editar/{id_cliente}")
async def web_update_cliente(
    request: Request,
    id_cliente: int,
    id_cliente_form: int = Form(...),
    nombre_cliente: str = Form(...),
    telefono: str = Form(...),
    correo: str = Form(...),
    fecha_registro: str = Form(...),
    segmento_cliente: str = Form("Nuevo"),
    foto_cliente: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    _assert_role(request, ["administrador", "atencioncliente"])
    cliente_existente = services.get_cliente(db, id_cliente)
    if not cliente_existente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if id_cliente_form != id_cliente and services.get_cliente(db, id_cliente_form):
        raise HTTPException(
            status_code=400, detail="El ID Cliente ya existe. Elige otro valor."
        )

    foto_filename = await save_upload_file(foto_cliente)
    if foto_filename is None:
        foto_filename = cliente_existente.foto_cliente

    cliente_data = schemas.ClienteCreate(
        id_cliente=id_cliente_form,
        nombre_cliente=nombre_cliente,
        telefono=telefono,
        correo=correo,
        fecha_registro=date.fromisoformat(fecha_registro),
        segmento_cliente=segmento_cliente,
        foto_cliente=foto_filename,
        habilitado=1,
    )

    services.update_cliente(db, id_cliente, cliente_data)

    return RedirectResponse(url="/clientes/", status_code=303)


# =========================================================
# ELIMINAR CLIENTE LOGICO
# =========================================================
@router.get("/eliminar/{id_cliente}")
def web_delete_cliente(request: Request, id_cliente: int, db: Session = Depends(get_db)):
    _assert_role(request, ["administrador"])

    services.delete_cliente(db, id_cliente)

    return RedirectResponse(url="/clientes/", status_code=303)


# =========================================================
# RESTAURAR CLIENTE
# =========================================================
@router.get("/restaurar/{id_cliente}")
def web_restore_cliente(request: Request, id_cliente: int, db: Session = Depends(get_db)):
    _assert_role(request, ["administrador"])

    services.restore_cliente(db, id_cliente)

    return RedirectResponse(url="/clientes/", status_code=303)
