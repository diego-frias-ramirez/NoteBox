"""
NoteBox - Vista del Módulo de Reportes
Ubicación: view/reports_view.py
"""

import customtkinter as ctk
from components.base_view import BaseView
# Opcional: Importar modelos si los necesitas para esta vista
# from model.report_model import ReportModel

class ReportesView(BaseView):
    """Vista del Módulo de Reportes."""

    def __init__(self, user_data):
        super().__init__(
            user_data=user_data,
            page_id="reportes", # Este ID debe coincidir con el del sidebar
            page_title="Generación de Reportes",
            page_subtitle="Visualizar y exportar información del inventario"
        )
        # Opcional: Instanciar modelos aquí si es necesario
        # self.report_model = ReportModel()

    def create_content(self):
        """Crea el contenido específico del módulo de reportes."""
        # Aquí irá el código para crear la UI de reportes
        # Por ejemplo: selector de reporte, vista previa, botón de exportar, etc.
        
        # Mensaje temporal
        label = ctk.CTkLabel(
            self.content_frame,
            text="Módulo de Reportes - Contenido por implementar",
            font=ctk.CTkFont(size=16)
        )
        label.pack(expand=True)

if __name__ == "__main__":
    example_user = {"id": 1, "nombre": "Admin", "rol": "Admin"}
    app = ReportesView(example_user)
    app.run()