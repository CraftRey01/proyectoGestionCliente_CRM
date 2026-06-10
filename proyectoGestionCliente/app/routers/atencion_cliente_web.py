# app/routers/atencion_cliente_web.py

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import random
import re

from app.db import get_db
from app import services, schemas

router = APIRouter(tags=["Atencion Cliente Web"])
templates = Jinja2Templates(directory="app/templates")


def _get_user_role(request: Request) -> str:
    return ((request.session.get("user") or {}).get("rol") or "").lower()


def _message_status(mensaje: str, remitente: str) -> str:
    texto = (mensaje or "").strip()
    if (remitente or "").lower() != "soporte":
        return "received"
    if len(texto) < 3:
        return "failed"
    if not re.search(r"[aeiouáéíóúü0-9]", texto, re.I) and len(texto) < 6:
        return "failed"
    return "sent"


def _is_invalid_support_message(mensaje: str) -> bool:
    texto = (mensaje or "").strip().lower()
    return len(texto) < 3 or not re.search(r"[aeiouáéíóúü0-9]", texto, re.I)


# LISTAR ATENCIONES
@router.get("/", response_class=HTMLResponse)
def vista_lista_atenciones(request: Request, q: Optional[str] = None, selected: Optional[int] = None, db: Session = Depends(get_db)):

    if q:
        atenciones = services.search_atenciones(db, q)
    else:
        atenciones = services.get_atenciones_activas(db)

    eliminadas = services.get_atenciones_eliminadas(db)

    # Ticket seleccionado para render del panel principal (si existe)
    atencion_seleccionada = None
    if selected:
        atencion_seleccionada = next(
            (t for t in atenciones if t.id_atencion == selected),
            None,
        )
    if not atencion_seleccionada:
        atencion_seleccionada = atenciones[0] if atenciones else None

    mensajes_preview = []
    from app.services.mensaje_atencion import get_mensajes_por_atencion
    # construir preview (último mensaje) por ticket y formatear fecha
    def fmt(m):
        try:
            hora = m.fecha.strftime("%d/%m %H:%M")
        except Exception:
            hora = ""
        return {"mensaje": (m.mensaje or ""), "remitente": (m.remitente or ""), "hora": hora}

    previews = {}
    for t in atenciones:
        ms = get_mensajes_por_atencion(db, t.id_atencion)
        previews[t.id_atencion] = fmt(ms[-1]) if ms else None

    if atencion_seleccionada:
        mensajes_preview_raw = get_mensajes_por_atencion(db, atencion_seleccionada.id_atencion)
        mensajes_preview = [fmt(m) for m in mensajes_preview_raw]

    user_role = _get_user_role(request)
    can_manage_atenciones = user_role in ["administrador", "soporte"]

    return templates.TemplateResponse(
        request=request,
        name="atencion_cliente/lista.html",
        context={
            "request": request,
            "atenciones": atenciones,
            "atenciones_eliminadas": eliminadas,
            "atencion": atencion_seleccionada,
            "mensajes": mensajes_preview,
            "previews": previews,
            "q": q,
            "selected": selected,
            "user_role": user_role,
            "can_manage_atenciones": can_manage_atenciones,
        },
    )


# FORMULARIO NUEVO
@router.get("/nuevo", response_class=HTMLResponse)
def vista_crear_atencion(request: Request, db: Session = Depends(get_db)):
    clientes = services.get_clientes(db)
    usuarios = services.get_usuarios(db)

    return templates.TemplateResponse(
        request=request,
        name="atencion_cliente/crear.html",
        context={"request": request, "clientes": clientes, "usuarios": usuarios},
    )


# CREAR ATENCION
@router.post("/nuevo")
def web_create_atencion(
    id_atencion: int = Form(...),
    fecha_registro: str = Form(...),
    tipo_solicitud: str = Form(...),
    descripcion: str = Form(...),
    prioridad: str = Form(...),
    estado: str = Form(...),
    id_cliente: int = Form(...),
    id_usuario: int = Form(...),
    db: Session = Depends(get_db),
):
    nueva_atencion = schemas.AtencionClienteCreate(
        id_atencion=id_atencion,
        fecha_registro=datetime.now(),
        tipo_solicitud=tipo_solicitud,
        descripcion=descripcion,
        prioridad=prioridad,
        estado=estado,
        id_cliente=id_cliente,
        id_usuario=id_usuario,
        habilitado=1,
    )

    services.create_atencion_cliente(db, nueva_atencion)

    return RedirectResponse(
        url="/atencion_cliente/",
        status_code=303,
    )


# FORMULARIO EDITAR
@router.get("/editar/{id_atencion}", response_class=HTMLResponse)
def vista_editar_atencion(
    id_atencion: int,
    request: Request,
    db: Session = Depends(get_db),
):

    atencion = services.get_atencion_cliente(db, id_atencion)

    if not atencion:
        raise HTTPException(
            status_code=404,
            detail="Atención no encontrada",
        )

    clientes = services.get_clientes(db)
    usuarios = services.get_usuarios(db)

    return templates.TemplateResponse(
        request=request,
        name="atencion_cliente/editar.html",
        context={
            "request": request,
            "atencion_cliente": atencion,
            "clientes": clientes,
            "usuarios": usuarios,
        },
    )


# ACTUALIZAR ATENCION
@router.post("/editar/{id_atencion}")
def web_update_atencion(
    id_atencion: int,
    fecha_registro: str = Form(...),
    tipo_solicitud: str = Form(...),
    descripcion: str = Form(...),
    prioridad: str = Form(...),
    estado: str = Form(...),
    id_cliente: int = Form(...),
    id_usuario: int = Form(...),
    db: Session = Depends(get_db),
):

    atencion_data = schemas.AtencionClienteCreate(
        id_atencion=id_atencion,
        fecha_registro=datetime.fromisoformat(fecha_registro),
        tipo_solicitud=tipo_solicitud,
        descripcion=descripcion,
        prioridad=prioridad,
        estado=estado,
        id_cliente=id_cliente,
        id_usuario=id_usuario,
        habilitado=1,
    )

    services.update_atencion_cliente(
        db,
        id_atencion,
        atencion_data,
    )

    return RedirectResponse(
        url="/atencion_cliente/",
        status_code=303,
    )


# ELIMINAR ATENCION
@router.get("/eliminar/{id_atencion}")
def web_delete_atencion(
    id_atencion: int,
    db: Session = Depends(get_db),
):

    services.delete_atencion_cliente(db, id_atencion)

    return RedirectResponse(
        url="/atencion_cliente/",
        status_code=303,
    )


# restaurar
@router.get("/restaurar/{id_atencion}")
def restaurar_atencion(id_atencion: int, db: Session = Depends(get_db)):

    services.restore_atencion_cliente(db, id_atencion)

    return RedirectResponse(url="/atencion_cliente/", status_code=303)


# CHAT (VER CONVERSACIÓN)
@router.get("/chat/{id_atencion}", response_class=HTMLResponse)
def vista_chat(
    id_atencion: int,
    request: Request,
    db: Session = Depends(get_db),
):
    atencion = services.get_atencion_cliente(db, id_atencion)
    if not atencion:
        raise HTTPException(status_code=404, detail="Atención no encontrada")

    atenciones = services.get_atenciones_activas(db)

    # Mensajes del ticket
    from app.services.mensaje_atencion import get_mensajes_por_atencion, create_mensaje
    from app.schemas.mensaje_atencion import MensajeAtencionCreate

    mensajes_raw = get_mensajes_por_atencion(db, id_atencion)

    # formatear mensajes para template (agregar hora y estado)
    def _fmt_msg(m):
        try:
            h = m.fecha.strftime("%d/%m %H:%M")
        except Exception:
            h = ""
        remitente = (m.remitente or "")
        return {
            "id_mensaje": getattr(m, "id_mensaje", None),
            "mensaje": (m.mensaje or ""),
            "remitente": remitente,
            "hora": h,
            "status": _message_status(m.mensaje, remitente),
        }

    mensajes = [ _fmt_msg(m) for m in mensajes_raw ]
    ultima_hora = mensajes[-1]['hora'] if mensajes else None

    # construir previews para la lista de conversaciones del chat
    previews = {}
    for t in atenciones:
        ms = get_mensajes_por_atencion(db, t.id_atencion)
        previews[t.id_atencion] = _fmt_msg(ms[-1]) if ms else None

    user_role = _get_user_role(request)
    can_manage_atenciones = user_role in ["administrador", "soporte"]
    can_delete_messages = user_role == "administrador"
    edit_message_id = None
    edit_message_text = None
    if can_delete_messages:
        edit_id = request.query_params.get("edit_id")
        if edit_id:
            try:
                edit_message_id = int(edit_id)
            except ValueError:
                edit_message_id = None
            else:
                for m in mensajes:
                    if m.get("id_mensaje") == edit_message_id:
                        edit_message_text = m.get("mensaje")
                        break

    q = request.query_params.get("q", "")

    # Si no hay mensajes y está abierto, generar mensaje de bienvenida del soporte
    if (not mensajes) and ((atencion.estado or "").lower() == "abierto"):
        bienvenida = f"Bienvenido, hemos recibido su {(atencion.tipo_solicitud or 'consulta').lower()}. Estamos revisando su caso."
        existe_bienvenida = False
        # Evitar duplicar
        for m in mensajes:
            if (m.get('remitente','') or '').lower() == "soporte" and (m.get('mensaje','') or '').strip() == bienvenida:
                existe_bienvenida = True
                break

        if not existe_bienvenida:
            create_mensaje(db, MensajeAtencionCreate(id_atencion=id_atencion, remitente="soporte", mensaje=bienvenida))
            mensajes_raw = get_mensajes_por_atencion(db, id_atencion)
            mensajes = [_fmt_msg(m) for m in mensajes_raw]

    # Automatización estilo conversación (tickets cerrados)
    if (atencion.estado or "").lower() == "cerrado":
        # Si ya hay un hilo automático, no duplicar
        ya_existe_hilo = any(
            (m.get('remitente','') or '').lower() == "soporte" and (m.get('mensaje','') or '').startswith("r1:")
            for m in mensajes
        )

        if not ya_existe_hilo:
            from app.schemas.mensaje_atencion import MensajeAtencionCreate
            from app.services.mensaje_atencion import create_mensaje

            # Lo que el cliente dijo (ahora lo tomamos de atencion.descripcion)
            cliente_texto = (atencion.descripcion or "").strip() or "consulta"
            tipo = (atencion.tipo_solicitud or "consulta").lower()
            # normalizamos el prefijo del cliente
            pref_cliente = "consulta" if tipo == "consulta" else "reclamo"
            cliente_mensaje = f"{pref_cliente} {cliente_texto}".strip()

            # Creamos 2-3 mensajes de ejemplo como conversación
            pasos = []
            pasos.append(("cliente", cliente_mensaje))
            pasos.append(("soporte", f"r1: precio 46464 r\" gracias por la informacion ty"))

            if "envio" in cliente_texto.lower() or "entrega" in cliente_texto.lower():
                pasos.append(("soporte", "r2: perfecto, te compartimos disponibilidad y tiempos de entrega. ty"))
            elif "garantia" in cliente_texto.lower():
                pasos.append(("soporte", "r2: revisamos garantía y te confirmamos condiciones. ty"))

            for remitente, texto in pasos:
                # evitamos duplicar si por alguna razón ya existe un mensaje idéntico
                existe = any(
                    (m.get('remitente','') or '').lower() == remitente and (m.get('mensaje','') or '') == texto
                    for m in mensajes
                )
                if not existe:
                    create_mensaje(
                        db,
                        MensajeAtencionCreate(
                            id_atencion=id_atencion,
                            remitente=remitente,
                            mensaje=texto,
                        ),
                    )

            mensajes_raw = get_mensajes_por_atencion(db, id_atencion)
            mensajes = [_fmt_msg(m) for m in mensajes_raw]

    # Render final del chat (si no se retornó antes)
    return templates.TemplateResponse(
        request=request,
        name="atencion_cliente/chat.html",
        context={
            "request": request,
            "atenciones": atenciones,
            "previews": previews,
            "atencion": atencion,
            "mensajes": mensajes,
            "ultima_hora": ultima_hora,
            "user_role": user_role,
            "can_manage_atenciones": can_manage_atenciones,
            "can_delete_messages": can_delete_messages,
            "edit_message_id": edit_message_id,
            "edit_message_text": edit_message_text,
            "q": q,
        },
    )


# ENVIAR MENSAJE DESDE CHAT
@router.post("/enviar")
def enviar_mensaje(

    id_atencion: int = Form(...),
    mensaje: str = Form(...),
    db: Session = Depends(get_db),
):

    atencion = services.get_atencion_cliente(db, id_atencion)
    if not atencion:
        raise HTTPException(status_code=404, detail="Atención no encontrada")

    # Bloqueo si está cerrada
    if (atencion.estado or "").lower() == "cerrado":
        raise HTTPException(status_code=403, detail="Esta atención está cerrada")

    # Guardar mensaje del soporte
    from app.schemas.mensaje_atencion import MensajeAtencionCreate
    from app.services.mensaje_atencion import create_mensaje

    data = MensajeAtencionCreate(
        id_atencion=id_atencion,
        remitente="soporte",
        mensaje=mensaje,
    )

    create_mensaje(db, data)

    # Automatización estilo chat real: si el soporte escribe OK/VALE/LISTO, generamos una respuesta del cliente.
    texto_normal = (mensaje or "").strip().lower()

    negativos = (
        "falta",
        "no",
        "aún",
        "aun",
        "incorrecto",
        "mal",
        "no funciona",
        "pendiente",
        "error",
        "problema",
        "no se",
        "no puedo",
        "fallo",
        "falla",
    )
    positivos = (
        "ok",
        "vale",
        "listo",
        "gracias",
        "resuelto",
        "resolví",
        "resolvi",
        "ya quedó",
        "ya quedo",
        "solucion",
        "solución",
        "perfecto",
        "funciona",
        "arreglado",
    )

    existentes = None

    def maybe_create_cliente_resp(text):
        nonlocal existentes
        if existentes is None:
            from app.services.mensaje_atencion import get_mensajes_por_atencion
            existentes = get_mensajes_por_atencion(db, id_atencion)

        # evitar duplicados exactos
        ya_existe = any((m.remitente or "").lower() == "cliente" and (m.mensaje or "").strip().lower() == text.strip().lower() for m in existentes)
        if not ya_existe:
            create_mensaje(db, MensajeAtencionCreate(id_atencion=id_atencion, remitente="cliente", mensaje=text))

    if _is_invalid_support_message(mensaje):
        respuestas_invalidas = [
            "No comprendo tu mensaje. Por favor envía más detalles.",
            "El mensaje no es claro. Intenta escribirlo de nuevo.",
        ]
        maybe_create_cliente_resp(random.choice(respuestas_invalidas))
    elif any(k in texto_normal for k in negativos):
        respuestas_neg = [
            "No, aún falta. Por favor revisen nuevamente.",
            "Sigue ocurriendo el problema, necesito más ayuda.",
            "No está resuelto, hay un error adicional.",
        ]
        maybe_create_cliente_resp(random.choice(respuestas_neg))
    elif any(k in texto_normal for k in positivos):
        respuestas_pos = [
            "Perfecto, muchas gracias. Quedo atento.",
            "Ok, genial, muchas gracias por la ayuda.",
            "Gracias, se solucionó. Buen día.",
            "Perfecto, quedó resuelto, muchas gracias.",
        ]
        maybe_create_cliente_resp(random.choice(respuestas_pos))
    else:
        # neutral: responder siempre para que el chat mantenga actividad
        respuestas_neut = [
            "Gracias por la info, quedo atento.",
            "Perfecto, gracias.",
            "Entendido, muchas gracias.",
            "Ya reviso la situación y te aviso.",
        ]
        maybe_create_cliente_resp(random.choice(respuestas_neut))


    # Mensaje automático de cierre/resolución (SIMULACIÓN)
    if (atencion.estado or "").lower() == "cerrado":
        # Evitar duplicados del resumen
        from app.services.mensaje_atencion import get_mensajes_por_atencion
        existentes = get_mensajes_por_atencion(db, id_atencion)
        ya_hay_resumen = any(
            (m.remitente or "").lower() == "soporte" and (m.mensaje or "").lower().startswith("resumen:")
            for m in existentes
        )

        if not ya_hay_resumen:
            tipo = (atencion.tipo_solicitud or "consulta").lower()
            resumen_inicio = "Consulta" if tipo == "consulta" else "Reclamo"
            auto_mensaje = (
                f"Resumen: recibimos su {resumen_inicio.lower()} y revisamos el caso. "
                f"Descripción: {atencion.descripcion or ''}"
            )

            auto = MensajeAtencionCreate(
                id_atencion=id_atencion,
                remitente="soporte",
                mensaje=auto_mensaje,
            )
            create_mensaje(db, auto)

    return RedirectResponse(url=f"/atencion_cliente/chat/{id_atencion}", status_code=303)


@router.get("/mensaje/eliminar/{id_mensaje}")
def eliminar_mensaje_chat(id_mensaje: int, request: Request, db: Session = Depends(get_db)):
    user_role = _get_user_role(request)
    if user_role != "administrador":
        raise HTTPException(status_code=403, detail="No autorizado")

    from app.services.mensaje_atencion import delete_mensaje
    delete_mensaje(db, id_mensaje)

    return RedirectResponse(url=request.headers.get("referer", "/atencion_cliente"), status_code=303)


@router.post("/mensaje/actualizar")
def actualizar_mensaje_chat(
    request: Request,
    id_atencion: int = Form(...),
    id_mensaje: int = Form(...),
    mensaje: str = Form(...),
    db: Session = Depends(get_db),
):

    user_role = _get_user_role(request)
    if user_role != "administrador":
        raise HTTPException(status_code=403, detail="No autorizado")

    from app.services.mensaje_atencion import update_mensaje
    update_mensaje(db, id_mensaje, mensaje)

    return RedirectResponse(url=f"/atencion_cliente/chat/{id_atencion}", status_code=303)


