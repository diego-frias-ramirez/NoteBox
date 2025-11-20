"""
NoteBox - Controlador de Login
"""

from model.user_model import UserModel
from model.database import Database
from utils.logger import Logger
from utils.alerts import Alerts

class LoginController:
    """Controlador para manejar el inicio de sesión"""
    
    def __init__(self):
        self.current_user = None
        self.is_authenticated = False
    
    def validate_credentials(self, username, password):
        """
        Valida las credenciales del usuario
        
        Returns:
            tuple: (success: bool, message: str, user_data: dict)
        """
        try:
            # Validar campos no vacíos
            if not username or not password:
                return False, "Por favor ingrese usuario y contraseña", None
            
            # Buscar usuario en la base de datos
            user_data = UserModel.authenticate(username, password)
            
            if user_data:
                # Verificar estado del usuario
                if user_data['estado'] != 'Activo':
                    Logger.log_user_action(
                        "Intento de login con usuario inactivo", 
                        username
                    )
                    return False, "Usuario inactivo. Contacte al administrador", None
                
                # Login exitoso
                self.current_user = user_data
                self.is_authenticated = True
                
                # Actualizar último acceso
                UserModel.update_last_access(user_data['id'])
                
                Logger.log_user_action(
                    "Inicio de sesión exitoso", 
                    f"{username} ({user_data['rol']})"
                )
                
                return True, "Inicio de sesión exitoso", user_data
            else:
                Logger.log_user_action(
                    "Intento de inicio de sesión fallido - Credenciales incorrectas", 
                    username
                )
                return False, "Usuario o contraseña incorrectos", None
                
        except Exception as e:
            Logger.error_exception(e, "LOGIN_CONTROLLER")
            return False, "Error al validar credenciales. Intente nuevamente", None
    
    def logout(self):
        """Cierra la sesión del usuario"""
        if self.current_user:
            Logger.log_user_action(
                "Cierre de sesión", 
                self.current_user['usuario']
            )
        
        self.current_user = None
        self.is_authenticated = False
        return True
    
    def get_current_user(self):
        """Obtiene el usuario actual"""
        return self.current_user
    
    def is_logged_in(self):
        """Verifica si hay un usuario autenticado"""
        return self.is_authenticated
    
    def is_admin(self):
        """Verifica si el usuario actual es administrador"""
        if self.current_user:
            return self.current_user['rol'] == 'Admin'
        return False
    
    def test_database_connection(self):
        """Prueba la conexión a la base de datos"""
        try:
            success = Database.test_connection()
            if success:
                Logger.success("Test de conexión exitoso", "LOGIN_CONTROLLER")
            else:
                Logger.error("Test de conexión fallido", "LOGIN_CONTROLLER")
            return success
        except Exception as e:
            Logger.error_exception(e, "LOGIN_CONTROLLER")
            return False
    
    def get_user_permissions(self):
        """
        Obtiene los permisos del usuario actual
        En v1.0 solo diferenciamos Admin y Empleado
        """
        if not self.current_user:
            return {
                'can_add_products': False,
                'can_edit_products': False,
                'can_delete_products': False,
                'can_manage_users': False,
                'can_view_reports': False,
                'can_manage_settings': False
            }
        
        is_admin = self.current_user['rol'] == 'Admin'
        
        return {
            'can_add_products': True,  # Todos pueden agregar
            'can_edit_products': True,  # Todos pueden editar
            'can_delete_products': is_admin,  # Solo admin puede eliminar
            'can_manage_users': is_admin,  # Solo admin
            'can_view_reports': True,  # Todos pueden ver reportes
            'can_manage_settings': is_admin  # Solo admin
        }