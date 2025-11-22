# view/settings_view.py

import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from datetime import datetime

class SettingsView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox - Configuración")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.backup_enabled = tk.BooleanVar(value=True)
        
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
            ("⚙️", "Configuración", True),
            ("❓", "Ayuda", False)
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
            text="Dashboard Principal",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_text,
            text="Bienvenido al sistema de gestión",
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
        
        # === 1. INFORMACIÓN DEL NEGOCIO ===
        business_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        business_card.pack(fill="x", pady=(0, 20))
        
        business_content = ctk.CTkFrame(business_card, fg_color="white")
        business_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header con icono
        business_header = ctk.CTkFrame(business_content, fg_color="white")
        business_header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            business_header,
            text="🏪",
            font=("Segoe UI Emoji", 24),
            fg_color="#e8f4f8",
            corner_radius=8,
            width=45,
            height=45
        ).pack(side="left", padx=(0, 15))
        
        header_text_frame = ctk.CTkFrame(business_header, fg_color="white")
        header_text_frame.pack(side="left")
        
        ctk.CTkLabel(
            header_text_frame,
            text="Información del Negocio",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_text_frame,
            text="Datos generales de su empresa",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w")
        
        # Nombre del Negocio
        ctk.CTkLabel(
            business_content,
            text="Nombre del Negocio",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        business_name = ctk.CTkEntry(
            business_content,
            placeholder_text="Papelería Mi Negocio",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        business_name.insert(0, "Papelería Mi Negocio")
        business_name.pack(fill="x", pady=(0, 20))
        
        # Tipo y Moneda (2 columnas)
        row1 = ctk.CTkFrame(business_content, fg_color="white")
        row1.pack(fill="x", pady=(0, 20))
        
        # Tipo de Negocio
        tipo_frame = ctk.CTkFrame(row1, fg_color="white")
        tipo_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            tipo_frame,
            text="Tipo de Negocio",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        tipo_entry = ctk.CTkEntry(
            tipo_frame,
            placeholder_text="Ej: Papelería, Abarrotes...",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        tipo_entry.pack(fill="x")
        
        # Moneda
        moneda_frame = ctk.CTkFrame(row1, fg_color="white")
        moneda_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            moneda_frame,
            text="Moneda",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        moneda_entry = ctk.CTkEntry(
            moneda_frame,
            placeholder_text="MXN, USD, EUR...",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        moneda_entry.pack(fill="x")
        
        # Dirección
        ctk.CTkLabel(
            business_content,
            text="Dirección",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        direccion_textbox = ctk.CTkTextbox(
            business_content,
            height=80,
            font=("Arial", 12),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        direccion_textbox.pack(fill="x", pady=(0, 20))
        
        # Teléfono y Email (2 columnas)
        row2 = ctk.CTkFrame(business_content, fg_color="white")
        row2.pack(fill="x")
        
        # Teléfono
        tel_frame = ctk.CTkFrame(row2, fg_color="white")
        tel_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            tel_frame,
            text="Teléfono",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        tel_entry = ctk.CTkEntry(
            tel_frame,
            placeholder_text="+52 123 456 7890",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        tel_entry.insert(0, "+52 123 456 7890")
        tel_entry.pack(fill="x")
        
        # Email
        email_frame = ctk.CTkFrame(row2, fg_color="white")
        email_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            email_frame,
            text="Email",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        email_entry = ctk.CTkEntry(
            email_frame,
            placeholder_text="contacto@minegocio.com",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        email_entry.insert(0, "contacto@minegocio.com")
        email_entry.pack(fill="x")
        
        # === 2. LOGO DEL NEGOCIO ===
        logo_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        logo_card.pack(fill="x", pady=(0, 20))
        
        logo_content = ctk.CTkFrame(logo_card, fg_color="white")
        logo_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        logo_header = ctk.CTkFrame(logo_content, fg_color="white")
        logo_header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            logo_header,
            text="🖼️",
            font=("Segoe UI Emoji", 24),
            fg_color="#e8f4f8",
            corner_radius=8,
            width=45,
            height=45
        ).pack(side="left", padx=(0, 15))
        
        logo_header_text = ctk.CTkFrame(logo_header, fg_color="white")
        logo_header_text.pack(side="left")
        
        ctk.CTkLabel(
            logo_header_text,
            text="Logo del Negocio",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_header_text,
            text="Personalice la imagen de su empresa",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w")
        
        # Logo upload area
        upload_row = ctk.CTkFrame(logo_content, fg_color="white")
        upload_row.pack(fill="x")
        
        # Logo actual (preview)
        logo_preview = ctk.CTkFrame(
            upload_row,
            fg_color="#f8f9fa",
            corner_radius=8,
            width=120,
            height=120
        )
        logo_preview.pack(side="left", padx=(0, 20))
        logo_preview.pack_propagate(False)
        
        ctk.CTkLabel(
            logo_preview,
            text="🖼️\nLogo actual",
            font=("Arial", 11),
            text_color="#6c757d",
            justify="center"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Upload area
        upload_area = ctk.CTkFrame(
            upload_row,
            fg_color="#f8f9fa",
            corner_radius=8,
            border_width=2,
            border_color="#e0e0e0"
        )
        upload_area.pack(side="left", fill="both", expand=True)
        
        upload_content = ctk.CTkFrame(upload_area, fg_color="transparent")
        upload_content.pack(expand=True, pady=40)
        
        ctk.CTkLabel(
            upload_content,
            text="📤",
            font=("Segoe UI Emoji", 32)
        ).pack()
        
        ctk.CTkLabel(
            upload_content,
            text="Haga clic para subir o arrastre su logo",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            upload_content,
            text="PNG, JPG hasta 2MB",
            font=("Arial", 11),
            text_color="#6c757d"
        ).pack()
        
        ctk.CTkLabel(
            logo_content,
            text="Recomendado: 200x200px, fondo transparente",
            font=("Arial", 10),
            text_color="#6c757d",
            anchor="w"
        ).pack(fill="x", pady=(15, 0))
        
        # === 3. PERSONALIZACIÓN DE COLORES ===
        colors_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        colors_card.pack(fill="x", pady=(0, 20))
        
        colors_content = ctk.CTkFrame(colors_card, fg_color="white")
        colors_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        colors_header = ctk.CTkFrame(colors_content, fg_color="white")
        colors_header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            colors_header,
            text="🎨",
            font=("Segoe UI Emoji", 24),
            fg_color="#e8f4f8",
            corner_radius=8,
            width=45,
            height=45
        ).pack(side="left", padx=(0, 15))
        
        colors_header_text = ctk.CTkFrame(colors_header, fg_color="white")
        colors_header_text.pack(side="left")
        
        ctk.CTkLabel(
            colors_header_text,
            text="Personalización de Colores",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            colors_header_text,
            text="Ajuste los colores del tema (opcional)",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w")
        
        # Colores (3 columnas)
        colors_row = ctk.CTkFrame(colors_content, fg_color="white")
        colors_row.pack(fill="x", pady=(0, 15))
        
        # Color Primario
        primary_frame = ctk.CTkFrame(colors_row, fg_color="white")
        primary_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            primary_frame,
            text="Color Primario",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        primary_entry = ctk.CTkEntry(
            primary_frame,
            placeholder_text="#0AB7F3",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        primary_entry.insert(0, "#0AB7F3")
        primary_entry.pack(fill="x")
        
        # Color Secundario
        secondary_frame = ctk.CTkFrame(colors_row, fg_color="white")
        secondary_frame.pack(side="left", fill="x", expand=True, padx=10)
        
        ctk.CTkLabel(
            secondary_frame,
            text="Color Secundario",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        secondary_entry = ctk.CTkEntry(
            secondary_frame,
            placeholder_text="#53D4FE",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        secondary_entry.insert(0, "#53D4FE")
        secondary_entry.pack(fill="x")
        
        # Color Sidebar
        sidebar_frame = ctk.CTkFrame(colors_row, fg_color="white")
        sidebar_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            sidebar_frame,
            text="Color Sidebar",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        sidebar_entry = ctk.CTkEntry(
            sidebar_frame,
            placeholder_text="#B77840",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        sidebar_entry.insert(0, "#B77840")
        sidebar_entry.pack(fill="x")
        
        # Vista previa
        ctk.CTkLabel(
            colors_content,
            text="Vista previa de los colores aplicados al tema de la aplicación",
            font=("Arial", 10),
            text_color="#6c757d",
            anchor="w"
        ).pack(fill="x", pady=(0, 20))
        
        # Botones
        buttons_frame = ctk.CTkFrame(colors_content, fg_color="white")
        buttons_frame.pack(fill="x")
        
        ctk.CTkButton(
            buttons_frame,
            text="💾 GUARDAR CAMBIOS",
            width=200,
            height=50,
            font=("Arial", 14, "bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=8
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=120,
            height=50,
            font=("Arial", 13),
            fg_color="white",
            text_color="#6c757d",
            border_width=1,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
            corner_radius=8
        ).pack(side="left")
        
        # === 4. BACKUP AUTOMÁTICO ===
        backup_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        backup_card.pack(fill="x", pady=(0, 20))
        
        backup_content = ctk.CTkFrame(backup_card, fg_color="white")
        backup_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header con toggle
        backup_header = ctk.CTkFrame(backup_content, fg_color="white")
        backup_header.pack(fill="x", pady=(0, 20))
        
        backup_left = ctk.CTkFrame(backup_header, fg_color="white")
        backup_left.pack(side="left")
        
        ctk.CTkLabel(
            backup_left,
            text="💾",
            font=("Segoe UI Emoji", 24),
            fg_color="#e8f4f8",
            corner_radius=8,
            width=45,
            height=45
        ).pack(side="left", padx=(0, 15))
        
        backup_text = ctk.CTkFrame(backup_left, fg_color="white")
        backup_text.pack(side="left")
        
        ctk.CTkLabel(
            backup_text,
            text="Backup Automático",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        # Toggle switch
        backup_switch = ctk.CTkSwitch(
            backup_header,
            text="",
            variable=self.backup_enabled,
            onvalue=True,
            offvalue=False,
            fg_color="#00b4d8",
            progress_color="#00b4d8",
            button_color="white",
            button_hover_color="#f0f0f0"
        )
        backup_switch.pack(side="right")
        
        # Info backup
        ctk.CTkLabel(
            backup_content,
            text="Backup Diario",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(
            backup_content,
            text="Respaldar datos cada 24 horas",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            backup_content,
            text="Último backup:",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(
            backup_content,
            text="05/11/2025 - 03:00 AM",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(fill="x", pady=(0, 20))
        
        # Botón crear backup
        ctk.CTkButton(
            backup_content,
            text="💾 Crear Backup Ahora",
            width=200,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=8
        ).pack(anchor="w")
        
        # === 5. INFORMACIÓN DEL SISTEMA ===
        system_card = ctk.CTkFrame(content, fg_color="#00b4d8", corner_radius=12)
        system_card.pack(fill="x", pady=(0, 20))
        
        system_content = ctk.CTkFrame(system_card, fg_color="transparent")
        system_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            system_content,
            text="Información del Sistema",
            font=("Arial", 18, "bold"),
            text_color="white",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))
        
        info_items = [
            ("Versión:", "NoteBox v1.0.0"),
            ("Licencia:", "Profesional"),
            ("Productos Registrados:", "1,245 / Ilimitado"),
            ("Usuarios Activos:", "5 / 10")
        ]
        
        for label, value in info_items:
            info_row = ctk.CTkFrame(system_content, fg_color="transparent")
            info_row.pack(fill="x", pady=3)
            
            ctk.CTkLabel(
                info_row,
                text=label,
                font=("Arial", 12),
                text_color="white",
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                info_row,
                text=value,
                font=("Arial", 12, "bold"),
                text_color="white",
                anchor="w"
            ).pack(side="left", padx=(10, 0))
        
        # === 6. RECORDATORIO ===
        reminder_card = ctk.CTkFrame(content, fg_color="#fff4e6", corner_radius=12)
        reminder_card.pack(fill="x")
        
        reminder_content = ctk.CTkFrame(reminder_card, fg_color="transparent")
        reminder_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(
            reminder_content,
            text="⚠️ Recordatorio",
            font=("Arial", 14, "bold"),
            text_color="#8b6914",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(
            reminder_content,
            text="Recuerde realizar respaldos periódicos de su información para evitar pérdida de datos.",
            font=("Arial", 11),
            text_color="#8b6914",
            anchor="w",
            wraplength=800
        ).pack(fill="x")
        
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


if __name__ == "__main__":
    root = ctk.CTk()
    app = SettingsView(root)
    root.mainloop()