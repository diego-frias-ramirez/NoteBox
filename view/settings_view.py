"""
NoteBox - Vista del Módulo de Configuración
Ubicación: view/settings_view.py
"""

import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime

from components.base_view import BaseView
from utils.logger import Logger

class ConfiguracionView(BaseView):
    """Vista del Módulo de Configuración."""

    def __init__(self, user_data):
        self.images = {}
        self.icon_refs = {}
        self.has_unsaved_changes = False
        
        # Instancia del controlador (import perezoso para evitar crash en import)
        try:
            from controller.settings_controller import SettingsController
            self.controller = SettingsController(user_data)

            # Cargar datos iniciales
            self.system_info = {}
            self.company_settings = {}
            self.alert_settings = {}
            self.backup_settings = {}
            self.storage_info = {}
            self.load_data()
        except Exception as e:
            Logger.error(f"Error inicializando módulo de configuración: {e}", "SETTINGS_VIEW")
            self.controller = None
            self.system_info = {}
            self.company_settings = {}
            self.alert_settings = {}
            self.backup_settings = {
                'auto_backup': True,
                'backup_frequency_days': 7,
                'retention_days': 30
            }
            self.storage_info = {}
        
        # Llamar al constructor de la clase base
        super().__init__(
            user_data=user_data,
            page_id="configuracion",
            page_title="Configuración del Sistema",
            page_subtitle="Personalizar ajustes de la aplicación"
        )

    def load_data(self):
        """Carga datos desde el controlador."""
        try:
            if not self.controller:
                Logger.error("Controlador de configuración no disponible, usando valores por defecto", "SETTINGS_VIEW")
                return

            self.system_info = self.controller.get_system_info()
            self.company_settings = self.controller.get_company_settings()
            self.alert_settings = self.controller.get_alert_settings()
            self.backup_settings = self.controller.get_backup_settings()
            self.storage_info = self.controller.get_storage_info()
            Logger.info("Datos de configuración cargados", "SETTINGS_VIEW")
        except Exception as e:
            Logger.error(f"Error cargando datos: {e}", "SETTINGS_VIEW")

    def create_content(self):
        """Crea el contenido del módulo de configuración."""
        content_frame = self.content_frame
        
        # Contenedor scrollable para todas las secciones
        main_scroll = ctk.CTkScrollableFrame(
            content_frame, fg_color="transparent",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        main_scroll.pack(fill="both", expand=True)
        
        # 1. INFORMACIÓN DEL NEGOCIO
        self.create_business_info_section(main_scroll)
        
        # 2. LOGO DEL NEGOCIO
        self.create_logo_section(main_scroll)
        
        # 3. PERSONALIZACIÓN DE COLORES
        self.create_colors_section(main_scroll)
        
        # 4. BACKUP AUTOMÁTICO
        self.create_backup_section(main_scroll)
        
        # 5. INFORMACIÓN DEL SISTEMA
        self.create_system_info_section(main_scroll)
        
        # 6. RECORDATORIO
        self.create_reminder_section(main_scroll)

    def create_business_info_section(self, parent):
        """Crea la sección de información del negocio."""
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 20))
        
        # Icono + Título
        title_container = ctk.CTkFrame(header, fg_color="transparent")
        title_container.pack(side="left")
        
        icon_frame = ctk.CTkFrame(title_container, fg_color="#E0F7FA", width=40, height=40, corner_radius=10)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="🏪", font=ctk.CTkFont(size=18)).place(relx=0.5, rely=0.5, anchor="center")
        
        titles = ctk.CTkFrame(title_container, fg_color="transparent")
        titles.pack(side="left")
        
        ctk.CTkLabel(
            titles, text="Información del Negocio",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            titles, text="Datos generales de su empresa",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(anchor="w")
        
        # Contenido del formulario
        form_container = ctk.CTkFrame(section, fg_color="transparent")
        form_container.pack(fill="x", padx=30, pady=(0, 25))
        
        # Nombre del Negocio
        ctk.CTkLabel(
            form_container, text="Nombre del Negocio",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.business_name_entry = ctk.CTkEntry(
            form_container, height=45, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8, placeholder_text="Ej: Papelería Mi Negocio"
        )
        self.business_name_entry.pack(fill="x", pady=(0, 15))
        self.business_name_entry.insert(0, self.company_settings.get('nombre_negocio', ''))
        self.business_name_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Fila: Tipo de Negocio + Moneda
        row1 = ctk.CTkFrame(form_container, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 15))
        
        # Tipo de Negocio (50%)
        tipo_container = ctk.CTkFrame(row1, fg_color="transparent")
        tipo_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            tipo_container, text="Tipo de Negocio",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.business_type_entry = ctk.CTkEntry(
            tipo_container, height=45, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1, corner_radius=8
        )
        self.business_type_entry.pack(fill="x")
        self.business_type_entry.insert(0, self.company_settings.get('tipo_negocio', ''))
        self.business_type_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Moneda (50%)
        moneda_container = ctk.CTkFrame(row1, fg_color="transparent")
        moneda_container.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            moneda_container, text="Moneda",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.currency_entry = ctk.CTkEntry(
            moneda_container, height=45, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1, corner_radius=8
        )
        self.currency_entry.pack(fill="x")
        self.currency_entry.insert(0, self.company_settings.get('moneda', 'MXN'))
        self.currency_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Dirección
        ctk.CTkLabel(
            form_container, text="Dirección",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.address_text = ctk.CTkTextbox(
            form_container, height=80, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8, wrap="word"
        )
        self.address_text.pack(fill="x", pady=(0, 15))
        self.address_text.insert("1.0", self.company_settings.get('direccion', ''))
        self.address_text.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Fila: Teléfono + Email
        row2 = ctk.CTkFrame(form_container, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 0))
        
        # Teléfono (50%)
        tel_container = ctk.CTkFrame(row2, fg_color="transparent")
        tel_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            tel_container, text="Teléfono",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.phone_entry = ctk.CTkEntry(
            tel_container, height=45, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8, placeholder_text="+52 123 456 7890"
        )
        self.phone_entry.pack(fill="x")
        self.phone_entry.insert(0, self.company_settings.get('telefono', ''))
        self.phone_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Email (50%)
        email_container = ctk.CTkFrame(row2, fg_color="transparent")
        email_container.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            email_container, text="Email",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
            email_container, height=45, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8, placeholder_text="contacto@minegocio.com"
        )
        self.email_entry.pack(fill="x")
        self.email_entry.insert(0, self.company_settings.get('email_contacto', ''))
        self.email_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())

    def create_logo_section(self, parent):
        """Crea la sección de logo del negocio."""
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 20))
        
        icon_frame = ctk.CTkFrame(header, fg_color="#E0F7FA", width=40, height=40, corner_radius=10)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="🖼️", font=ctk.CTkFont(size=18)).place(relx=0.5, rely=0.5, anchor="center")
        
        titles = ctk.CTkFrame(header, fg_color="transparent")
        titles.pack(side="left")
        
        ctk.CTkLabel(
            titles, text="Logo del Negocio",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            titles, text="Personalice la imagen de su empresa",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(anchor="w")
        
        # Contenedor del logo
        logo_container = ctk.CTkFrame(section, fg_color="transparent")
        logo_container.pack(fill="x", padx=30, pady=(0, 25))
        
        logo_row = ctk.CTkFrame(logo_container, fg_color="transparent")
        logo_row.pack(fill="x")
        
        # Logo actual (izquierda)
        current_logo_frame = ctk.CTkFrame(logo_row, fg_color="#F8FAFC", width=140, height=140, corner_radius=12, border_width=2, border_color="#E2E8F0")
        current_logo_frame.pack(side="left", padx=(0, 20))
        current_logo_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            current_logo_frame, text="🖼️", font=ctk.CTkFont(size=40), text_color="#94A3B8"
        ).place(relx=0.5, rely=0.4, anchor="center")
        
        ctk.CTkLabel(
            current_logo_frame, text="Logo actual",
            font=ctk.CTkFont(size=11), text_color="#64748B"
        ).place(relx=0.5, rely=0.7, anchor="center")
        
        # Área de carga (derecha)
        upload_frame = ctk.CTkFrame(logo_row, fg_color="#F8FAFC", corner_radius=12, border_width=2, border_color="#E2E8F0")
        upload_frame.pack(side="left", fill="both", expand=True)
        
        upload_inner = ctk.CTkFrame(upload_frame, fg_color="transparent")
        upload_inner.pack(expand=True, pady=30)
        
        ctk.CTkLabel(
            upload_inner, text="⬆️",
            font=ctk.CTkFont(size=32), text_color="#00B4D8"
        ).pack()
        
        ctk.CTkLabel(
            upload_inner, text="Haga clic para subir o arrastre su logo",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#1E293B"
        ).pack(pady=(10, 3))
        
        ctk.CTkLabel(
            upload_inner, text="PNG, JPG hasta 2MB",
            font=ctk.CTkFont(size=11), text_color="#94A3B8"
        ).pack()
        
        ctk.CTkLabel(
            logo_container, text="Recomendado: 200x200px, fondo transparente",
            font=ctk.CTkFont(size=11), text_color="#94A3B8"
        ).pack(anchor="center", pady=(15, 0))

    def create_colors_section(self, parent):
        """Crea la sección de personalización de colores."""
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 20))
        
        icon_frame = ctk.CTkFrame(header, fg_color="#E0F7FA", width=40, height=40, corner_radius=10)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="🎨", font=ctk.CTkFont(size=18)).place(relx=0.5, rely=0.5, anchor="center")
        
        titles = ctk.CTkFrame(header, fg_color="transparent")
        titles.pack(side="left")
        
        ctk.CTkLabel(
            titles, text="Personalización de Colores",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            titles, text="Ajuste los colores del tema (opcional)",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(anchor="w")
        
        # Contenedor de colores
        colors_container = ctk.CTkFrame(section, fg_color="transparent")
        colors_container.pack(fill="x", padx=30, pady=(0, 20))
        
        colors_row = ctk.CTkFrame(colors_container, fg_color="transparent")
        colors_row.pack(fill="x")
        
        # Color Primario
        primary_container = ctk.CTkFrame(colors_row, fg_color="transparent")
        primary_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            primary_container, text="Color Primario",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.primary_color_entry = ctk.CTkEntry(
            primary_container, height=45, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8, placeholder_text="#00B4D8"
        )
        self.primary_color_entry.pack(fill="x")
        self.primary_color_entry.insert(0, self.company_settings.get('color_primario', '#00B4D8'))
        self.primary_color_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Color Secundario
        secondary_container = ctk.CTkFrame(colors_row, fg_color="transparent")
        secondary_container.pack(side="left", fill="both", expand=True, padx=(10, 10))
        
        ctk.CTkLabel(
            secondary_container, text="Color Secundario",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.secondary_color_entry = ctk.CTkEntry(
            secondary_container, height=45, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8, placeholder_text="#10B981"
        )
        self.secondary_color_entry.pack(fill="x")
        self.secondary_color_entry.insert(0, self.company_settings.get('color_secundario', '#10B981'))
        self.secondary_color_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Color Sidebar
        sidebar_container = ctk.CTkFrame(colors_row, fg_color="transparent")
        sidebar_container.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            sidebar_container, text="Color Sidebar",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.sidebar_color_entry = ctk.CTkEntry(
            sidebar_container, height=45, font=ctk.CTkFont(size=13),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8, placeholder_text="#1E293B"
        )
        self.sidebar_color_entry.pack(fill="x")
        self.sidebar_color_entry.insert(0, "#1E293B")
        self.sidebar_color_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Preview de colores
        ctk.CTkLabel(
            colors_container, text="Vista previa de los colores aplicados al tema de la aplicación",
            font=ctk.CTkFont(size=11), text_color="#94A3B8"
        ).pack(anchor="w", pady=(15, 0))
        
        # Botones de acción
        buttons_row = ctk.CTkFrame(section, fg_color="transparent")
        buttons_row.pack(fill="x", padx=30, pady=(20, 25))
        
        save_btn = ctk.CTkButton(
            buttons_row, text="💾 GUARDAR CAMBIOS", height=45, width=180,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#00B4D8", hover_color="#0096B4",
            corner_radius=10, command=self.save_all_settings
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            buttons_row, text="Cancelar", height=45, width=120,
            font=ctk.CTkFont(size=13), fg_color="transparent",
            text_color="#64748B", hover_color="#F1F5F9",
            border_width=1, border_color="#E2E8F0",
            corner_radius=10, command=self.cancel_changes
        )
        cancel_btn.pack(side="left")

    def create_backup_section(self, parent):
        """Crea la sección de backup automático."""
        section = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 20))
        
        icon_frame = ctk.CTkFrame(header, fg_color="#E0F7FA", width=40, height=40, corner_radius=10)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="💾", font=ctk.CTkFont(size=18)).place(relx=0.5, rely=0.5, anchor="center")
        
        titles = ctk.CTkFrame(header, fg_color="transparent")
        titles.pack(side="left")
        
        ctk.CTkLabel(
            titles, text="Backup Automático",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        # Contenedor
        content = ctk.CTkFrame(section, fg_color="transparent")
        content.pack(fill="x", padx=30, pady=(0, 25))
        
        # Fila: Label + Switch
        backup_row = ctk.CTkFrame(content, fg_color="transparent")
        backup_row.pack(fill="x", pady=(0, 10))
        
        backup_info = ctk.CTkFrame(backup_row, fg_color="transparent")
        backup_info.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            backup_info, text="Backup Diario",
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            backup_info, text="Respaldar datos cada 24 horas",
            font=ctk.CTkFont(size=11), text_color="#64748B"
        ).pack(anchor="w")
        
        # Switch
        self.backup_switch = ctk.CTkSwitch(
            backup_row, text="", width=50, height=28,
            fg_color="#CBD5E1", progress_color="#00B4D8",
            button_color="#FFFFFF", button_hover_color="#F8FAFC"
        )
        self.backup_switch.pack(side="right")
        if self.backup_settings.get('auto_backup', True):
            self.backup_switch.select()
        
        # Último backup
        last_backup = self.system_info.get('last_backup', 'Nunca')
        
        ctk.CTkLabel(
            content, text="Último backup:",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(anchor="w", pady=(10, 3))
        
        ctk.CTkLabel(
            content, text=last_backup,
            font=ctk.CTkFont(size=13, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        # Botón crear backup
        backup_btn = ctk.CTkButton(
            content, text="💾 Crear Backup Ahora", height=42, width=200,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#00B4D8", hover_color="#0096B4",
            corner_radius=10, command=self.create_backup_now
        )
        backup_btn.pack(anchor="w", pady=(15, 0))

    def create_system_info_section(self, parent):
        """Crea la sección de información del sistema."""
        section = ctk.CTkFrame(parent, fg_color="#00B4D8", corner_radius=15)
        section.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(section, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Título
        ctk.CTkLabel(
            content, text="Información del Sistema",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#FFFFFF"
        ).pack(anchor="w", pady=(0, 15))
        
        # Grid de información
        info_grid = ctk.CTkFrame(content, fg_color="transparent")
        info_grid.pack(fill="x")
        
        info_items = [
            ("Versión", self.system_info.get('app_version', 'v1.0.0')),
            ("Licencia", "Profesional"),
            ("Productos Registrados", f"{self.system_info.get('total_products', 0):,} / Ilimitado"),
            ("Usuarios Activos", f"{self.system_info.get('total_users', 0)} / 10")
        ]
        
        for i, (label, value) in enumerate(info_items):
            item_frame = ctk.CTkFrame(info_grid, fg_color="transparent")
            item_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                item_frame, text=label,
                font=ctk.CTkFont(size=12), text_color="#E0F7FA"
            ).pack(side="left")
            
            ctk.CTkLabel(
                item_frame, text=value,
                font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFFFFF"
            ).pack(side="right")

    def create_reminder_section(self, parent):
        """Crea la sección de recordatorio."""
        section = ctk.CTkFrame(parent, fg_color="#FEF3C7", corner_radius=15, border_width=2, border_color="#F59E0B")
        section.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(section, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título
        title_row = ctk.CTkFrame(content, fg_color="transparent")
        title_row.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            title_row, text="⚠️",
            font=ctk.CTkFont(size=20)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_row, text="Recordatorio",
            font=ctk.CTkFont(size=14, weight="bold"), text_color="#92400E"
        ).pack(side="left")
        
        # Mensaje
        ctk.CTkLabel(
            content, text="Recuerde realizar respaldos periódicos de su información para evitar pérdida de datos.",
            font=ctk.CTkFont(size=12), text_color="#78350F",
            wraplength=800, justify="left"
        ).pack(anchor="w")

    def mark_unsaved_changes(self):
        """Marca que hay cambios sin guardar."""
        self.has_unsaved_changes = True

    def save_all_settings(self):
        """Guarda todos los cambios de configuración."""
        try:
            # Recopilar datos
            company_data = {
                'nombre_negocio': self.business_name_entry.get().strip(),
                'tipo_negocio': self.business_type_entry.get().strip(),
                'direccion': self.address_text.get("1.0", "end-1c").strip(),
                'telefono': self.phone_entry.get().strip(),
                'email_contacto': self.email_entry.get().strip()
            }
            
            # Validar datos básicos
            if not company_data['nombre_negocio']:
                self.show_message("El nombre del negocio es obligatorio", "error")
                return
            
            # Guardar configuración de empresa
            if not self.controller:
                Logger.error("Intento de guardar configuración sin controlador disponible", "SETTINGS_VIEW")
                self.show_message("No se puede guardar: módulo de configuración no disponible", "error")
                return

            success, message = self.controller.update_company_settings(company_data)
            
            if success:
                self.has_unsaved_changes = False
                Logger.success("Configuración guardada", "SETTINGS_VIEW")
                self.show_message("✅ Configuración guardada correctamente", "success")
                
                # Recargar datos
                self.load_data()
            else: self.show_message(f"❌ Error: {message}", "error")
            
        except Exception as e:
            Logger.error(f"Error guardando configuración: {e}", "SETTINGS_VIEW")
            self.show_message(f"❌ Error: {str(e)}", "error")

    def cancel_changes(self):
        """Cancela los cambios y recarga los datos."""
        if self.has_unsaved_changes:
            # Confirmar cancelación
            confirm = self.show_confirm("¿Desea descartar los cambios?")
            if not confirm:
                return
        
        # Recargar datos originales
        self.load_data()
        self.business_name_entry.delete(0, "end")
        self.business_name_entry.insert(0, self.company_settings.get('nombre_negocio', ''))
        # ... (recargar todos los campos)
        
        self.has_unsaved_changes = False
        self.show_message("Cambios descartados", "info")

    def create_backup_now(self):
        """Crea un backup manual."""
        try:
            if not self.controller:
                Logger.error("Intento de backup sin controlador disponible", "SETTINGS_VIEW")
                self.show_message("No se puede crear backup: módulo de configuración no disponible", "error")
                return

            success, result = self.controller.create_backup()
            
            if success:
                filename = os.path.basename(result)
                self.show_message(f"✅ Backup creado exitosamente\n\n{filename}", "success")
                # Recargar información
                self.load_data()
            else:
                self.show_message(f"❌ Error creando backup:\n{result}", "error")
                
        except Exception as e:
            Logger.error(f"Error en backup manual: {e}", "SETTINGS_VIEW")
            self.show_message(f"❌ Error: {str(e)}", "error")

    def show_confirm(self, message):
        """Muestra diálogo de confirmación."""
        from tkinter import messagebox
        return messagebox.askyesno("Confirmar", message, parent=self)

    def show_message(self, message, msg_type="info"):
        """Muestra un mensaje temporal."""
        colors = {
            "info": "#3B82F6", 
            "success": "#10B981", 
            "warning": "#F59E0B", 
            "error": "#EF4444"
        }
        color = colors.get(msg_type, "#3B82F6")
        
        popup = ctk.CTkToplevel(self)
        popup.title("")
        popup.geometry("420x140")
        popup.resizable(False, False)
        popup.configure(fg_color="#FFFFFF")
        popup.transient(self)
        popup.grab_set()
        
        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (420 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (140 // 2)
        popup.geometry(f"420x140+{x}+{y}")
        
        label = ctk.CTkLabel(
            popup, text=message, wraplength=380,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color, justify="center"
        )
        label.pack(expand=True, padx=20, pady=20)
        
        popup.after(3000, popup.destroy)