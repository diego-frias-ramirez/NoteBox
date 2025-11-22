"""
NoteBox - Vista del Módulo de Ayuda
Ubicación: view/help_view.py
"""

import customtkinter as ctk
from components.base_view import BaseView

class AyudaView(BaseView):
    """Vista del Módulo de Ayuda."""

    def __init__(self, user_data):
        super().__init__(
            user_data=user_data,
            page_id="ayuda", # Este ID debe coincidir con el del sidebar
            page_title="Centro de Ayuda",
            page_subtitle="Manuales, tutoriales y soporte"
        )

    def create_content(self):
        """Crea el contenido específico del módulo de ayuda."""
        # Aquí irá el código para crear la UI de ayuda
        # Por ejemplo: vista de manual de usuario, contacto, etc.
        
        # Mensaje temporal
        label = ctk.CTkLabel(
            self.content_frame,
            text="Módulo de Ayuda - Contenido por implementar",
            font=ctk.CTkFont(size=16)
        )
        label.pack(expand=True)

if __name__ == "__main__":
    example_user = {"id": 1, "nombre": "Admin", "rol": "Admin"}
    app = AyudaView(example_user)
    app.run()