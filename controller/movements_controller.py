"""
NoteBox - Controlador del Módulo de Movimientos
Responsabilidad: Gestionar la lógica del módulo de movimientos, conectar vista y modelo.
Ubicación: controller/movements_controller.py
"""

import os
import sys

# Asegurar que el módulo 'controller' esté en el path para imports relativos
controller_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(controller_path)

from model.movement_model import MovementModel
from model.product_model import ProductModel
from model.user_model import UserModel
from utils.logger import Logger
from utils.validators import Validators
from datetime import datetime

class MovementsController:
    """Controlador para gestionar la lógica del módulo de movimientos."""

    def __init__(self):
        self.movement_model = MovementModel()
        self.product_model = ProductModel()
        self.user_model = UserModel()
        self.current_user = None # Se puede inicializar aquí o recibirlo en cada método

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
        Registra un movimiento de inventario.
        
        Args:
            product_id (int): ID del producto.
            quantity (int): Cantidad movida.
            movement_type (str): 'Entrada' o 'Salida'.
            reason (str): Motivo del movimiento.
            notes (str): Notas adicionales.
        
        Returns:
            tuple: (bool: éxito, str: mensaje).
        """
        # Validar datos de entrada
        is_valid, msg = Validators.validate_movement_data(product_id, quantity, movement_type, reason)
        if not is_valid:
            Logger.warning(f"Validación fallida en registro de movimiento: {msg}", "MOVEMENTS_CONTROLLER")
            return False, msg
        
        try:
            # Registrar el movimiento
            movement_id = self.movement_model.register_movement(
                product_id=product_id,
                quantity=quantity,
                movement_type=movement_type,
                reason=reason,
                user_id=self.current_user['id'],
                notes=notes
            )
            
            if movement_id:
                Logger.success(f"Movimiento ID {movement_id} registrado correctamente", "MOVEMENTS_CONTROLLER")
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action("REGISTRAR_MOVIMIENTO", self.current_user['nombre'], details=f"ID: {movement_id}, Tipo: {movement_type}, Producto: {product_id}, Cantidad: {quantity}")
                return True, f"Movimiento registrado correctamente (ID: {movement_id})"
            else:
                error_msg = "No se pudo registrar el movimiento"
                Logger.error(error_msg, "MOVEMENTS_CONTROLLER")
                return False, error_msg
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return False, str(e)

    def get_products(self):
        """Obtiene todos los productos activos para el selector."""
        try:
            products = self.product_model.get_all_products() # Asumiendo que tienes este método
            Logger.info(f"Productos obtenidos para el selector: {len(products)}", "MOVEMENTS_CONTROLLER")
            return products
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return []

    def get_users(self):
        """Obtiene todos los usuarios para el selector."""
        try:
            users = self.user_model.get_all_users() # Asumiendo que tienes este método
            Logger.info(f"Usuarios obtenidos para el selector: {len(users)}", "MOVEMENTS_CONTROLLER")
            return users
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_CONTROLLER")
            return []

if __name__ == "__main__":
    # Prueba rápida del controlador
    controller = MovementsController()
    
    # Cargar resumen diario
    summary = controller.get_daily_summary()
    print("Resumen diario:", summary)
    
    # Cargar movimientos (primera página)
    movements, total = controller.get_movements()
    print(f"Movimientos obtenidos (pág 1): {len(movements)} de {total}")
    
    # Cargar productos
    products = controller.get_products()
    print(f"Productos cargados: {len(products)}")
    
    # Cargar usuarios
    users = controller.get_users()
    print(f"Usuarios cargados: {len(users)}")