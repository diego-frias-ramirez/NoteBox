"""
NoteBox - Controlador del Dashboard
"""

from model.product_model import ProductModel
from model.category_model import CategoryModel
from model.report_model import ReportModel
from utils.logger import Logger
from utils.helpers import Helpers

class DashboardController:
    """Controlador para el dashboard principal"""
    
    def __init__(self):
        self.product_model = ProductModel
        self.category_model = CategoryModel
        self.report_model = ReportModel
    
    def get_dashboard_data(self):
        """Obtiene todos los datos necesarios para el dashboard"""
        try:
            # Obtener resumen del inventario
            summary = self.report_model.get_inventory_summary()
            
            # Obtener productos con stock bajo
            low_stock = self.product_model.get_low_stock()
            
            # Obtener productos por categoría
            by_category = self.report_model.get_products_by_category()
            
            # Obtener top productos
            top_products = self.report_model.get_top_products(5)
            
            data = {
                'summary': summary if summary else {
                    'total_productos': 0,
                    'productos_ok': 0,
                    'productos_stock_bajo': 0,
                    'productos_sin_stock': 0,
                    'unidades_totales': 0,
                    'valor_total_inventario': 0.0
                },
                'low_stock': low_stock,
                'by_category': by_category,
                'top_products': top_products
            }
            
            Logger.info("Datos del dashboard cargados correctamente", "DASHBOARD_CONTROLLER")
            return True, data
            
        except Exception as e:
            Logger.error_exception(e, "DASHBOARD_CONTROLLER")
            return False, None
    
    def get_statistics(self):
        """Obtiene estadísticas del inventario"""
        try:
            stats = self.report_model.get_inventory_summary()
            
            if stats:
                # Formatear valores
                formatted_stats = {
                    'total_productos': Helpers.format_number(stats['total_productos']),
                    'productos_ok': Helpers.format_number(stats['productos_ok']),
                    'productos_stock_bajo': Helpers.format_number(stats['productos_stock_bajo']),
                    'productos_sin_stock': Helpers.format_number(stats['productos_sin_stock']),
                    'unidades_totales': Helpers.format_number(stats['unidades_totales']),
                    'valor_total': Helpers.format_currency(stats['valor_total_inventario'])
                }
                
                return True, formatted_stats
            
            return False, None
            
        except Exception as e:
            Logger.error_exception(e, "DASHBOARD_CONTROLLER")
            return False, None
    
    def get_alerts_count(self):
        """Obtiene el conteo de alertas"""
        try:
            low_stock = self.product_model.get_low_stock()
            return len(low_stock)
        except Exception as e:
            Logger.error_exception(e, "DASHBOARD_CONTROLLER")
            return 0
    
    def refresh_data(self):
        """Refresca los datos del dashboard"""
        Logger.info("Refrescando datos del dashboard", "DASHBOARD_CONTROLLER")
        return self.get_dashboard_data()