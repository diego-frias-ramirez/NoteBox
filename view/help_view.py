# view/help_view.py

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class HelpView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox - Centro de Ayuda")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.create_layout()
    
    def create_layout(self):
        # === SIDEBAR ===
        sidebar = ctk.CTkFrame(self.root, width=240, fg_color="white", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="white", height=80)
        logo_frame.pack(fill="x", pady=(20, 30))
        
        logo_icon = ctk.CTkLabel(logo_frame, text="📦", font=("Segoe UI Emoji", 24))
        logo_icon.pack(side="left", padx=(20, 10))
        
        logo_text_frame = ctk.CTkFrame(logo_frame, fg_color="white")
        logo_text_frame.pack(side="left")
        
        ctk.CTkLabel(
            logo_text_frame,
            text="NoteBox",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_text_frame,
            text="Admin Panel",
            font=("Arial", 10),
            text_color="#8d99ae",
            anchor="w"
        ).pack(anchor="w")
        
        # Buscador
        search_frame = ctk.CTkFrame(sidebar, fg_color="white", height=50)
        search_frame.pack(fill="x", padx=15, pady=(0, 20))
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar...",
            height=40,
            font=("Arial", 12),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        search_entry.pack(fill="x")
        
        # Menú
        menu_items = [
            ("📊", "Dashboard", False),
            ("📦", "Inventario", False),
            ("🔄", "Movimientos", False),
            ("📈", "Reportes", False),
            ("👥", "Usuarios", False),
            ("⚙️", "Configuración", False),
            ("❓", "Ayuda", True)
        ]
        
        for icon, text, active in menu_items:
            self.create_menu_item(sidebar, icon, text, active)
        
        # Usuario
        user_frame = ctk.CTkFrame(sidebar, fg_color="white")
        user_frame.pack(side="bottom", fill="x", pady=20, padx=15)
        
        user_avatar = ctk.CTkFrame(
            user_frame,
            fg_color="#2b2d42",
            corner_radius=20,
            width=40,
            height=40
        )
        user_avatar.pack(side="left", padx=(0, 10))
        user_avatar.pack_propagate(False)
        
        ctk.CTkLabel(
            user_avatar,
            text="👤",
            font=("Segoe UI Emoji", 18),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        user_info = ctk.CTkFrame(user_frame, fg_color="white")
        user_info.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            user_info,
            text="Admin User",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            user_info,
            text="Administrador",
            font=("Arial", 10),
            text_color="#8d99ae",
            anchor="w"
        ).pack(anchor="w")
        
        # === MAIN CONTENT ===
        main_container = ctk.CTkFrame(self.root, fg_color="#f8f9fa", corner_radius=0)
        main_container.pack(side="right", fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="white", height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_left = ctk.CTkFrame(header, fg_color="white")
        header_left.pack(side="left", padx=30, pady=15)
        
        ctk.CTkButton(
            header_left,
            text="☰",
            width=40,
            height=40,
            fg_color="transparent",
            text_color="#2b2d42",
            hover_color="#f8f9fa",
            font=("Arial", 20)
        ).pack(side="left", padx=(0, 20))
        
        header_text = ctk.CTkFrame(header_left, fg_color="white")
        header_text.pack(side="left")
        
        ctk.CTkLabel(
            header_text,
            text="Centro de Ayuda",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_text,
            text="Guías, tutoriales y documentación",
            font=("Arial", 12),
            text_color="#8d99ae",
            anchor="w"
        ).pack(anchor="w")
        
        # Notificación
        notif_btn = ctk.CTkButton(
            header,
            text="🔔",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#f8f9fa",
            font=("Segoe UI Emoji", 18),
            corner_radius=8
        )
        notif_btn.pack(side="right", padx=30)
        
        badge = ctk.CTkLabel(
            notif_btn,
            text="3",
            font=("Arial", 9, "bold"),
            text_color="white",
            fg_color="#ef233c",
            corner_radius=10,
            width=18,
            height=18
        )
        badge.place(relx=0.7, rely=0.2, anchor="center")
        
        # === CONTENT ===
        content = ctk.CTkScrollableFrame(main_container, fg_color="#f8f9fa")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # === BANNER DE BIENVENIDA ===
        welcome_banner = ctk.CTkFrame(content, fg_color="#00b4d8", corner_radius=12, height=140)
        welcome_banner.pack(fill="x", pady=(0, 30))
        welcome_banner.pack_propagate(False)
        
        banner_content = ctk.CTkFrame(welcome_banner, fg_color="transparent")
        banner_content.pack(fill="both", expand=True, padx=40, pady=30)
        
        banner_text = ctk.CTkFrame(banner_content, fg_color="transparent")
        banner_text.pack(side="left")
        
        ctk.CTkLabel(
            banner_text,
            text="👋 ¡Bienvenido al Centro de Ayuda!",
            font=("Arial", 28, "bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            banner_text,
            text="Encuentra respuestas rápidas y aprende a usar NoteBox al máximo",
            font=("Arial", 13),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(10, 0))
        
        ctk.CTkLabel(
            banner_content,
            text="📚",
            font=("Segoe UI Emoji", 70),
            text_color="white"
        ).pack(side="right", padx=30)
        
        # === BARRA DE BÚSQUEDA GRANDE ===
        search_container = ctk.CTkFrame(content, fg_color="white", corner_radius=12, height=90)
        search_container.pack(fill="x", pady=(0, 30))
        search_container.pack_propagate(False)
        
        search_content = ctk.CTkFrame(search_container, fg_color="white")
        search_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(
            search_content,
            text="¿En qué podemos ayudarte?",
            font=("Arial", 14, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        search_big = ctk.CTkEntry(
            search_content,
            placeholder_text="🔍 Buscar en la documentación, tutoriales, preguntas frecuentes...",
            height=50,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        search_big.pack(fill="x")
        
        # === SECCIÓN: INICIO RÁPIDO ===
        ctk.CTkLabel(
            content,
            text="🚀 Inicio Rápido",
            font=("Arial", 20, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        quick_start_row = ctk.CTkFrame(content, fg_color="transparent")
        quick_start_row.pack(fill="x", pady=(0, 30))
        
        quick_items = [
            ("📦", "Registrar Producto", "Aprende a dar de alta productos en el inventario", "#e8f4f8"),
            ("🔄", "Crear Movimiento", "Registra entradas y salidas de mercancía", "#fff4e6"),
            ("📊", "Ver Dashboard", "Conoce las métricas y estadísticas principales", "#e8f4f8"),
            ("👥", "Gestionar Usuarios", "Administra permisos y roles del sistema", "#d4edda")
        ]
        
        for i, (icon, title, desc, color) in enumerate(quick_items):
            self.create_help_card(quick_start_row, icon, title, desc, color, i, 4)
        
        # === SECCIÓN: GUÍAS POR MÓDULO ===
        ctk.CTkLabel(
            content,
            text="📖 Guías por Módulo",
            font=("Arial", 20, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        # Inventario
        self.create_module_guide(
            content,
            "📦",
            "Gestión de Inventario",
            [
                "• Cómo registrar un nuevo producto",
                "• Editar información de productos existentes",
                "• Eliminar productos del sistema",
                "• Aplicar filtros y búsquedas avanzadas",
                "• Exportar listado de inventario a Excel/PDF"
            ],
            "#e8f4f8"
        )
        
        # Movimientos
        self.create_module_guide(
            content,
            "🔄",
            "Control de Movimientos",
            [
                "• Registrar entradas de mercancía (compras)",
                "• Registrar salidas de mercancía (ventas)",
                "• Consultar historial de movimientos",
                "• Ajustes de inventario manuales",
                "• Ver resumen diario de entradas y salidas"
            ],
            "#fff4e6"
        )
        
        # Reportes
        self.create_module_guide(
            content,
            "📈",
            "Reportes y Análisis",
            [
                "• Generar reporte de inventario actual",
                "• Productos de baja rotación",
                "• Evolución del inventario mensual",
                "• Distribución por categoría",
                "• Exportar reportes personalizados"
            ],
            "#d4edda"
        )
        
        # Usuarios
        self.create_module_guide(
            content,
            "👥",
            "Administración de Usuarios",
            [
                "• Crear nuevos usuarios del sistema",
                "• Asignar roles y permisos",
                "• Activar o desactivar cuentas",
                "• Diferencias entre rol Admin y Empleado",
                "• Recuperación de contraseñas"
            ],
            "#ffe5e5"
        )
        
        # === PREGUNTAS FRECUENTES ===
        ctk.CTkLabel(
            content,
            text="❓ Preguntas Frecuentes",
            font=("Arial", 20, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(30, 15))
        
        faqs = [
            ("¿Cómo cambio mi contraseña?", "Dirígete a Configuración > Perfil de Usuario > Cambiar Contraseña"),
            ("¿Puedo restaurar un producto eliminado?", "Sí, desde Configuración > Respaldo de Datos puedes recuperar información eliminada"),
            ("¿Cómo exporto mi inventario a Excel?", "Ve a Inventario > Botón 'Exportar' > Selecciona formato Excel"),
            ("¿Qué pasa si se agota un producto?", "El sistema enviará una alerta automática y marcará el producto como 'Agotado'"),
            ("¿Puedo usar NoteBox sin internet?", "Sí, NoteBox funciona completamente offline en modo escritorio")
        ]
        
        for question, answer in faqs:
            self.create_faq_item(content, question, answer)
        
        # === SOPORTE Y CONTACTO ===
        support_card = ctk.CTkFrame(content, fg_color="#00b4d8", corner_radius=12)
        support_card.pack(fill="x", pady=(30, 0))
        
        support_content = ctk.CTkFrame(support_card, fg_color="transparent")
        support_content.pack(fill="both", expand=True, padx=40, pady=30)
        
        support_left = ctk.CTkFrame(support_content, fg_color="transparent")
        support_left.pack(side="left")
        
        ctk.CTkLabel(
            support_left,
            text="¿Necesitas más ayuda?",
            font=("Arial", 22, "bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(
            support_left,
            text="Nuestro equipo de soporte está disponible para ayudarte",
            font=("Arial", 13),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(0, 20))
        
        contact_btns = ctk.CTkFrame(support_left, fg_color="transparent")
        contact_btns.pack(anchor="w")
        
        ctk.CTkButton(
            contact_btns,
            text="📧 Enviar Email",
            width=150,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="white",
            text_color="#00b4d8",
            hover_color="#f0f0f0",
            corner_radius=8
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            contact_btns,
            text="💬 Chat en Vivo",
            width=150,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="transparent",
            text_color="white",
            border_width=2,
            border_color="white",
            hover_color="#0096c7",
            corner_radius=8
        ).pack(side="left")
        
        ctk.CTkLabel(
            support_content,
            text="🎧",
            font=("Segoe UI Emoji", 60),
            text_color="white"
        ).pack(side="right")
        
        # === INFO DEL SISTEMA ===
        info_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        info_card.pack(fill="x", pady=(20, 0))
        
        info_content = ctk.CTkFrame(info_card, fg_color="white")
        info_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        ctk.CTkLabel(
            info_content,
            text="ℹ️ Información del Sistema",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        info_items = [
            ("Versión actual:", "NoteBox v1.0.0"),
            ("Última actualización:", "05 de noviembre 2025"),
            ("Tipo de licencia:", "Profesional"),
            ("Documentación:", "https://docs.notebox.com"),
            ("Soporte técnico:", "soporte@notebox.com")
        ]
        
        for label, value in info_items:
            info_row = ctk.CTkFrame(info_content, fg_color="white")
            info_row.pack(fill="x", pady=3)
            
            ctk.CTkLabel(
                info_row,
                text=label,
                font=("Arial", 12, "bold"),
                text_color="#2b2d42",
                anchor="w",
                width=200
            ).pack(side="left")
            
            ctk.CTkLabel(
                info_row,
                text=value,
                font=("Arial", 12),
                text_color="#6c757d",
                anchor="w"
            ).pack(side="left", padx=(10, 0))
        
        # Footer
        footer = ctk.CTkLabel(
            main_container,
            text="NoteBox v1.0 - 2025",
            font=("Arial", 10),
            text_color="#adb5bd",
            fg_color="#f8f9fa",
            height=40
        )
        footer.pack(side="bottom", fill="x")
    
    def create_menu_item(self, parent, icon, text, active):
        """Crear item del menú"""
        bg_color = "#e8f4f8" if active else "white"
        text_color = "#00b4d8" if active else "#6c757d"
        
        item = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=8, height=45)
        item.pack(fill="x", padx=15, pady=2)
        item.pack_propagate(False)
        
        ctk.CTkLabel(
            item,
            text=icon,
            font=("Segoe UI Emoji", 16),
            width=30
        ).pack(side="left", padx=(15, 10))
        
        ctk.CTkLabel(
            item,
            text=text,
            font=("Arial", 13, "bold" if active else "normal"),
            text_color=text_color,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
    
    def create_help_card(self, parent, icon, title, description, color, position, total):
        """Crear tarjeta de ayuda rápida"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        
        if position == 0:
            card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        elif position == total - 1:
            card.pack(side="left", fill="both", expand=True, padx=(8, 0))
        else:
            card.pack(side="left", fill="both", expand=True, padx=8)
        
        card_content = ctk.CTkFrame(card, fg_color="white")
        card_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono
        ctk.CTkLabel(
            card_content,
            text=icon,
            font=("Segoe UI Emoji", 40),
            fg_color=color,
            corner_radius=12,
            width=70,
            height=70
        ).pack(pady=(0, 15))
        
        # Título
        ctk.CTkLabel(
            card_content,
            text=title,
            font=("Arial", 14, "bold"),
            text_color="#2b2d42",
            anchor="center"
        ).pack(pady=(0, 8))
        
        # Descripción
        ctk.CTkLabel(
            card_content,
            text=description,
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="center",
            wraplength=150
        ).pack()
        
        # Botón
        ctk.CTkButton(
            card_content,
            text="Ver guía →",
            width=120,
            height=35,
            font=("Arial", 11, "bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=6
        ).pack(pady=(15, 0))
    
    def create_module_guide(self, parent, icon, title, items, color):
        """Crear guía de módulo"""
        guide_card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        guide_card.pack(fill="x", pady=(0, 15))
        
        guide_content = ctk.CTkFrame(guide_card, fg_color="white")
        guide_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Header
        header = ctk.CTkFrame(guide_content, fg_color="white")
        header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            header,
            text=icon,
            font=("Segoe UI Emoji", 28),
            fg_color=color,
            corner_radius=10,
            width=50,
            height=50
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Items
        for item in items:
            ctk.CTkLabel(
                guide_content,
                text=item,
                font=("Arial", 12),
                text_color="#6c757d",
                anchor="w"
            ).pack(fill="x", pady=3)
    
    def create_faq_item(self, parent, question, answer):
        """Crear item de FAQ"""
        faq_card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        faq_card.pack(fill="x", pady=(0, 10))
        
        faq_content = ctk.CTkFrame(faq_card, fg_color="white")
        faq_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Pregunta
        question_frame = ctk.CTkFrame(faq_content, fg_color="white")
        question_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            question_frame,
            text="❓",
            font=("Segoe UI Emoji", 20)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            question_frame,
            text=question,
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        # Respuesta
        ctk.CTkLabel(
            faq_content,
            text=answer,
            font=("Arial", 12),
            text_color="#6c757d",
            anchor="w",
            wraplength=900
        ).pack(fill="x", padx=(30, 0))


if __name__ == "__main__":
    root = ctk.CTk()
    app = HelpView(root)
    root.mainloop()