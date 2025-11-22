"""
NoteBox - Vista del Módulo de Configuración
Ubicación: view/settings_view.py
"""

import customtkinter as ctk
from components.base_view import BaseView
# Opcional: Importar modelos si los necesitas para esta vista
# from model.settings_model import SettingsModel

class ConfiguracionView(BaseView):
    """Vista del Módulo de Configuración."""

    def __init__(self, user_data):
        super().__init__(
            user_data=user_data,
            page_id="configuracion", # Este ID debe coincidir con el del sidebar
            page_title="Configuración del Sistema",
            page_subtitle="Personalizar ajustes de la aplicación"
        )
        # Opcional: Instanciar modelos aquí si es necesario
        # self.settings_model = SettingsModel()

    def create_content(self):
        """Crea el contenido específico del módulo de configuración."""
        # Aquí irá el código para crear la UI de configuración
        # Por ejemplo: formularios para cambiar colores, moneda, backups, etc.
        
        # Mensaje temporal
        label = ctk.CTkLabel(
            self.content_frame,
            text="Módulo de Configuración - Contenido por implementar",
            font=ctk.CTkFont(size=16)
        )
        label.pack(expand=True)

if __name__ == "__main__":
    example_user = {"id": 1, "nombre": "Admin", "rol": "Admin"}
    app = ConfiguracionView(example_user)
    app.run()