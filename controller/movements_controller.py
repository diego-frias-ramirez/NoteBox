"""
NoteBox - Controlador del Módulo de Movimientos
Responsabilidad: Gestionar la lógica del módulo de movimientos, conectar vista y modelo.
Ubicación: controller/movements_controller.py
"""

import os
import sys
from datetime import datetime

# Asegurar que el módulo 'controller' esté en el path para imports relativos
controller_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(controller_path)

from model.movement_model import MovementModel
from model.product_model import ProductModel
from model.user_model import UserModel
from utils.logger import Logger
from utils.validators import Validators

class MovementsController:
    """Controlador para gestionar la lógica del módulo de movimientos."""

    def __init__(self):
        self.movement_model = MovementModel()  # ✅ Instancia única del modelo de movimientos
        self.product_model = ProductModel()    # ✅ Para obtener productos si es necesario
        self.user_model = UserModel()          # ✅ Para obtener usuarios si es necesario
        self.current_user = None               # ✅ Usuario actual para auditoría

    def set_current_user(self, user_data):
        """Establece el usuario actual para auditoría."""
        self.current_user = user_data

    def get_movements(self, page=1, limit=5):
        """
        Obtiene movimientos con paginación.
        
        Args:
            page (int): Número de página.
            limit (int): Límite de movimientos por página.
        
        Returns:
            tuple: (lista de movimientos, total de movimientos).
        """
        try:
            offset = (page - 1) * limit
            movements = self.movement_model.get_movements(limit=limit, offset=offset)
            total = self.movement_model.get_total_movements()
            
            Logger.info(f"Movimientos obtenidos: {len(movements)}, Total: {total}", "MOVEMENTS_CONTROLLER")
            return movements, total
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return [], 0

    def get_daily_summary(self):
        """
        Obtiene el resumen diario de entradas y salidas.
        
        Returns:
            dict: Resumen diario.
        """
        try:
            summary = self.movement_model.get_daily_summary()
            Logger.info(f"Resumen diario obtenido: {summary}", "MOVEMENTS_CONTROLLER")
            return summary
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return {"entradas": 0, "salidas": 0, "count_entradas": 0, "count_salidas": 0}

    def register_movement(self, product_id, quantity, movement_type, reason, notes=""):
        """
        Registra un movimiento y devuelve el estado, mensaje y datos del producto actualizado.
        
        Returns:
            tuple: (success: bool, message: str, updated_product: dict or None)
        """
        # Validar usuario actual
        if not self.current_user:
            return False, "No hay usuario autenticado", None

        user_id = self.current_user.get("id")

        # Usar el modelo para registrar el movimiento
        success, message = self.movement_model.register_movement(
            product_id=product_id,
            quantity=quantity,
            movement_type=movement_type,
            reason=reason,
            user_id=user_id,
            notes=notes
        )

        if not success:
            return False, message, None

        # Obtener datos actualizados del producto
        try:
            updated_product = self.movement_model.get_product_by_id(product_id)
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            updated_product = None

        return True, message, updated_product

    def get_products(self, limit=1000):
        """
        Obtiene una lista de productos activos para el selector.
        
        Args:
            limit (int): Límite máximo de productos a devolver.
        
        Returns:
            list: Lista de productos.
        """
        try:
            # Usar directamente el ProductModel (ya está inicializado)
            query = """
                SELECT id, codigo, nombre, categoria_id, stock, stock_minimo, precio, estado
                FROM productos
                WHERE activo = TRUE
                ORDER BY nombre ASC
                LIMIT %s
            """
            params = (limit,)
            products = self.product_model.db.execute_query(query, params=params, fetch=True)
            
            Logger.info(f"Productos obtenidos para el selector: {len(products) if products else 0}", "MOVEMENTS_CONTROLLER")
            return products if products else []
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return []

    def get_users(self):
        """Obtiene todos los usuarios para el selector."""
        try:
            users = self.user_model.get_all_users()  # Asumiendo que este método existe
            Logger.info(f"Usuarios obtenidos para el selector: {len(users)}", "MOVEMENTS_CONTROLLER")
            return users
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return []

    def get_all_movements(self):
        """
        Obtiene todos los movimientos sin paginación.
        
        Returns:
            list: Todos los movimientos.
        """
        try:
            movements = self.movement_model.get_all_movements()
            Logger.info(f"Movimientos completos obtenidos: {len(movements)}", "MOVEMENTS_CONTROLLER")
            return movements
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return []

    def export_movements(self, movements_data, filepath=None):
        """
        Exporta los movimientos a un archivo CSV.
        
        Args:
            movements_data (list): Lista de diccionarios con datos de movimientos.
            filepath (str): Ruta completa para guardar el archivo (opcional).
            
        Returns:
            tuple: (bool, str) - (Éxito, Ruta del archivo o mensaje de error)
        """
        try:
            if not movements_data:
                return False, "No hay datos para exportar"
                
            import pandas as pd
            import os
            from datetime import datetime
            
            # Convertir a DataFrame
            df = pd.DataFrame(movements_data)
            
            # Seleccionar y renombrar columnas para una mejor exportación
            # Asegurarse de que las columnas existen antes de renombrar
            columns_map = {
                'id': 'ID',
                'tipo': 'Tipo',
                'producto_nombre': 'Producto',
                'cantidad': 'Cantidad',
                'motivo': 'Motivo',
                'fecha': 'Fecha',
                'usuario_nombre': 'Usuario',
                'notas': 'Notas'
            }
            
            # Filtrar columnas que existen en el DataFrame
            existing_cols = [c for c in columns_map.keys() if c in df.columns]
            df = df[existing_cols]
            df = df.rename(columns=columns_map)
            
            if filepath:
                # Si se proporciona ruta completa, usarla
                final_filepath = filepath
            else:
                # Definir ruta de exportación por defecto
                from utils.helpers import Helpers
                export_dir = Helpers.get_exports_dir("reports")
                
                # Generar nombre de archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"movimientos_{timestamp}.csv"
                final_filepath = os.path.join(export_dir, filename)
            
            # Guardar a CSV
            df.to_csv(final_filepath, index=False, encoding='utf-8-sig')
            
            Logger.success(f"Movimientos exportados a: {final_filepath}", "MOVEMENTS_CONTROLLER")
            return True, final_filepath
            
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return False, str(e)