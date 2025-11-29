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
        # Usamos la consulta directamente en Python, como sugieres
        query = """
            SELECT
                COUNT(*) AS total_productos,
                COALESCE(SUM(CASE WHEN estado = 'Disponible' THEN 1 ELSE 0 END), 0) AS productos_disponibles,
                COALESCE(SUM(CASE WHEN estado = 'Stock Bajo' THEN 1 ELSE 0 END), 0) AS productos_stock_bajo,
                COALESCE(SUM(CASE WHEN estado = 'Agotado' THEN 1 ELSE 0 END), 0) AS productos_agotados,
                COALESCE(SUM(stock), 0) AS unidades_totales,
                COALESCE(SUM(stock * precio), 0) AS valor_total_inventario,
                COUNT(CASE WHEN dias_sin_movimiento > 30 THEN 1 END) AS productos_sin_movimiento
            FROM productos
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            if result:
                Logger.info("Resumen de inventario obtenido correctamente.", "REPORT_MODEL")
                return result[0] # Devuelve el primer (y único) registro
            else:
                Logger.warning("Consulta de resumen de inventario no devolvió resultados.", "REPORT_MODEL")
                # Devolver un diccionario con valores por defecto en caso de error o tabla vacía
                return {
                    "total_productos": 0,
                    "productos_disponibles": 0,
                    "productos_stock_bajo": 0,
                    "productos_agotados": 0,
                    "unidades_totales": 0,
                    "valor_total_inventario": 0,
                    "productos_sin_movimiento": 0
                }
        except Exception as e:
            Logger.error(f"Error al obtener resumen de inventario: {e}", "REPORT_MODEL")
            # Devolver un diccionario con valores por defecto en caso de error
            return {
                "total_productos": 0,
                "productos_disponibles": 0,
                "productos_stock_bajo": 0,
                "productos_agotados": 0,
                "unidades_totales": 0,
                "valor_total_inventario": 0,
                "productos_sin_movimiento": 0
            }
    
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
            LEFT JOIN productos p ON c.id = p.categoria_id AND p.estado != 'Agotado'
            -- WHERE c.estado != 'Inactiva'  <-- ELIMINAR ESTA LÍNEA
            GROUP BY c.id, c.nombre
            ORDER BY c.nombre
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            Logger.log_database_operation("SELECT", "productos_por_categoria", True, f"{len(result) if result else 0} categorías")
            return result if result else []
        except Exception as e:
            Logger.log_error_exception(e, "REPORT_MODEL")
            return []
    
    @staticmethod
    def get_low_stock_products():
        """Obtiene productos con stock bajo"""
        query = """
            SELECT * FROM vista_alertas_stock
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            Logger.log_database_operation("SELECT", "vista_alertas_stock", True, f"{len(result) if result else 0} productos")
            return result if result else []
        except Exception as e:
            Logger.log_error_exception(e, "REPORT_MODEL")
            return []
    
    @staticmethod
    def get_top_products(limit=10):
        """Obtiene los productos con mayor valor en inventario"""
        query = """
            SELECT 
                id, codigo, nombre, categoria_nombre, stock, precio,
                (stock * precio) as valor_total
            FROM productos_completos
            WHERE estado != 'Agotado' -- Opcional: excluir agotados
            ORDER BY valor_total DESC
            LIMIT %s
        """
        
        try:
            result = Database.execute_query(query, (limit,), fetch=True)
            Logger.log_database_operation("SELECT", "productos_top_valor", True, f"{len(result) if result else 0} productos")
            return result if result else []
        except Exception as e:
            Logger.log_error_exception(e, "REPORT_MODEL")
            return []
        
    