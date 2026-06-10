from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.oportunidad import Oportunidad
from app.models.cotizacion import Cotizacion
from app.models.pedido import Pedido
from app.models.factura import Factura
from app.models.venta import Venta
from app.models.campania import Campania
from app.models.atencion_cliente import AtencionCliente
from app.models.notificacion import Notificacion
from app.models.reporte import Reporte

def obtener_metricas(db: Session) -> dict:    
    return {
        # Gestión de Accesos y Core
        "usuarios": db.query(Usuario).count(),
        "clientes": db.query(Cliente).count(),
        
        # Embudo Comercial y Ventas
        "oportunidades": db.query(Oportunidad).count(),
        "cotizaciones": db.query(Cotizacion).count(),
        "pedidos": db.query(Pedido).count(),
        "facturas": db.query(Factura).count(),
        "ventas": db.query(Venta).count(),
        
        # Marketing y Soporte
        "campanias": db.query(Campania).count(),
        "soporte": db.query(AtencionCliente).count(),
        
        # Sistema
        "notificaciones": db.query(Notificacion).count(),
        "reportes": db.query(Reporte).count()
    }