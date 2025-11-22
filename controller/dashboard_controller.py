"""
NoteBox - Controlador del Dashboard
"""

from model.report_model import ReportModel
from model.alert_model import AlertModel  # Importar el modelo de alertas (de base de datos)
from utils.logger import Logger
# Opcional: Si necesitas usar directamente la lógica de presentación de alertas en el controlador
# from utils.alerts import alert_manager # (Solo si es necesario llamar métodos específicos aquí)

class DashboardController:
    """Controlador para gestionar la lógica del dashboard."""

    def __init__(self, user_data):
        self.user_data = user_data
        self.report_model = ReportModel()
        self.alert_model = AlertModel() # Usar el modelo de alertas de base de datos

    def get_dashboard_summary(self):
        """Obtiene los datos resumidos para mostrar en el dashboard."""
        try:
            # Obtener resumen general del inventario (AHORA llama al nuevo código en report_model.py)
            inventory_summary = self.report_model.get_inventory_summary()

            # Obtener productos con stock bajo
            low_stock_products = self.report_model.get_low_stock_products()

            # Obtener alertas activas (usando el modelo de base de datos)
            active_alerts = self.alert_model.get_active_alerts()

            # Obtener productos de ejemplo (top 5 por valor)
            top_products = self.report_model.get_top_products(limit=5)

            Logger.info("Datos del dashboard cargados correctamente", "DASHBOARD_CONTROLLER")

            return {
                "inventory_summary": inventory_summary,
                "low_stock_products": low_stock_products,
                "active_alerts": active_alerts, # Solo los datos de la BD
                "top_products": top_products
            }
        except Exception as e:
            # CORREGIDO: Cambiar error_exception por error
            Logger.error(f"Error al cargar datos del dashboard: {e}", "DASHBOARD_CONTROLLER")
            return {
                "inventory_summary": None, # O un diccionario vacío con valores por defecto
                "low_stock_products": [],
                "active_alerts": [],
                "top_products": []
            }

    def get_user_info(self):
        """Devuelve la información del usuario logueado."""
        return self.user_data

    # Otros métodos del controlador...