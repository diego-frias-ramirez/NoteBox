"""
NoteBox - Modelo de Alertas (Interacción con BD)
"""

from model.database import Database
from utils.logger import Logger
# No se importa utils.alerts aquí

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
                # Opcional: Notificar a la capa de presentación si es necesario
                # Aquí no se llama directamente a utils.alerts, eso lo haría el controlador o la vista
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

    # Métodos para operaciones CRUD adicionales si se necesitan
    # Por ejemplo: get_alert_by_id, delete_alert, etc.