# settings_controller.py
import json
import os
import logging
from datetime import datetime

class SettingsController:
    def __init__(self, config_file="config/db_config.json"):
        self.config_file = config_file
        self.config = {}

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        self.logger = logging.getLogger("SettingsController")
        self.load_settings()

    # -----------------------------
    # Cargar configuraciones
    # -----------------------------
    def load_settings(self):
        """Carga las configuraciones desde el JSON."""

        if not os.path.exists(self.config_file):
            self.logger.error(f"El archivo de configuración no existe: {self.config_file}")
            return

        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                self.config = json.load(file)

            self.logger.info(f"Configuraciones cargadas desde: {self.config_file}")

        except json.JSONDecodeError as e:
            self.logger.error(f"Error al leer JSON: {e}")
        except Exception as e:
            self.logger.error(f"Error inesperado al cargar configuraciones: {e}")

    # -----------------------------
    # Obtener configuraciones
    # -----------------------------
    def get_config(self, key_path):
        """Permite acceder a valores usando rutas tipo: database.host"""

        parts = key_path.split(".")
        data = self.config

        try:
            for key in parts:
                data = data[key]
            return data
        except Exception:
            return None

    # -----------------------------
    # Actualizar configuraciones
    # -----------------------------
    def update_config(self, key_path, value):
        parts = key_path.split(".")
        data = self.config

        try:
            for key in parts[:-1]:
                data = data[key]

            data[parts[-1]] = value

            self.logger.info(f"Actualizado: {key_path} = {value}")
            self.save_settings()

        except Exception as e:
            self.logger.error(f"Error al actualizar configuración: {e}")

    # -----------------------------
    # Guardar configuraciones
    # -----------------------------
    def save_settings(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as file:
                json.dump(self.config, file, indent=4, ensure_ascii=False)

            self.logger.info(f"Configuraciones guardadas en: {self.config_file}")

        except Exception as e:
            self.logger.error(f"Error al guardar configuraciones: {e}")

    # -----------------------------
    # Validación de BD
    # -----------------------------
    def validate_database_config(self):
        """
        Valida que la sección database tenga los campos necesarios.
        Permite password vacío ("").
        """

        if "database" not in self.config:
            return False, "La sección 'database' no existe."

        db = self.config["database"]

        campos_requeridos = ["host", "user", "port", "charset"]

        for campo in campos_requeridos:
            if campo not in db:
                return False, f"Falta el campo requerido: {campo}"

        # Password vacío es válido → NO marca error
        if "password" not in db:
            return False, "Falta el campo 'password' (aunque sea vacío)."

        return True, "OK"

    # -----------------------------
    # Backup de configuración
    # -----------------------------
    def create_backup(self):
        try:
            backup_dir = "exports/backups/"
            os.makedirs(backup_dir, exist_ok=True)

            filename = f"settings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            path = os.path.join(backup_dir, filename)

            with open(path, "w", encoding="utf-8") as file:
                json.dump(self.config, file, indent=4, ensure_ascii=False)

            self.logger.info(f"Backup creado: {path}")
            return path

        except Exception as e:
            self.logger.error(f"Error al crear backup: {e}")
            return None


# -----------------------------
# Pruebas rápidas (si ejecutas el archivo)
# -----------------------------
if __name__ == "__main__":
    controller = SettingsController()

    print("Configuraciones cargadas:", controller.config)

    print("Host de BD:", controller.get_config("database.host"))

    controller.update_config("application.company_name", "Mi Empresa")

    valid, msg = controller.validate_database_config()
    print("Validación BD:", valid, msg)

    backup = controller.create_backup()
    print("Backup creado en:", backup)
