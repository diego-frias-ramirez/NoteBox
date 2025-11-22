"""
NoteBox - Vista del Módulo de Usuarios
Ubicación: view/users_view.py
"""

import customtkinter as ctk
from components.base_view import BaseView
# Opcional: Importar modelos si los necesitas para esta vista
# from model.user_model import UserModel

class UsuariosView(BaseView):
    """Vista del Módulo de Usuarios."""

    def __init__(self, user_data):
        super().__init__(
            user_data=user_data,
            page_id="usuarios", # Este ID debe coincidir con el del sidebar
            page_title="Gestión de Usuarios",
            page_subtitle="Administrar cuentas de acceso al sistema"
        )
        # Opcional: Instanciar modelos aquí si es necesario
        # self.user_model = UserModel()

    def create_content(self):
        """Crea el contenido específico del módulo de usuarios."""
        # Aquí irá el código para crear la UI de usuarios
        # Por ejemplo: tabla de usuarios, formulario de edición/creación, etc.
        
        # Mensaje temporal
        label = ctk.CTkLabel(
            self.content_frame,
            text="Módulo de Usuarios - Contenido por implementar",
            font=ctk.CTkFont(size=16)
        )
        label.pack(expand=True)

if __name__ == "__main__":
    example_user = {"id": 1, "nombre": "Admin", "rol": "Admin"}
    app = UsuariosView(example_user)
    app.run()