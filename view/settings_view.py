"""
NoteBox - Vista del Módulo de Configuración
Ubicación: view/settings_view.py
"""

import customtkinter as ctk
from PIL import Image
import os
import shutil
from tkinter import filedialog
from datetime import datetime

from components.base_view import BaseView
from controller.settings_controller import SettingsController
from utils.logger import Logger
from utils.helpers import Helpers

class SettingsView(BaseView):
    """Vista del Módulo de Configuración."""

    def __init__(self, user_data):
        self.images = {}
        self.icon_refs = {}
        self.has_unsaved_changes = False
        
        # Instancia del controlador
        self.controller = SettingsController(user_data)
        
        # Cargar datos iniciales
        self.system_info = {}
        self.company_settings = {}
        self.alert_settings = {}
        self.backup_settings = {}
        self.storage_info = {}
        self.load_data()
        
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
        main_scroll.pack(fill="both", expand=True, padx=15, pady=15)
        main_scroll.configure(height=650)
        
        # 1. INFORMACIÓN DEL NEGOCIO
        self.create_business_info_section(main_scroll)
        
        # 2. IMÁGENES / ASSETS (splash, banner, reports)
        self.create_assets_section(main_scroll)
        
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
            corner_radius=8, placeholder_text="#0960ae"
        )
        self.primary_color_entry.pack(fill="x")
        app_cfg = self.controller.load_app_settings()
        primary_color = app_cfg.get('ui', {}).get('colors', {}).get('primary', '#0960ae')
        self.primary_color_entry.insert(0, primary_color)
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
            corner_radius=8, placeholder_text="#0960ae"
        )
        self.secondary_color_entry.pack(fill="x")
        app_cfg = self.controller.load_app_settings()
        secondary_color = app_cfg.get('ui', {}).get('colors', {}).get('secondary', '#0960ae')
        self.secondary_color_entry.insert(0, secondary_color)
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
            corner_radius=8, placeholder_text="#0960ae"
        )
        self.sidebar_color_entry.pack(fill="x")
        app_cfg = self.controller.load_app_settings()
        sidebar_color = app_cfg.get('ui', {}).get('colors', {}).get('sidebar', '#0960ae')
        self.sidebar_color_entry.insert(0, sidebar_color)
        self.sidebar_color_entry.bind("<KeyRelease>", lambda e: self.mark_unsaved_changes())
        
        # Preview de colores
        ctk.CTkLabel(
            colors_container, text="Reiniciar para mostara los colores aplicados al tema de la aplicación",
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

        # Frecuencia y retención
        freq_row = ctk.CTkFrame(content, fg_color="transparent")
        freq_row.pack(fill="x", pady=(12, 0))

        freq_container = ctk.CTkFrame(freq_row, fg_color="transparent")
        freq_container.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(freq_container, text="Frecuencia (días)", font=ctk.CTkFont(size=12), text_color="#64748B").pack(anchor="w")
        self.backup_freq_entry = ctk.CTkEntry(freq_container, height=36, width=120)
        self.backup_freq_entry.pack(anchor="w", pady=(6, 0))
        self.backup_freq_entry.insert(0, str(self.backup_settings.get('backup_frequency_days', 7)))

        retention_container = ctk.CTkFrame(freq_row, fg_color="transparent")
        retention_container.pack(side="right", fill="both", expand=True)
        ctk.CTkLabel(retention_container, text="Retención (días)", font=ctk.CTkFont(size=12), text_color="#64748B").pack(anchor="w")
        self.backup_retention_entry = ctk.CTkEntry(retention_container, height=36, width=120)
        self.backup_retention_entry.pack(anchor="w", pady=(6, 0))
        self.backup_retention_entry.insert(0, str(self.backup_settings.get('retention_days', 30)))

    def create_assets_section(self, parent):
        """Sección para gestionar imágenes/configuración de assets (splash, banner, reports)."""
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
            titles, text="Recursos / Imágenes",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            titles, text="Configure imágenes usadas en splash, dashboard y reportes",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(anchor="w")

        # Content
        content = ctk.CTkFrame(section, fg_color="transparent")
        content.pack(fill="x", padx=30, pady=(0, 25))

        # Assets to manage: key -> (label, default_relative, dest_folder)
        assets = {
            'splash_image': ("Imagen Splash (fondo)", 'assets/images/splash_bg.png', 'images'),
            'splash_logo': ("Logo Splash", 'assets/icons/logo.png', 'icons'),
            'dashboard_banner': ("Banner Dashboard", 'assets/images/banner.png', 'images'),
            'reports_top_product_image': ("Imagen - Más Vendido (Reportes)", 'assets/images/products_showcase.png', 'images')
        }

        for key, (label_text, default_rel, dest_folder) in assets.items():
            self._create_asset_row(content, key, label_text, default_rel, dest_folder)

    def _create_asset_row(self, parent, key, label_text, default_rel, dest_folder):
        """Crea una fila para un asset con preview, ruta y botones."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(8, 8))

        # Preview
        preview_frame = ctk.CTkFrame(row, fg_color="#F8FAFC", width=90, height=90, corner_radius=10)
        preview_frame.pack(side="left", padx=(0, 12))
        preview_frame.pack_propagate(False)

        preview_label = ctk.CTkLabel(preview_frame, text="🖼️", font=ctk.CTkFont(size=28), text_color="#94A3B8")
        preview_label.place(relx=0.5, rely=0.5, anchor="center")

        # Info + path
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(info, text=label_text, font=ctk.CTkFont(size=12, weight="bold"), text_color="#374151").pack(anchor="w")

        path_label = ctk.CTkLabel(info, text="(ruta no disponible)", font=ctk.CTkFont(size=11), text_color="#64748B")
        path_label.pack(anchor="w", pady=(6, 0))

        # Buttons
        btns = ctk.CTkFrame(row, fg_color="transparent")
        btns.pack(side="right")

        change_btn = ctk.CTkButton(btns, text="Cambiar", width=110, height=34, fg_color="#00B4D8",
                                   corner_radius=8, command=lambda k=key, d=dest_folder, pr=path_label, pv=preview_label, dr=default_rel: self.choose_asset_file(k, d, pr, pv, dr))
        change_btn.pack(side="right", padx=(8, 0))

        reset_btn = ctk.CTkButton(btns, text="Restaurar", width=110, height=34, fg_color="transparent",
                                  text_color="#64748B", border_width=1, border_color="#E2E8F0",
                                  corner_radius=8, command=lambda k=key, pr=path_label, pv=preview_label, dr=default_rel: self.restore_asset_default(k, pr, pv, dr))
        reset_btn.pack(side="right")

        # Initialize preview/path
        try:
            asset_path = Helpers.get_asset_path(key, default_rel)
            if os.path.exists(asset_path):
                path_label.configure(text=os.path.relpath(asset_path, os.path.dirname(self.base_path)))
                # try to load preview
                try:
                    img = Image.open(asset_path)
                    img = img.resize((80, 80), Image.LANCZOS)
                    self.images[key] = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
                    preview_label.configure(image=self.images[key], text="")
                except Exception:
                    preview_label.configure(text="🖼️")
            else:
                path_label.configure(text="(archivo no encontrado)")
        except Exception:
            path_label.configure(text="(error cargando ruta)")

    def choose_asset_file(self, key, dest_folder, path_label, preview_label, default_rel):
        """Abre un file dialog para seleccionar la nueva imagen y la copia a assets."""
        filetypes = [("Images", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*")]
        selected = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=filetypes)
        if not selected:
            return

        try:
            # Validar tamaño (2MB recomendado)
            max_bytes = 2 * 1024 * 1024
            if os.path.getsize(selected) > max_bytes:
                self.show_message("El archivo excede 2MB. Elija uno más pequeño.", "warning")
                return

            # Copiar al folder correspondiente en assets
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            assets_dir = os.path.join(project_root, 'assets', dest_folder)
            os.makedirs(assets_dir, exist_ok=True)

            filename = Helpers.sanitize_filename(os.path.basename(selected))
            dest_path = os.path.join(assets_dir, filename)

            # Evitar sobreescribir: si existe, usar sufijo
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(assets_dir, f"{base}_{counter}{ext}")
                counter += 1

            shutil.copy2(selected, dest_path)

            # Guardar ruta relativa en configuración
            rel = os.path.relpath(dest_path, project_root).replace('\\', '/')
            ok = Helpers.update_asset_setting(key, rel)
            if not ok:
                self.show_message("No se pudo actualizar la configuración.", "error")
                return

            # Actualizar vista
            path_label.configure(text=rel)
            try:
                img = Image.open(dest_path)
                img = img.resize((80, 80), Image.LANCZOS)
                self.images[key] = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
                preview_label.configure(image=self.images[key], text="")
            except Exception:
                preview_label.configure(text="🖼️")

            self.show_message("Imagen actualizada correctamente", "success")

        except Exception as e:
            Logger.error(f"Error al actualizar asset {key}: {e}", "SETTINGS_VIEW")
            self.show_message(f"Error: {str(e)}", "error")

    def restore_asset_default(self, key, path_label, preview_label, default_rel):
        """Restaura la ruta del asset a la ruta por defecto en config."""
        try:
            ok = Helpers.update_asset_setting(key, default_rel)
            if ok:
                asset_path = Helpers.get_asset_path(key, default_rel)
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if os.path.exists(asset_path):
                    rel = os.path.relpath(asset_path, project_root).replace('\\', '/')
                    path_label.configure(text=rel)
                    try:
                        img = Image.open(asset_path)
                        img = img.resize((80, 80), Image.LANCZOS)
                        self.images[key] = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
                        preview_label.configure(image=self.images[key], text="")
                    except Exception:
                        preview_label.configure(text="🖼️")
                else:
                    path_label.configure(text="(archivo por defecto no encontrado)")

                self.show_message("Ruta restaurada a la configuración por defecto", "success")
            else:
                self.show_message("No se pudo actualizar la configuración", "error")
        except Exception as e:
            Logger.error(f"Error al restaurar asset {key}: {e}", "SETTINGS_VIEW")
            self.show_message(f"Error: {str(e)}", "error")

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
            # Recopilar datos de empresa
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
            success_company, msg_company = self.controller.update_company_settings(company_data)
            
            # Guardar colores UI en app_settings.json
            colors = {
                'primary': self.primary_color_entry.get().strip() or "#00B4D8",
                'secondary': self.secondary_color_entry.get().strip() or "#10B981",
                'sidebar': self.sidebar_color_entry.get().strip() or "#1E293B"
            }
            success_colors, msg_colors = self.controller.update_ui_colors(colors)

            # Guardar configuración de backup
            backup_data = {
                'auto_backup': bool(self.backup_switch.get()),
                'backup_frequency_days': int(self.backup_freq_entry.get().strip() or 7),
                'retention_days': int(self.backup_retention_entry.get().strip() or 30)
            }
            success_backup, msg_backup = self.controller.update_backup_settings(backup_data)

            # Determinar resultado general
            all_ok = success_company and success_colors and success_backup
            
            if all_ok:
                self.has_unsaved_changes = False
                Logger.success("Toda la configuración guardada correctamente", "SETTINGS_VIEW")
                self.show_message("✅ Configuración guardada\n\nLos colores se aplicarán al reiniciar la app", "success")
                self.load_data()
            else:
                error_parts = []
                if not success_company:
                    error_parts.append("empresa")
                if not success_colors:
                    error_parts.append("colores")
                if not success_backup:
                    error_parts.append("backup")
                
                error_msg = ", ".join(error_parts)
                self.show_message(f"⚠️ Error guardando: {error_msg}", "warning")
            
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
            # Default filename: backup_notebox_YYYYMMDD_HHMMSS.sql
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"backup_notebox_{timestamp}.sql"
            
            # Initial dir: configured backup dir or exports/backups
            initial_dir = Helpers.get_exports_dir('backups')
            
            # Ask where to save
            filepath = filedialog.asksaveasfilename(
                title="Guardar Backup",
                initialdir=initial_dir,
                initialfile=default_filename,
                defaultextension=".sql",
                filetypes=[("SQL Database Dump", "*.sql"), ("All files", "*.*")]
            )

            if not filepath:
                return  # Usuario canceló
            
            success, result = self.controller.create_backup(filepath=filepath)
            
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

    def get_notification_count(self):
        """Obtiene el número de notificaciones no leídas."""
        try:
            from model.alert_model import AlertModel
            alert_model = AlertModel()
            unread_alerts = alert_model.get_unread_alerts()
            return len(unread_alerts) if unread_alerts else 0
        except Exception as e:
            print(f"Error al contar notificaciones: {e}")
            return 0
