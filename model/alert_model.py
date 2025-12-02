"""
NoteBox - Modelo de Alertas (Interacción con BD)
"""

from model.database import Database
from utils.logger import Logger

class AlertModel:
    """Modelo para manejar alertas en la base de datos."""

    @staticmethod
    def get_active_alerts():
        """
        Obtiene las alertas activas (no leídas) de la base de datos.

        Returns:
            list: Lista de alertas activas.
        """
        query = """
            SELECT id, tipo, producto_id, descripcion, fecha_alerta, leida, usuario_id
            FROM alertas
            WHERE leida = FALSE
            ORDER BY fecha_alerta DESC
        """

        try:
            result = Database.execute_query(query, fetch=True)
            Logger.log_database_operation("SELECT", "alertas", True, f"{len(result) if result else 0} alertas activas")
            return result if result else []
        except Exception as e:
            Logger.log_error_exception(e, "ALERT_MODEL")
            return []

    @staticmethod
    def get_unread_alerts():
        """
        Obtiene las alertas no leídas de la base de datos.
        Alias para get_active_alerts.

        Returns:
            list: Lista de alertas no leídas.
        """
        return AlertModel.get_active_alerts()

    @staticmethod
    def mark_alert_as_read(alert_id):
        """
        Marca una alerta como leída en la base de datos.

        Args:
            alert_id (int): ID de la alerta a marcar como leída.

        Returns:
            bool: True si se actualizó correctamente, False en caso contrario.
        """
        query = """
            UPDATE alertas
            SET leida = TRUE
            WHERE id = %s
        """

        try:
            result = Database.execute_query(query, (alert_id,))
            if result:
                Logger.log_database_operation("UPDATE", "alertas", True, f"Alerta ID: {alert_id} marcada como leída")
                return True
            return False
        except Exception as e:
            Logger.log_error_exception(e, "ALERT_MODEL")
            return False

    @staticmethod
    def create_alert(tipo, producto_id=None, descripcion="", usuario_id=None):
        """
        Crea una nueva alerta en la base de datos.

        Args:
            tipo (str): Tipo de alerta.
            producto_id (int, optional): ID del producto relacionado.
            descripcion (str): Descripción de la alerta.
            usuario_id (int, optional): ID del usuario relacionado.

        Returns:
            int: ID de la alerta creada, o None si falla.
        """
        query = """
            INSERT INTO alertas (tipo, producto_id, descripcion, usuario_id)
            VALUES (%s, %s, %s, %s)
        """

        params = (tipo, producto_id, descripcion, usuario_id)

        try:
            result = Database.execute_query(query, params)
            if result:
                Logger.log_database_operation("INSERT", "alertas", True, f"Alerta ID: {result} creada")
                return result
            return None
        except Exception as e:
            Logger.log_error_exception(e, "ALERT_MODEL")
            return None

    @staticmethod
    def get_all_alerts(limit=100):
        """
        Obtiene todas las alertas (leídas y no leídas) de la base de datos.
        Incluye información del producto asociado.
        
        Args:
            limit (int): Número máximo de alertas a obtener.
        
        Returns:
            list: Lista de todas las alertas.
        """
        query = """
            SELECT 
                a.id, 
                a.tipo, 
                a.producto_id, 
                a.descripcion, 
                a.fecha_alerta, 
                a.leida, 
                a.usuario_id,
                p.nombre as producto_nombre,
                p.codigo as producto_codigo,
                p.stock as producto_stock
            FROM alertas a
            LEFT JOIN productos p ON a.producto_id = p.id
            ORDER BY a.fecha_alerta DESC
            LIMIT %s
        """
        
        try:
            result = Database.execute_query(query, params=(limit,), fetch=True)
            Logger.log_database_operation("SELECT", "alertas", True, f"{len(result) if result else 0} alertas totales")
            return result if result else []
        except Exception as e:
            Logger.log_error_exception(e, "ALERT_MODEL")
            return []
    
    @staticmethod
    def check_existing_alert(tipo, producto_id, hours=24):
        """
        Verifica si ya existe una alerta del mismo tipo para el mismo producto
        en las últimas X horas.
        
        Args:
            tipo (str): Tipo de alerta.
            producto_id (int): ID del producto.
            hours (int): Número de horas hacia atrás para buscar.
        
        Returns:
            bool: True si existe una alerta similar reciente, False en caso contrario.
        """
        query = """
            SELECT COUNT(*) as count
            FROM alertas
            WHERE tipo = %s 
            AND producto_id = %s 
            AND fecha_alerta >= NOW() - INTERVAL %s HOUR
        """
        
        try:
            result = Database.execute_query(query, params=(tipo, producto_id, hours), fetch=True)
            count = result[0]['count'] if result else 0
            return count > 0
        except Exception as e:
            Logger.log_error_exception(e, "ALERT_MODEL")
            return False
    
    @staticmethod
    def mark_stock_alerts_as_resolved(producto_id):
        """
        Marca las alertas de stock bajo/agotado como leídas cuando el stock se normaliza.
        
        Args:
            producto_id (int): ID del producto.
        
        Returns:
            int: Número de alertas marcadas como resueltas.
        """
        query = """
            UPDATE alertas
            SET leida = TRUE
            WHERE producto_id = %s 
            AND tipo IN ('Stock bajo', 'Producto agotado')
            AND leida = FALSE
        """
        
        try:
            result = Database.execute_query(query, params=(producto_id,))
            if result:
                Logger.log_database_operation("UPDATE", "alertas", True, f"Alertas de stock resueltas para producto {producto_id}")
                return result
            return 0
        except Exception as e:
            Logger.log_error_exception(e, "ALERT_MODEL")
            return 0
    
    @staticmethod
    def delete_old_alerts(days=30):
        """
        Elimina alertas antiguas que ya fueron leídas.
        
        Args:
            days (int): Días de antigüedad para eliminar.
        
        Returns:
            int: Número de alertas eliminadas.
        """
        query = """
            DELETE FROM alertas
            WHERE leida = TRUE 
            AND fecha_alerta < NOW() - INTERVAL %s DAY
        """
        
        try:
            result = Database.execute_query(query, params=(days,))
            if result:
                Logger.log_database_operation("DELETE", "alertas", True, f"{result} alertas antiguas eliminadas")
                return result
            return 0
        except Exception as e:
            Logger.log_error_exception(e, "ALERT_MODEL")
            return 0
    
    @staticmethod
    def delete_read_alerts():
        """
        Elimina todas las alertas (limpieza manual completa).
        
        Returns:
            int: Número de alertas eliminadas.
        """
        query = """
            DELETE FROM alertas
        """
        
        try:
            result = Database.execute_query(query)
            if result:
                Logger.log_database_operation("DELETE", "alertas", True, f"{result} alertas eliminadas")
                return result
            return 0
        except Exception as e:
            Logger.log_error_exception(e, "ALERT_MODEL")
            return 0
