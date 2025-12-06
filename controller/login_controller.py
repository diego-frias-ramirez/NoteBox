import os
import json
from model.user_model import UserModel
from utils.logger import Logger
from utils.validators import Validators

class LoginController:
    """Controlador para gestionar el login de usuarios."""    
    def __init__(self):
        self.user_model = UserModel()
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Ruta de la carpeta logs
        self.logs_path = os.path.join(self.base_path, "..", "logs")
        os.makedirs(self.logs_path, exist_ok=True)  # Crear la carpeta si no existe

        # Ruta del archivo remember_user.json en logs
        self.remember_file = os.path.join(self.logs_path, "remember_user.json")
    
    def authenticate_user(self, username, password):
        """Autentica un usuario con sus credenciales."""        
        if not username or not password:
            Logger.warning("Intento de login sin usuario o contraseña", "LOGIN_CONTROLLER")
            return None
        
        is_valid, msg = Validators.validate_not_empty(username, "Usuario")
        if not is_valid:
            Logger.warning(f"Validación fallida: {msg}", "LOGIN_CONTROLLER")
            return None
        
        is_valid, msg = Validators.validate_not_empty(password, "Contraseña")
        if not is_valid:
            Logger.warning(f"Validación fallida: {msg}", "LOGIN_CONTROLLER")
            return None
        
        user_data = self.user_model.authenticate(username, password)
        
        if user_data and user_data.get('estado') == 'Activo':
            self.user_model.update_last_access(user_data['id'])
            Logger.log_user_action("LOGIN_EXITOSO", username)
            return user_data
        else:
            Logger.log_user_action("LOGIN_FALLIDO", username)
            return None
    
    def remember_user(self, username, remember):
        """Guarda o borra el usuario recordado según la opción."""        
        if remember:
            try:
                with open(self.remember_file, "w") as f:
                    json.dump({"username": username}, f)
                Logger.info(f"Usuario {username} recordado", "LOGIN_CONTROLLER")
            except Exception as e:
                Logger.error(f"No se pudo guardar usuario: {e}", "LOGIN_CONTROLLER")
        else:
            if os.path.exists(self.remember_file):
                try:
                    os.remove(self.remember_file)
                    Logger.info(f"Usuario {username} eliminado del recordado", "LOGIN_CONTROLLER")
                except Exception as e:
                    Logger.error(f"No se pudo eliminar usuario recordado: {e}", "LOGIN_CONTROLLER")

    def load_remembered_user(self):
        """Carga el usuario recordado si existe."""        
        if os.path.exists(self.remember_file):
            try:
                with open(self.remember_file, "r") as f:
                    data = json.load(f)
                    return data.get("username", "")
            except Exception as e:
                Logger.error(f"No se pudo cargar usuario recordado: {e}", "LOGIN_CONTROLLER")
        return ""
