"""
NoteBox - Componente Header (Barra Superior)
Ubicación: components/header.py
"""

import customtkinter as ctk
from datetime import datetime
from PIL import Image
import os

class Header(ctk.CTkFrame):
    """Barra superior de navegación reutilizable."""
    
    def __init__(self, parent, title, subtitle="", on_menu_toggle=None, 
                 on_notifications=None, notification_count=0):
        super().__init__(parent, fg_color="#FAFAFA", height=70, corner_radius=0)
        self.pack_propagate(False)
        
        self.title = title
        self.subtitle = subtitle
        self.on_menu_toggle = on_menu_toggle
        self.on_notifications = on_notifications
        self.notification_count = notification_count
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Colores por defecto
        self.colors = {
            "bg": "#FAFAFA",
            "title": "#1E293B",
            "subtitle": "#64748B",
            "icon": "#64748B",
            "notification_badge": "#EF4444",
            "border": "#E2E8F0"
        }
        
        # Cargar colores desde app_settings.json si existen
        self._load_custom_colors()
        
        self.notification_icon_img = None
        self.create_header()
    
    
    def _load_custom_colors(self):
        """Carga colores personalizados desde app_settings.json."""
        try:
            import json
            config_path = os.path.join(self.base_path, "..", "config", "app_settings.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    ui_colors = cfg.get('ui', {}).get('colors', {})
                    if ui_colors.get('primary'):
                        self.colors['bg'] = ui_colors['primary']
                    if ui_colors.get('secondary'):
                        self.colors['title'] = ui_colors['secondary']
                        self.colors['icon'] = ui_colors['secondary']
        except Exception:
            pass

    def load_notification_icon(self):
        """Carga el ícono de notificaciones desde assets/icons/."""
        icon_path = os.path.join(self.base_path, "..", "assets", "icons", "notifications.png")
        try:
            img = Image.open(icon_path)
            # Ajustar tamaño del ícono (ancho, alto)
            img = img.resize((20, 20), Image.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img)
            return ctk_img
        except FileNotFoundError:
            print(f"Error: Ícono de notificación no encontrado en {icon_path}")
            return None
    
    def create_header(self):
        """Crea la estructura del header."""
        # Borde inferior
        self.configure(border_width=0)
        
        # ===== LADO IZQUIERDO =====
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=20)
        
        # Botón menú hamburguesa
        menu_btn = ctk.CTkButton(
            left_frame, text="☰", width=40, height=40,
            font=ctk.CTkFont(size=20), fg_color="transparent",
            text_color=self.colors["icon"], hover_color="#E2E8F0",
            command=self.on_menu_toggle if self.on_menu_toggle else lambda: None
        )
        menu_btn.pack(side="left", padx=(0, 15))
        
        # Títulos
        titles_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        titles_frame.pack(side="left", fill="y", pady=15)
        
        title_label = ctk.CTkLabel(
            titles_frame, text=self.title,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=self.colors["title"]
        )
        title_label.pack(anchor="w")
        
        if self.subtitle:
            subtitle_label = ctk.CTkLabel(
                titles_frame, text=self.subtitle,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=self.colors["subtitle"]
            )
            subtitle_label.pack(anchor="w")
        
        # ===== LADO DERECHO =====
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20)
        
        # Botón de notificaciones con badge
        notif_container = ctk.CTkFrame(right_frame, fg_color="transparent", width=45, height=45)
        notif_container.pack(side="right", pady=12)
        notif_container.pack_propagate(False)
        
        # Cargar ícono de notificación
        self.notification_icon_img = self.load_notification_icon()
        
        notif_btn = ctk.CTkButton(
            notif_container, 
            text="", # Quitamos el texto (emoji)
            width=40, height=40,
            font=ctk.CTkFont(size=18), fg_color="#F1F5F9",
            text_color=self.colors["icon"], hover_color="#E2E8F0",
            corner_radius=10,
            command=self.on_notifications if self.on_notifications else lambda: None,
            image=self.notification_icon_img # Añadir ícono
        )
        notif_btn.place(x=0, y=2)
        
        # Badge de notificaciones (Punto rojo sin número)
        if self.notification_count > 0:
            badge = ctk.CTkFrame(
                notif_container, width=12, height=12,
                fg_color=self.colors["notification_badge"],
                corner_radius=6
            )
            badge.place(x=28, y=2) # Ajustado para esquina superior derecha del ícono
    
    def update_title(self, title, subtitle=""):
        """Actualiza el título del header."""
        self.title = title
        self.subtitle = subtitle
        # Reconstruir
        for widget in self.winfo_children():
            widget.destroy()
        self.create_header()
    
    def update_notifications(self, count):
        """Actualiza el contador de notificaciones."""
        self.notification_count = count
        # Reconstruir
        for widget in self.winfo_children():
            widget.destroy()
        self.create_header()