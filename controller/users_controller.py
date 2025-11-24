"""
NoteBox - Controlador del Módulo de Usuarios
Responsabilidad: Gestionar la lógica del módulo de usuarios, conectar vista y modelo.
Ubicación: controller/users_controller.py
"""

import os
import sys

# Asegurar que el módulo 'controller' esté en el path para imports relativos
controller_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(controller_path)

from model.user_model import UserModel
from utils.logger import Logger
from utils.validators import Validators
from datetime import datetime

class UsersController:
    """Controlador para gestionar la lógica del módulo de usuarios."""

    def __init__(self):
        self.user_model = UserModel()
        self.current_user = None # Se puede inicializar aquí o recibirlo en cada método

    def set_current_user(self, user_data):
        """Establece el usuario actual para auditoría."""
        self.current_user = user_data

    def get_users(self, page=None, search="", role_filter=None):
        """
        Obtiene usuarios con paginación y filtros.
        
        Args:
            page (int): Número de página (opcional, usa self.current_page si no se pasa).
            search (str): Término de búsqueda.
            role_filter (str): Filtro por rol ('Admin', 'Empleado').
        
        Returns:
            tuple: (lista de usuarios, total de usuarios).
        """
        try:
            current_page = page if page is not None else 1
            offset = (current_page - 1) * 5 # Usamos 5 usuarios por página como en el diseño

            users = self.user_model.get_users(
                search=search,
                role=role_filter,
                limit=5,
                offset=offset
            )
            total = self.user_model.get_total_users(search=search, role=role_filter)
            
            Logger.info(f"Usuarios obtenidos: {len(users)}, Total: {total}", "USERS_CONTROLLER")
            return users, total
        except Exception as e:
            Logger.log_error_exception(e, "USERS_CONTROLLER")
            return [], 0

    def create_user(self, data):
        """
        Crea un nuevo usuario.
        
        Args:
            data (dict): Datos del usuario {nombre, email, rol, password}.
        
        Returns:
            tuple: (bool: éxito, str: mensaje o dict: usuario creado).
        """
        # Validar datos de entrada
        is_valid, msg = Validators.validate_user_data(data)
        if not is_valid:
            Logger.warning(f"Validación fallida en creación: {msg}", "USERS_CONTROLLER")
            return False, msg
        
        try:
            user_id = self.user_model.create_user(**data)
            if user_id:
                Logger.success(f"Usuario '{data['nombre']}' creado con ID {user_id}", "USERS_CONTROLLER")
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action("CREAR_USUARIO", self.current_user['nombre'], details=f"ID: {user_id}, Nombre: {data['nombre']}")
                # Devolver el usuario recién creado para actualizar la vista
                created_user = self.get_user_by_id(user_id)
                return True, created_user
            else:
                error_msg = "No se pudo crear el usuario en la base de datos"
                Logger.error(error_msg, "USERS_CONTROLLER")
                return False, error_msg
        except Exception as e:
            Logger.log_error_exception(e, "USERS_CONTROLLER")
            return False, str(e)

    def update_user(self, user_id, data):
        """
        Actualiza un usuario existente.
        
        Args:
            user_id (int): ID del usuario.
            data (dict): Datos a actualizar.
        
        Returns:
            tuple: (bool: éxito, str: mensaje).
        """
        # Validar datos de entrada
        is_valid, msg = Validators.validate_user_data(data, update=True)
        if not is_valid:
            Logger.warning(f"Validación fallida en actualización: {msg}", "USERS_CONTROLLER")
            return False, msg
        
        try:
            success = self.user_model.update_user(user_id, **data)
            if success:
                Logger.success(f"Usuario ID {user_id} actualizado", "USERS_CONTROLLER")
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action("ACTUALIZAR_USUARIO", self.current_user['nombre'], details=f"ID: {user_id}")
                
                # Devolver el usuario actualizado para actualizar la vista
                updated_user = self.get_user_by_id(user_id)
                return True, updated_user
            else:
                error_msg = f"No se pudo actualizar el usuario ID {user_id}"
                Logger.error(error_msg, "USERS_CONTROLLER")
                return False, error_msg
        except Exception as e:
            Logger.log_error_exception(e, "USERS_CONTROLLER")
            return False, str(e)

    def delete_user(self, user_id):
        """
        Elimina (desactiva) un usuario.
        
        Args:
            user_id (int): ID del usuario.
        
        Returns:
            tuple: (bool: éxito, str: mensaje).
        """
        try:
            success = self.user_model.deactivate_user(user_id) # Asumiendo que tienes este método
            if success:
                Logger.success(f"Usuario ID {user_id} eliminado (desactivado)", "USERS_CONTROLLER")
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action("ELIMINAR_USUARIO", self.current_user['nombre'], details=f"ID: {user_id}")
                return True, "Usuario eliminado correctamente"
            else:
                error_msg = f"No se pudo eliminar el usuario ID {user_id}"
                Logger.error(error_msg, "USERS_CONTROLLER")
                return False, error_msg
        except Exception as e:
            Logger.log_error_exception(e, "USERS_CONTROLLER")
            return False, str(e)

    def change_user_status(self, user_id, new_status):
        """
        Cambia el estado de un usuario (Activo/Inactivo).
        
        Args:
            user_id (int): ID del usuario.
            new_status (bool): Nuevo estado (True = Activo, False = Inactivo).
        
        Returns:
            tuple: (bool: éxito, str: mensaje).
        """
        try:
            success = self.user_model.change_user_status(user_id, new_status)
            if success:
                status_str = "Activo" if new_status else "Inactivo"
                Logger.success(f"Estado del usuario ID {user_id} cambiado a {status_str}", "USERS_CONTROLLER")
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action("CAMBIAR_ESTADO_USUARIO", self.current_user['nombre'], details=f"ID: {user_id}, Estado: {status_str}")
                return True, f"Estado del usuario actualizado a {status_str}"
            else:
                error_msg = f"No se pudo cambiar el estado del usuario ID {user_id}"
                Logger.error(error_msg, "USERS_CONTROLLER")
                return False, error_msg
        except Exception as e:
            Logger.log_error_exception(e, "USERS_CONTROLLER")
            return False, str(e)

    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID."""
        try:
            user = self.user_model.get_user_by_id(user_id)
            if user:
                Logger.info(f"Usuario ID {user_id} obtenido", "USERS_CONTROLLER")
            else:
                Logger.warning(f"Usuario ID {user_id} no encontrado", "USERS_CONTROLLER")
            return user
        except Exception as e:
            Logger.log_error_exception(e, "USERS_CONTROLLER")
            return None

    def get_user_roles(self):
        """Obtiene los roles disponibles para asignar a usuarios."""
        try:
            roles = [
                {"id": "admin", "name": "Administrador", "description": "Acceso completo al sistema"},
                {"id": "empleado", "name": "Empleado", "description": "Acceso limitado según permisos"}
            ]
            Logger.info(f"Roles obtenidos: {len(roles)}", "USERS_CONTROLLER")
            return roles
        except Exception as e:
            Logger.log_error_exception(e, "USERS_CONTROLLER")
            return []

    def get_users_summary(self):
        """Obtiene un resumen de usuarios por rol."""
        try:
            summary = {
                "admin": self.user_model.get_users_count_by_role("admin"),
                "empleado": self.user_model.get_users_count_by_role("empleado"),
                "total": self.user_model.get_total_users()
            }
            Logger.info(f"Resumen de usuarios: {summary}", "USERS_CONTROLLER")
            return summary
        except Exception as e:
            Logger.log_error_exception(e, "USERS_CONTROLLER")
            return {"admin": 0, "empleado": 0, "total": 0}

