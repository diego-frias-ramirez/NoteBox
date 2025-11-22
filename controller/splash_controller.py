"""
NoteBox - Controlador del Splash Screen (CORREGIDO)
"""

import os
import json
import time
from model.database import Database
from model.settings_model import SettingsModel
from utils.logger import Logger
from utils.helpers import Helpers

class SplashScreenController:
    """Controlador para gestionar la carga inicial de la aplicación."""

    def __init__(self):
        self.progress = 0
        self.steps = [
            ("Verificando conexión a la base de datos...", self.check_database),
            ("Verificando archivos y carpetas del sistema...", self.check_directories),
            ("Cargando configuración del sistema...", self.load_settings),
            ("Verificando sesión anterior...", self.check_session),
            ("Pre-cargando datos iniciales...", self.preload_data)
        ]
        self.current_step = 0
        self.total_steps = len(self.steps)
        self.has_session = False  # Para saber si ir al dashboard o login

    def check_database(self):
        """Verifica la conexión a la base de datos y crea las tablas si no existen."""
        try:
            if not Database.test_connection():
                raise Exception("No se pudo conectar a la base de datos")
            
            if not Database.init_database():
                raise Exception("No se pudo inicializar la base de datos")
            
            Logger.success("Conexión a la base de datos establecida y tablas verificadas.", "SPLASH")
            return True
        except Exception as e:
            Logger.error(f"Error en la verificación de la base de datos: {e}", "SPLASH")
            return False

    def check_directories(self):
        """Verifica y crea las carpetas necesarias si no existen."""
        try:
            paths = SettingsModel.load_paths()
            if not paths:
                raise Exception("No se pudo cargar la configuración de rutas")
            
            for folder_path in [paths['logs_dir'], paths['exports']['reports'], paths['exports']['backups']]:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    Logger.info(f"Carpeta creada: {folder_path}", "SPLASH")
            
            Logger.success("Carpetas del sistema verificadas y creadas si era necesario.", "SPLASH")
            return True
        except Exception as e:
            Logger.error(f"Error en la verificación de directorios: {e}", "SPLASH")
            return False

    def load_settings(self):
        """Carga la configuración del sistema."""
        try:
            app_settings = SettingsModel.load_app_settings()
            if not app_settings:
                raise Exception("No se pudo cargar la configuración de la aplicación")
            
            db_config = SettingsModel.load_db_config()
            if not db_config:
                raise Exception("No se pudo cargar la configuración de la base de datos")
            
            Logger.success("Configuración del sistema cargada correctamente.", "SPLASH")
            return True
        except Exception as e:
            Logger.error(f"Error en la carga de configuración: {e}", "SPLASH")
            return False

    def check_session(self):
        """Verifica si hay una sesión guardada. SIEMPRE retorna True (el paso fue exitoso)."""
        try:
            session_file = os.path.join(os.path.dirname(__file__), '..', 'temp', 'session.json')
            
            if os.path.exists(session_file):
                # Leer y validar sesión
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                # Verificar que la sesión no haya expirado (opcional)
                self.has_session = True
                Logger.info("Sesión guardada encontrada.", "SPLASH")
            else:
                self.has_session = False
                Logger.info("No hay sesión guardada.", "SPLASH")
            
            # IMPORTANTE: Retornar True porque el paso se ejecutó correctamente
            # (encontrar o no sesión no es un error)
            return True
            
        except Exception as e:
            Logger.error(f"Error en la verificación de sesión: {e}", "SPLASH")
            self.has_session = False
            return True  # Aún así continuar, ir al login

    def preload_data(self):
        """Pre-carga datos iniciales como alertas de stock bajo."""
        try:
            from model.report_model import ReportModel
            low_stock_products = ReportModel.get_low_stock_products()
            Logger.info(f"Datos iniciales pre-cargados: {len(low_stock_products)} productos con stock bajo.", "SPLASH")
            Logger.success("Sistema listo para iniciar.", "SPLASH")
            return True
        except Exception as e:
            Logger.warning(f"Advertencia en pre-carga de datos: {e}", "SPLASH")
            # No es crítico, continuar de todos modos
            return True

    def get_progress(self):
        """Obtiene el progreso actual."""
        return self.progress

    def next_step(self):
        """Avanza al siguiente paso."""
        if self.current_step < self.total_steps:
            step_name, step_func = self.steps[self.current_step]
            Logger.info(f"Ejecutando paso: {step_name}", "SPLASH")
            
            success = step_func()
            if success:
                self.current_step += 1
                self.progress = int((self.current_step / self.total_steps) * 100)
                return True
            else:
                return False
        return True  # Ya completó todos los pasos

    def is_complete(self):
        """Verifica si todos los pasos han sido completados."""
        return self.current_step >= self.total_steps

    def should_go_to_dashboard(self):
        """Determina si se debe ir directamente al dashboard."""
        return self.has_session