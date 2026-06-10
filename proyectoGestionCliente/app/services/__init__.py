from .usuario import (
    create_usuario,
    get_usuarios,
    get_usuario,
    update_usuario,
    delete_usuario,
    restore_usuario,
)
from .campania import (
    create_campania,
    get_campanias,
    get_campania,
    update_campania,
    delete_campania,
    restore_campania,
    set_clients_for_campania,
    automate_campania,
    automate_next_campania,
    automate_all_campanias,
)
from .mensaje_atencion import (
    create_mensaje,
    get_mensajes_por_atencion,
    get_atencion_for_chat,
)

from .atencion_cliente import (
    create_atencion_cliente,
    get_atenciones_cliente,
    get_atencion_cliente,
    update_atencion_cliente,
    delete_atencion_cliente,
    get_atenciones_activas,
    search_atenciones,
    get_atenciones_eliminadas,
    restore_atencion_cliente,
)
from .cliente import (
    create_cliente,
    get_clientes,
    get_cliente,
    update_cliente,
    delete_cliente,
    restore_cliente,
)
from .oportunidad import (
    create_oportunidad,
    get_oportunidades,
    get_oportunidad,
    update_oportunidad,
    delete_oportunidad,
    restore_oportunidad,
    automate_next_oportunidad,
)
from .cotizacion import (
    create_cotizacion,
    get_cotizaciones,
    get_cotizacion,
    update_cotizacion,
    delete_cotizacion,
    get_cotizaciones_eliminadas,
    restore_cotizacion,
)
from .venta import (
    create_venta,
    get_ventas,
    get_venta,
    update_venta,
    delete_venta,
    get_ventas_eliminadas,
    restore_venta,
    automate_next_venta,
)
from .pedido import (
    create_pedido,
    get_pedidos,
    get_pedido,
    update_pedido,
    delete_pedido,
    restore_pedido,
    automate_next_pedido,
)
from .factura import (
    create_factura,
    get_facturas,
    get_factura,
    update_factura,
    delete_factura,
    get_facturas_eliminadas,
    restore_factura,
)
from .reporte import (
    create_reporte,
    get_reportes,
    get_reportes_activos,
    get_reportes_eliminados,
    get_reporte,
    update_reporte,
    delete_reporte,
    restore_reporte,
    total_ventas,
    total_campanias,
    suma_ventas,
    ventas_por_estado,
)
from .notificacion import (
    create_notificacion,
    get_notificaciones,
    get_notificacion,
    update_notificacion,
    delete_notificacion,
    get_notificaciones_eliminadas,
    restore_notificacion,
    get_notificaciones_by_estado,
    count_notificaciones_enviadas,
)
from .metrica import obtener_metricas