"""
NoteBox - Modelo de Reportes
"""

from model.database import Database
from utils.logger import Logger

class ReportModel:
    """Modelo para generar reportes del sistema"""
    
    @staticmethod
    def get_inventory_summary():
        """Obtiene resumen general del inventario"""
        query = """
            CALL obtener_resumen_inventario()
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            if result:
                return result[0]
            return None
        except Exception as e:
            Logger.error_exception(e, "REPORT_MODEL")
            return None
    
    @staticmethod
    def get_products_by_category():
        """Obtiene productos agrupados por categoría"""
        query = """
            SELECT 
                c.nombre as categoria,
                COUNT(p.id) as total_productos,
                SUM(p.stock) as total_unidades,
                SUM(p.stock * p.precio) as valor_inventario
            FROM categorias c
            LEFT JOIN productos p ON c.id = p.categoria_id AND p.activo = TRUE
            WHERE c.activo = TRUE
            GROUP BY c.id, c.nombre
            ORDER BY c.nombre
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "REPORT_MODEL")
            return []
    
    @staticmethod
    def get_low_stock_products():
        """Obtiene productos con stock bajo"""
        query = """
            SELECT * FROM alertas_stock_bajo
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "REPORT_MODEL")
            return []
    
    @staticmethod
    def get_top_products(limit=10):
        """Obtiene los productos con mayor valor en inventario"""
        query = """
            SELECT 
                id, codigo, nombre, categoria_nombre, stock, precio,
                (stock * precio) as valor_total
            FROM productos_completos
            WHERE activo = TRUE
            ORDER BY valor_total DESC
            LIMIT %s
        """
        
        try:
            result = Database.execute_query(query, (limit,), fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "REPORT_MODEL")
            return []