"""
NoteBox - Vista del Módulo de Ayuda (Corregida y Optimizada)
Ubicación: view/help_view.py
"""

import customtkinter as ctk
from PIL import Image
import os
import webbrowser
import subprocess
import sys

from components.base_view import BaseView
from utils.logger import Logger
from utils.helpers import Helpers

class HelpView(BaseView):
    """Vista del Módulo de Ayuda."""

    def __init__(self, user_data):
        # Rutas y referencias para íconos
        self.images = {}
        self.icon_refs = {}

        # Llamar al constructor de la clase base
        super().__init__(
            user_data=user_data,
            page_id="ayuda",
            page_title="Centro de Ayuda",
            page_subtitle="Manuales, soporte y guías de usuario"
        )

    def create_content(self):
        """Crea el contenido específico del módulo de ayuda."""
        # El content_frame ya viene de BaseView y tiene scroll.
        # No necesitamos crear otro scrollable frame aquí.
        parent_frame = self.content_frame

        # Título principal
        title_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))

        # Icono de ayuda
        help_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "help.png")
        try:
            img = Image.open(help_icon_path)
            img = img.resize((48, 48), Image.LANCZOS)
            self.images["help_icon"] = ctk.CTkImage(light_image=img, dark_image=img, size=(48, 48))
            ctk.CTkLabel(title_frame, image=self.images["help_icon"], text="").pack(side="left", padx=(0, 15))
        except Exception as e:
            Logger.warning(f"No se pudo cargar el ícono de ayuda: {e}", "HELP_VIEW")

        title_label = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_label.pack(side="left", fill="y")

        ctk.CTkLabel(
            title_label,
            text="Centro de Ayuda de NoteBox",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_label,
            text="Encuentra manuales, guías y soporte técnico para usar el sistema.",
            font=ctk.CTkFont(size=14),
            text_color="#6c757d"
        ).pack(anchor="w", pady=(5, 0))

        # Contenido principal en un solo frame para aprovechar el scroll de BaseView
        main_container = ctk.CTkFrame(parent_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # Configurar el grid para las dos columnas
        main_container.grid_columnconfigure(1, weight=1)  # La columna derecha se expande

        # Columna Izquierda: Secciones de ayuda
        left_column = ctk.CTkFrame(main_container, fg_color="transparent", width=350)
        left_column.grid(row=0, column=0, sticky="nsw", padx=(0, 20), pady=(0, 20))
        left_column.grid_propagate(False)

        # Tarjetas de secciones
        self.create_help_section(
            left_column,
            "📘 Manual de Usuario",
            "Guía paso a paso para usar NoteBox.",
            self.show_user_manual
        )

        self.create_help_section(
            left_column,
            "🛠️ Soporte Técnico",
            "Reporta errores o problemas del sistema.",
            self.show_support_info
        )

        self.create_help_section(
            left_column,
            "📞 Contacto con Papelería Valeria",
            "Información de contacto del negocio.",
            self.show_contact_info
        )

        self.create_help_section(
            left_column,
            "ℹ️ Acerca de NoteBox",
            "Información sobre el proyecto y la versión.",
            self.show_about
        )

        # Columna Derecha: Contenido detallado
        right_column = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=12)
        right_column.grid(row=0, column=1, sticky="nsew", pady=(0, 20))
        right_column.grid_propagate(False)

        # Área de contenido detallado DENTRO de right_column
        self.detail_area = ctk.CTkFrame(right_column, fg_color="transparent")
        self.detail_area.pack(fill="both", expand=True, padx=30, pady=30)

        # Mostrar contenido inicial (Manual de Usuario)
        self.show_user_manual()

    def create_help_section(self, parent, title, description, command):
        """Crea una tarjeta de sección de ayuda."""
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=10, height=100)
        section.pack(fill="x", pady=10)
        section.pack_propagate(False)

        inner = ctk.CTkFrame(section, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(
            inner,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))

        section.bind("<Button-1>", lambda e: command())
        for child in inner.winfo_children():
            child.bind("<Button-1>", lambda e: command())

        # Hover effect
        def on_enter(e):
            section.configure(fg_color="#F0F9FF")
        def on_leave(e):
            section.configure(fg_color="#FFFFFF")

        section.bind("<Enter>", on_enter)
        section.bind("<Leave>", on_leave)
        for child in inner.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    def clear_detail_area(self):
        """Limpia el área de contenido detallado."""
        for widget in self.detail_area.winfo_children():
            widget.destroy()

    def show_user_manual(self):
        """Muestra el contenido del Manual de Usuario."""
        self.clear_detail_area()

        # Título
        ctk.CTkLabel(
            self.detail_area,
            text="📘 Manual de Usuario",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 15))

        # Secciones del manual
        sections = [
            ("1. Inicio de Sesión", "Ingrese con su usuario y contraseña asignados por el administrador."),
            ("2. Dashboard", "Visualice un resumen de su inventario, alertas y métricas clave."),
            ("3. Gestión de Inventario", "Agregue, edite o elimine productos. Use la búsqueda y filtros para encontrar rápidamente artículos."),
            ("4. Movimientos de Inventario", "Registre entradas (compras) y salidas (ventas) de productos. El stock se actualizará automáticamente."),
            ("5. Alertas", "Reciba notificaciones automáticas cuando el stock de un producto sea bajo."),
            ("6. Cierre de Sesión", "Haga clic en 'Cerrar Sesión' en la barra lateral para salir de forma segura."),
        ]

        for title, desc in sections:
            section_frame = ctk.CTkFrame(self.detail_area, fg_color="transparent")
            section_frame.pack(fill="x", pady=(0, 15))

            ctk.CTkLabel(
                section_frame,
                text=title,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#2b2d42",
                anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                section_frame,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color="#6c757d",
                anchor="w",
                wraplength=500, # Ajustado al ancho de la columna
                justify="left"
            ).pack(anchor="w", pady=(5, 0))

        # Botón de acción
        ctk.CTkButton(
            self.detail_area,
            text="Ver Manual",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#00B4D8",
            text_color="#FFFFFF",
            hover_color="#0096B4",
            corner_radius=8,
            height=40,
            command=self.open_user_manual
        ).pack(pady=(20, 0))

    def show_support_info(self):
        """Muestra la información de soporte técnico."""
        self.clear_detail_area()

        ctk.CTkLabel(
            self.detail_area,
            text="🛠️ Soporte Técnico",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 15))

        ctk.CTkLabel(
            self.detail_area,
            text="¿Encontraste un error o tienes un problema con el sistema?",
            font=ctk.CTkFont(size=14),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w", pady=(0, 10))

        # Información de contacto
        contact_frame = ctk.CTkFrame(self.detail_area, fg_color="#F0F9FF", corner_radius=10)
        contact_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            contact_frame,
            text="📧 Correo de Soporte:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#0AB7F3",
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(10, 0))

        ctk.CTkLabel(
            contact_frame,
            text="soporte.notebox@example.com",
            font=ctk.CTkFont(size=13),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        ctk.CTkLabel(
            contact_frame,
            text="📱 WhatsApp:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#0AB7F3",
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(10, 0))

        ctk.CTkLabel(
            contact_frame,
            text="+52 618 XXX XXXX",
            font=ctk.CTkFont(size=13),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(0, 15))

        ctk.CTkLabel(
            self.detail_area,
            text="Por favor, incluya en su mensaje:\n- Su nombre de usuario\n- Una descripción clara del problema\n- Capturas de pantalla si es posible",
            font=ctk.CTkFont(size=12),
            text_color="#6c757d",
            anchor="w",
            justify="left"
        ).pack(anchor="w", pady=(10, 0))

    def show_contact_info(self):
        """Muestra la información de contacto con Papelería Valeria."""
        self.clear_detail_area()

        ctk.CTkLabel(
            self.detail_area,
            text="📞 Contacto con Papelería Valeria",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 15))

        info_text = (
            "Papelería Valeria\n"
            "📍 Dirección: Durango, México\n"
            "📞 Teléfono: +52 618 000 0000\n"
            "✉️ Email: contacto@papeleriavaleria.com\n\n"
            "Horarios de Atención:\n"
            "Lunes a Viernes: 9:00 AM - 7:00 PM\n"
            "Sábados: 10:00 AM - 3:00 PM\n"
            "Domingos: Cerrado"
        )

        ctk.CTkLabel(
            self.detail_area,
            text=info_text,
            font=ctk.CTkFont(size=14),
            text_color="#2b2d42",
            anchor="w",
            justify="left"
        ).pack(anchor="w", pady=(0, 15))

    def show_about(self):
        """Muestra información sobre el proyecto NoteBox."""
        self.clear_detail_area()

        ctk.CTkLabel(
            self.detail_area,
            text="ℹ️ Acerca de NoteBox",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 15))

        about_text = (
            "NoteBox es un sistema de gestión de inventario diseñado específicamente para la Papelería Valeria.\n\n"
            "Desarrollado por estudiantes de la Universidad Tecnológica de Durango como parte del Proyecto Integrador I.\n\n"
            "Versión: v1.0.0\n"
            "Fecha de lanzamiento: Noviembre 2025\n"
            "Tecnologías: Python, Tkinter, MySQL\n\n"
            "Este sistema busca modernizar y optimizar los procesos de control de inventario, reemplazando los métodos manuales por una solución tecnológica accesible y eficiente."
        )

        ctk.CTkLabel(
            self.detail_area,
            text=about_text,
            font=ctk.CTkFont(size=13),
            text_color="#2b2d42",
            anchor="w",
            justify="left",
            wraplength=500
        ).pack(anchor="w", pady=(0, 15))

        # Enlace al repositorio (simulado)
        def open_repo():
            webbrowser.open("https://github.com/diego-frias-ramirez/NoteBox")

        ctk.CTkButton(
            self.detail_area,
            text="Ver Código en GitHub",
            font=ctk.CTkFont(size=13),
            fg_color="#E0F7FA",
            text_color="#00B4D8",
            hover_color="#B2EBF2",
            corner_radius=8,
            height=35,
            command=open_repo
        ).pack(pady=(10, 0))

    def open_user_manual(self):
        """Abre el archivo PDF del manual de usuario."""
        try:
            # Ruta del PDF en la carpeta docs
            pdf_path = os.path.join(self.base_path, "..", "docs", "Manual de usuario.pdf")
            
            # Obtener la ruta absoluta
            pdf_path = os.path.abspath(pdf_path)
            
            # Verificar si el archivo existe
            if not os.path.exists(pdf_path):
                from tkinter import messagebox
                messagebox.showerror("Error", f"No se encontró el archivo: {pdf_path}")
                return
            
            # Abrir el PDF según el sistema operativo
            if sys.platform == "win32":
                # Windows
                os.startfile(pdf_path)
            elif sys.platform == "darwin":
                # macOS
                subprocess.run(["open", pdf_path])
            else:
                # Linux
                subprocess.run(["xdg-open", pdf_path])
                
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudo abrir el manual: {str(e)}")
            Logger.error(f"Error al abrir el manual: {e}", "HELP_VIEW")

if __name__ == "__main__":
    # Ejemplo para pruebas
    example_user = {"id": 1, "nombre": "Admin", "rol": "Admin"}
    app = HelpView(example_user)
    app.run()