"""
NoteBox - Controlador del Login
"""

from model.user_model import UserModel
from utils.logger import Logger
from utils.validators import Validators

class LoginController:
    """Controlador para gestionar el login de usuarios."""
    
    def __init__(self):
        self.user_model = UserModel()
    
    def authenticate_user(self, username, password):
        """
        Autentica un usuario con sus credenciales.
        
        Args:
            username (str): Nombre de usuario
            password (str): Contraseña
        
        Returns:
            dict: Datos del usuario si es válido, None si no
        """
        # Validar entradas
        if not username or not password:
            Logger.warning("Intento de login sin usuario o contraseña", "LOGIN_CONTROLLER")
            return None
        
        # Validar formato de usuario
        is_valid, msg = Validators.validate_not_empty(username, "Usuario")
        if not is_valid:
            Logger.warning(f"Validación fallida: {msg}", "LOGIN_CONTROLLER")
            return None
        
        # Validar formato de contraseña
        is_valid, msg = Validators.validate_not_empty(password, "Contraseña")
        if not is_valid:
            Logger.warning(f"Validación fallida: {msg}", "LOGIN_CONTROLLER")
            return None
        
        # Autenticar con el modelo
        user_data = self.user_model.authenticate(username, password)
        
        if user_data:
            # Actualizar último acceso
            self.user_model.update_last_access(user_data['id'])
            Logger.log_user_action("LOGIN_EXITOSO", username)
            return user_data
        else:
            Logger.log_user_action("LOGIN_FALLIDO", username)
            return None
    
    def remember_user(self, username, remember):
        """
        Maneja la opción de recordar usuario.
        
        Args:
            username (str): Nombre de usuario
            remember (bool): Si se debe recordar el usuario
        """
        # Aquí puedes implementar la lógica para guardar el usuario en un archivo
        # o en una base de datos local para recordarlo
        if remember:
            # Guardar usuario en sesión
            Logger.info(f"Usuario {username} recordado", "LOGIN_CONTROLLER")
        else:
            # Limpiar sesión
            Logger.info(f"Usuario {username} no recordado", "LOGIN_CONTROLLER")