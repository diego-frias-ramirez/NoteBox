"""
NoteBox - Sistema de Gestión de Inventario
Sistema de registro de logs
"""

import os
import json
from datetime import datetime

class Logger:
    """Clase para registrar eventos y errores del sistema"""
    
    # Obtener la ruta absoluta del directorio actual (donde está logger.py)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta absoluta al archivo paths.json
    PATHS_FILE = os.path.join(CURRENT_DIR, '..', 'config', 'paths.json')
    
    # Cargar rutas desde paths.json
    try:
        with open(PATHS_FILE, 'r', encoding='utf-8') as f:
            paths = json.load(f)
            LOG_DIR = paths['logs']['app_log']
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {PATHS_FILE}")
        LOG_DIR = "../logs/app.log"  # Fallback
    except json.JSONDecodeError:
        print(f"Error: El archivo {PATHS_FILE} no tiene un formato JSON válido.")
        LOG_DIR = "../logs/app.log"  # Fallback
    
    # Tipos de log
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    SUCCESS = "SUCCESS"
    
    @staticmethod
    def _ensure_log_dir():
        """Asegura que el directorio de logs exista"""
        if not os.path.exists(os.path.dirname(Logger.LOG_DIR)):
            os.makedirs(os.path.dirname(Logger.LOG_DIR))
    
    @staticmethod
    def _get_log_filename():
        """Genera el nombre del archivo de log basado en la fecha actual"""
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(os.path.dirname(Logger.LOG_DIR), f"notebox_{today}.log")
    
    @staticmethod
    def _format_message(level, message, module=None):
        """Formatea el mensaje de log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        module_str = f"[{module}]" if module else ""
        return f"[{timestamp}] [{level}] {module_str} {message}\n"
    
    @staticmethod
    def log(level, message, module=None, print_console=True):
        """Registra un mensaje en el log"""
        try:
            Logger._ensure_log_dir()
            
            formatted_message = Logger._format_message(level, message, module)
            
            # Escribir en archivo
            log_file = Logger._get_log_filename()
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_message)
            
            # Imprimir en consola si se especifica
            if print_console:
                print(formatted_message.strip())
            
            return True
        except Exception as e:
            print(f"Error al escribir log: {e}")
            return False
    
    @staticmethod
    def info(message, module=None):
        """Registra un mensaje de información"""
        return Logger.log(Logger.INFO, message, module)
    
    @staticmethod
    def warning(message, module=None):
        """Registra una advertencia"""
        return Logger.log(Logger.WARNING, message, module)
    
    @staticmethod
    def error(message, module=None):
        """Registra un error"""
        return Logger.log(Logger.ERROR, message, module)
    
    @staticmethod
    def debug(message, module=None):
        """Registra un mensaje de debug"""
        return Logger.log(Logger.DEBUG, message, module)
    
    @staticmethod
    def success(message, module=None):
        """Registra un mensaje de éxito"""
        return Logger.log(Logger.SUCCESS, message, module)
    
    @staticmethod
    def log_database_operation(operation, table, success=True, details=None):
        """Registra operaciones de base de datos"""
        status = "EXITOSA" if success else "FALLIDA"
        message = f"Operación BD {status}: {operation} en tabla '{table}'"
        if details:
            message += f" - {details}"
        
        level = Logger.SUCCESS if success else Logger.ERROR
        return Logger.log(level, message, "DATABASE")
    
    @staticmethod
    def log_user_action(action, user=None, details=None):
        """Registra acciones del usuario"""
        user_str = f"Usuario: {user}" if user else "Usuario: Sistema"
        message = f"{user_str} - Acción: {action}"
        if details:
            message += f" - {details}"
        
        return Logger.info(message, "USER_ACTION")
    
    @staticmethod
    def log_error_exception(exception, module=None):
        """Registra una excepción"""
        message = f"Excepción capturada: {type(exception).__name__} - {str(exception)}"
        return Logger.error(message, module)
    
    @staticmethod
    def clear_old_logs(days=30):
        """Elimina logs antiguos"""
        try:
            Logger._ensure_log_dir()
            
            current_time = datetime.now()
            deleted_count = 0
            
            for filename in os.listdir(os.path.dirname(Logger.LOG_DIR)):
                if filename.endswith('.log'):
                    filepath = os.path.join(os.path.dirname(Logger.LOG_DIR), filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    # Si el archivo tiene más de X días
                    if (current_time - file_time).days > days:
                        os.remove(filepath)
                        deleted_count += 1
            
            Logger.info(f"Limpieza de logs completada. {deleted_count} archivo(s) eliminado(s)", "MAINTENANCE")
            return True
        except Exception as e:
            Logger.error(f"Error al limpiar logs: {e}", "MAINTENANCE")
            return False