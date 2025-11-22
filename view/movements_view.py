"""
NoteBox - Vista del Módulo de Movimientos
Ubicación: view/movements_view.py
"""

import customtkinter as ctk
from components.base_view import BaseView
# Opcional: Importar modelos si los necesitas para esta vista
# from model.movement_model import MovementModel

class MovimientosView(BaseView):
    """Vista del Módulo de Movimientos."""

    def __init__(self, user_data):
        super().__init__(
            user_data=user_data,
            page_id="movimientos", # Este ID debe coincidir con el del sidebar
            page_title="Control de Movimientos",
            page_subtitle="Registrar entradas y salidas de productos"
        )
        # Opcional: Instanciar modelos aquí si es necesario
        # self.movement_model = MovementModel()

    def create_content(self):
        """Crea el contenido específico del módulo de movimientos."""
        # Aquí irá el código para crear la UI de movimientos
        # Por ejemplo: formulario para registrar movimientos, historial, etc.
        
        # Mensaje temporal
        label = ctk.CTkLabel(
            self.content_frame,
            text="Módulo de Movimientos - Contenido por implementar",
            font=ctk.CTkFont(size=16)
        )
        label.pack(expand=True)

if __name__ == "__main__":
    example_user = {"id": 1, "nombre": "Admin", "rol": "Admin"}
    app = MovimientosView(example_user)
    app.run()