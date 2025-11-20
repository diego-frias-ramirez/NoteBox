"""
NoteBox - Modelo de Movimientos de Inventario
"""

from model.database import Database
from utils.logger import Logger

class MovementModel:
    """Modelo para manejar movimientos de inventario"""
    
    @staticmethod
    def create(producto_id, tipo_movimiento, cantidad, motivo="", usuario="Sistema"):
        """Registra un movimiento de inventario"""
        # Primero obtener el stock actual
        query_stock = "SELECT stock FROM productos WHERE id = %s"
        
        try:
            result = Database.execute_query(query_stock, (producto_id,), fetch=True)
            if not result:
                return False, "Producto no encontrado"
            
            stock_anterior = result[0]['stock']
            
            # Calcular nuevo stock
            if tipo_movimiento == 'entrada':
                stock_nuevo = stock_anterior + cantidad
            elif tipo_movimiento == 'salida':
                stock_nuevo = stock_anterior - cantidad
                if stock_nuevo < 0:
                    return False, "No hay suficiente stock para la salida"
            else:  # ajuste
                stock_nuevo = cantidad
            
            # Registrar movimiento
            query_mov = """
                INSERT INTO movimientos 
                (producto_id, tipo_movimiento, cantidad, stock_anterior, 
                 stock_nuevo, motivo, usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            params_mov = (
                producto_id, tipo_movimiento, cantidad,
                stock_anterior, stock_nuevo, motivo, usuario
            )
            
            mov_id = Database.execute_query(query_mov, params_mov)
            
            if not mov_id:
                return False, "No se pudo registrar el movimiento"
            
            # Actualizar stock del producto
            query_update = "UPDATE productos SET stock = %s WHERE id = %s"
            Database.execute_query(query_update, (stock_nuevo, producto_id))
            
            Logger.log_database_operation(
                "INSERT", "movimientos", True,
                f"Tipo: {tipo_movimiento}, Cantidad: {cantidad}, Producto ID: {producto_id}"
            )
            
            return True, mov_id
            
        except Exception as e:
            Logger.error_exception(e, "MOVEMENT_MODEL")
            return False, str(e)
    
    @staticmethod
    def get_by_product(producto_id, limit=50):
        """Obtiene los movimientos de un producto"""
        query = """
            SELECT m.*, p.nombre as producto_nombre
            FROM movimientos m
            INNER JOIN productos p ON m.producto_id = p.id
            WHERE m.producto_id = %s
            ORDER BY m.fecha_movimiento DESC
            LIMIT %s
        """
        
        try:
            result = Database.execute_query(query, (producto_id, limit), fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "MOVEMENT_MODEL")
            return []
    
    @staticmethod
    def get_recent(limit=100):
        """Obtiene los movimientos más recientes"""
        query = """
            SELECT m.*, p.nombre as producto_nombre, p.codigo as producto_codigo
            FROM movimientos m
            INNER JOIN productos p ON m.producto_id = p.id
            ORDER BY m.fecha_movimiento DESC
            LIMIT %s
        """
        
        try:
            result = Database.execute_query(query, (limit,), fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "MOVEMENT_MODEL")
            return []
    
    @staticmethod
    def get_by_date_range(fecha_inicio, fecha_fin):
        """Obtiene movimientos en un rango de fechas"""
        query = """
            SELECT m.*, p.nombre as producto_nombre, p.codigo as producto_codigo
            FROM movimientos m
            INNER JOIN productos p ON m.producto_id = p.id
            WHERE DATE(m.fecha_movimiento) BETWEEN %s AND %s
            ORDER BY m.fecha_movimiento DESC
        """
        
        try:
            result = Database.execute_query(query, (fecha_inicio, fecha_fin), fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "MOVEMENT_MODEL")
            return []