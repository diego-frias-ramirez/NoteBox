"""
NoteBox - Modelo de Movimientos
Ubicación: model/movement_model.py
"""

import sys
import os
import datetime

# Asegurar que el módulo 'model' esté en el path para imports relativos
model_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(model_path)

from model.database import Database
from utils.logger import Logger

class MovementModel:
    """Modelo para gestionar movimientos de inventario."""

    def __init__(self):
        self.db = Database()

    def register_movement(self, product_id, quantity, movement_type, reason, user_id, notes=""):
        """
        Registra un movimiento de inventario (entrada o salida).
        
        Args:
            product_id (int): ID del producto.
            quantity (int): Cantidad movida.
            movement_type (str): 'Entrada' o 'Salida'.
            reason (str): Motivo del movimiento.
            user_id (int): ID del usuario que registra.
            notes (str): Notas adicionales.
        
        Returns:
            int: ID del movimiento registrado, o None si falló.
        """
        query = """
            INSERT INTO movimientos (
                tipo, producto_id, cantidad, motivo, fecha, usuario_id, notas
            ) VALUES (%s, %s, %s, %s, NOW(), %s, %s)
        """
        params = (movement_type, product_id, quantity, reason, user_id, notes)
        
        try:
            movement_id = self.db.execute_query(query, params=params)
            if movement_id:
                # Actualizar el stock del producto
                if movement_type == "Entrada":
                    update_stock_query = "UPDATE productos SET stock = stock + %s WHERE id = %s"
                else:  # Salida
                    update_stock_query = "UPDATE productos SET stock = stock - %s WHERE id = %s AND stock >= %s"
                    # Verificar que haya suficiente stock antes de actualizar
                    check_stock_query = "SELECT stock FROM productos WHERE id = %s"
                    current_stock = self.db.execute_query(check_stock_query, params=(product_id,), fetch=True)
                    if not current_stock or current_stock[0]['stock'] < quantity:
                        msg = f"Stock insuficiente para salida del producto ID {product_id}. Stock actual: {current_stock[0]['stock'] if current_stock else 0}, Cantidad solicitada: {quantity}"
                        Logger.error(msg, "MOVEMENT_MODEL")
                        return None, msg
                
                # Ejecutar la actualización del stock
                if movement_type == "Entrada":
                    stock_params = (quantity, product_id)
                else:
                    stock_params = (quantity, product_id, quantity)

                rows_affected = self.db.execute_query(update_stock_query, params=stock_params)
                
                if rows_affected > 0:
                    Logger.success(f"Movimiento ID {movement_id} registrado y stock actualizado", "MOVEMENT_MODEL")
                    return movement_id, None
                else:
                    msg = f"No se pudo actualizar el stock del producto ID {product_id} después del movimiento"
                    Logger.error(msg, "MOVEMENT_MODEL")
                    return None, msg
            else:
                msg = "No se pudo registrar el movimiento en la base de datos"
                Logger.error(msg, "MOVEMENT_MODEL")
                return None, msg
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENT_MODEL")
            return None, str(e)

    def get_movements(self, limit=5, offset=0):
        """
        Obtiene movimientos con paginación.
        
        Args:
            limit (int): Límite de resultados por página.
            offset (int): Offset para paginación.
        
        Returns:
            list: Lista de movimientos.
        """
        query = """
            SELECT 
                m.id, m.tipo, m.producto_id, p.nombre AS producto_nombre,
                m.cantidad, m.motivo, m.fecha, m.usuario_id, u.nombre AS usuario_nombre,
                m.notas
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            JOIN usuarios u ON m.usuario_id = u.id
            ORDER BY m.fecha DESC
            LIMIT %s OFFSET %s
        """
        try:
            result = self.db.execute_query(query, params=(limit, offset), fetch=True)
            Logger.info(f"Obtenidos {len(result) if result else 0} movimientos", "MOVEMENT_MODEL")
            return result if result else []
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENT_MODEL")
            return []

    def get_all_movements(self):
        """
        Obtiene todos los movimientos sin paginación.
        Returns:
            list: Lista completa de movimientos.
        """
        query = """
            SELECT 
                m.id, m.tipo, m.producto_id, p.nombre AS producto_nombre,
                m.cantidad, m.motivo, m.fecha, m.usuario_id, u.nombre AS usuario_nombre,
                m.notas
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            JOIN usuarios u ON m.usuario_id = u.id
            ORDER BY m.fecha DESC
        """
        try:
            result = self.db.execute_query(query, fetch=True)
            Logger.info(f"Obtenidos {len(result) if result else 0} movimientos (todos)", "MOVEMENT_MODEL")
            return result if result else []
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENT_MODEL")
            return []

    def get_movements_by_product(self, product_id):
        """
        Obtiene todos los movimientos de un producto específico.
        
        Args:
            product_id (int): ID del producto.
        
        Returns:
            list: Lista de movimientos del producto.
        """
        query = """
            SELECT 
                m.id, m.tipo, m.producto_id, p.nombre AS producto_nombre,
                m.cantidad, m.motivo, m.fecha, m.usuario_id, u.nombre AS usuario_nombre,
                m.notas
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.producto_id = %s
            ORDER BY m.fecha DESC
        """
        try:
            result = self.db.execute_query(query, params=(product_id,), fetch=True)
            Logger.info(f"Obtenidos {len(result) if result else 0} movimientos para el producto ID {product_id}", "MOVEMENT_MODEL")
            return result if result else []
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENT_MODEL")
            return []

    def get_total_movements(self):
        """
        Obtiene el total de movimientos registrados.
        
        Returns:
            int: Número total de movimientos.
        """
        query = "SELECT COUNT(*) as total FROM movimientos"
        try:
            result = self.db.execute_query(query, fetch=True)
            total = result[0]['total'] if result else 0
            Logger.info(f"Total de movimientos obtenidos: {total}", "MOVEMENT_MODEL")
            return total
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENT_MODEL")
            return 0

    def get_daily_summary(self):
        """
        Obtiene un resumen diario de entradas y salidas.
        
        Returns:
            dict: Diccionario con el resumen diario.
        """
        today = datetime.date.today().isoformat()
        query = f"""
            SELECT 
                SUM(CASE WHEN tipo = 'Entrada' THEN cantidad ELSE 0 END) as entradas,
                SUM(CASE WHEN tipo = 'Salida' THEN cantidad ELSE 0 END) as salidas,
                COUNT(CASE WHEN tipo = 'Entrada' THEN 1 END) as count_entradas,
                COUNT(CASE WHEN tipo = 'Salida' THEN 1 END) as count_salidas
            FROM movimientos
            WHERE DATE(fecha) = '{today}'
        """
        try:
            result = self.db.execute_query(query, fetch=True)
            summary = {
                "entradas": result[0]['entradas'] if result and result[0]['entradas'] else 0,
                "salidas": result[0]['salidas'] if result and result[0]['salidas'] else 0,
                "count_entradas": result[0]['count_entradas'] if result else 0,
                "count_salidas": result[0]['count_salidas'] if result else 0
            }
            Logger.info(f"Resumen diario obtenido: {summary}", "MOVEMENT_MODEL")
            return summary
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENT_MODEL")
            return {"entradas": 0, "salidas": 0, "count_entradas": 0, "count_salidas": 0}

