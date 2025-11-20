"""
NoteBox - Modelo de Configuraciones del Sistema
"""

import json
from utils.logger import Logger

class SettingsModel:
    """Modelo para manejar configuraciones del sistema"""
    
    @staticmethod
    def load_app_settings():
        """Carga la configuración de la aplicación"""
        try:
            with open('config/app_settings.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            Logger.error_exception(e, "SETTINGS_MODEL")
            return None
    
    @staticmethod
    def load_db_config():
        """Carga la configuración de la base de datos"""
        try:
            with open('config/db_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            Logger.error_exception(e, "SETTINGS_MODEL")
            return None
    
    @staticmethod
    def load_paths():
        """Carga las rutas del sistema"""
        try:
            with open('config/paths.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            Logger.error_exception(e, "SETTINGS_MODEL")
            return None
    
    @staticmethod
    def save_app_settings(settings):
        """Guarda la configuración de la aplicación"""
        try:
            with open('config/app_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            Logger.success("Configuración guardada", "SETTINGS_MODEL")
            return True
        except Exception as e:
            Logger.error_exception(e, "SETTINGS_MODEL")
            return False