"""
NoteBox - Componente Sidebar (Barra Lateral)
Ubicación: components/sidebar.py
"""

import customtkinter as ctk
from PIL import Image
from utils.logger import Logger
import os

class Sidebar(ctk.CTkFrame):
    """Barra lateral de navegación reutilizable."""
    
    def __init__(self, parent, user_data, on_navigate, on_logout, active_page="dashboard"):
        super().__init__(parent, fg_color="#FFFFFF", width=250, corner_radius=0)
        self.pack_propagate(False)
        
        self.user_data = user_data
        self.on_navigate = on_navigate
        self.on_logout = on_logout
        self.active_page = active_page
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Colores por defecto
        self.colors = {
            "bg": "#FFFFFF",
            "active_bg": "#E8F8F8",
            "active_text": "#00B4D8",
            "text": "#64748B",
            "hover": "#F1F5F9",
            "border": "#E2E8F0"
        }
        
        # Cargar colores personalizados desde app_settings.json
        self._load_custom_colors()
        
        # Menú items con rutas de iconos
        self.menu_items = [
            {"id": "dashboard", "label": "Dashboard", "icon": "dashboard.png"},
            {"id": "inventario", "label": "Inventario", "icon": "inventory.png"},
            {"id": "movimientos", "label": "Movimientos", "icon": "movements.png"},
            {"id": "reportes", "label": "Reportes", "icon": "reports.png"},
            {"id": "usuarios", "label": "Usuarios", "icon": "users.png"},
            {"id": "configuracion", "label": "Configuración", "icon": "settings.png"},
            {"id": "ayuda", "label": "Ayuda", "icon": "help.png"},
        ]
        
        self.menu_buttons = {}
        self.icon_images = {} # Diccionario para almacenar los objetos CTkImage de los iconos
        self.create_sidebar()
    
    
    def _load_custom_colors(self):
        """Carga colores personalizados desde app_settings.json."""
        try:
            import json
            config_path = os.path.join(self.base_path, "..", "config", "app_settings.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    ui_colors = cfg.get('ui', {}).get('colors', {})
                    if ui_colors.get('sidebar'):
                        self.colors['bg'] = ui_colors['sidebar']
                    if ui_colors.get('secondary'):
                        self.colors['active_text'] = ui_colors['secondary']
        except Exception:
            pass

    def load_logo(self):
        """Carga el logo desde assets."""
        logo_path = os.path.join(self.base_path, "..", "assets", "icons", "logo_2.png")
        try:
            img = Image.open(logo_path)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
        except FileNotFoundError:
            Logger.warning(f"Logo no encontrado en {logo_path}", "SIDEBAR")
            return None
    
    def load_icon(self, icon_filename):
        """Carga un ícono desde assets/icons/."""
        icon_path = os.path.join(self.base_path, "..", "assets", "icons", icon_filename)
        try:
            img = Image.open(icon_path)
            # Ajustar tamaño del ícono (ancho, alto)
            img = img.resize((20, 20), Image.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img)
            return ctk_img
        except FileNotFoundError:
            Logger.warning(f"Ícono no encontrado en {icon_path}", "SIDEBAR")
            return None
    
    def create_sidebar(self):
        """Crea la estructura del sidebar."""
        # ===== HEADER CON LOGO =====
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Logo
        logo_img = self.load_logo()
        if logo_img:
            logo_label = ctk.CTkLabel(header_frame, image=logo_img, text="")
            logo_label.pack(side="left", padx=(0, 10))
        
        # Título y subtítulo
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="y", pady=5)
        
        title = ctk.CTkLabel(
            title_frame, text="NoteBox",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#1E293B"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_frame, text="Admin Panel",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#94A3B8"
        )
        subtitle.pack(anchor="w")
        
        # ===== BUSCADOR =====
        search_frame = ctk.CTkFrame(self, fg_color="#F1F5F9", corner_radius=10, height=40)
        search_frame.pack(fill="x", padx=15, pady=(10, 20))
        search_frame.pack_propagate(False)
        
        search_icon_img = self.load_icon("search.png") # Asumiendo que tienes un search.png
        if search_icon_img:
            search_icon = ctk.CTkLabel(search_frame, image=search_icon_img, text="")
            search_icon.pack(side="left", padx=(12, 5))
        else:
            # Fallback si no hay ícono de búsqueda
            search_icon = ctk.CTkLabel(search_frame, text="🔍", font=ctk.CTkFont(size=14))
            search_icon.pack(side="left", padx=(12, 5))
        
        search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Buscar...",
            font=ctk.CTkFont(size=13), fg_color="transparent",
            border_width=0, text_color="#64748B", height=35
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # ===== MENÚ DE NAVEGACIÓN =====
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=10)
        
        for item in self.menu_items:
            btn = self.create_menu_button(menu_frame, item)
            self.menu_buttons[item["id"]] = btn
        
        # ===== FOOTER CON USUARIO =====
        self.create_user_footer()
    
    def create_menu_button(self, parent, item):
        """Crea un botón del menú."""
        is_active = item["id"] == self.active_page
        
        btn_frame = ctk.CTkFrame(
            parent, fg_color=self.colors["active_bg"] if is_active else "transparent",
            corner_radius=10, height=45
        )
        btn_frame.pack(fill="x", pady=2)
        btn_frame.pack_propagate(False)
        
        # Indicador activo (barra lateral)
        if is_active:
            indicator = ctk.CTkFrame(btn_frame, fg_color=self.colors["active_text"], 
                                      width=4, corner_radius=2)
            indicator.pack(side="left", fill="y", padx=(0, 0), pady=8)
        
        # Contenido del botón
        content = ctk.CTkFrame(btn_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15)
        
        # Cargar y mostrar el ícono
        icon_ctk = self.load_icon(item["icon"])
        if icon_ctk:
            icon_label = ctk.CTkLabel(content, image=icon_ctk, text="")
            icon_label.pack(side="left", padx=(0, 12))
            # Almacenar la imagen para evitar que sea recolectada por el garbage collector
            # y se pierda el ícono
            self.icon_images[item["id"]] = icon_ctk 
        else:
            # Fallback si no se encuentra el ícono
            icon_label = ctk.CTkLabel(content, text="📁", font=ctk.CTkFont(size=16))
            icon_label.pack(side="left", padx=(0, 12))
        
        label = ctk.CTkLabel(
            content, text=item["label"],
            font=ctk.CTkFont(family="Segoe UI", size=14, 
                            weight="bold" if is_active else "normal"),
            text_color=self.colors["active_text"] if is_active else self.colors["text"]
        )
        label.pack(side="left")
        
        # Eventos hover y click
        for widget in [btn_frame, content, icon_label, label]:
            widget.bind("<Enter>", lambda e, f=btn_frame, i=item: self.on_hover(f, i, True))
            widget.bind("<Leave>", lambda e, f=btn_frame, i=item: self.on_hover(f, i, False))
            widget.bind("<Button-1>", lambda e, i=item: self.navigate(i["id"]))
        
        return btn_frame
    
    def on_hover(self, frame, item, entering):
        """Maneja el hover de los botones."""
        if item["id"] != self.active_page:
            frame.configure(fg_color=self.colors["hover"] if entering else "transparent")
    
    def navigate(self, page_id):
        """Navega a una página."""
        if page_id != self.active_page:
            self.on_navigate(page_id)
    
    def create_user_footer(self):
        """Crea el footer con info del usuario."""
        # Separador
        sep = ctk.CTkFrame(self, fg_color=self.colors["border"], height=1)
        sep.pack(fill="x", padx=20, pady=(10, 0))
        
        # Frame usuario
        user_frame = ctk.CTkFrame(self, fg_color="transparent", height=70)
        user_frame.pack(fill="x", padx=15, pady=15)
        user_frame.pack_propagate(False)
        
        # Avatar
        avatar = ctk.CTkFrame(user_frame, width=40, height=40, 
                              fg_color="#E0F7FA", corner_radius=20)
        avatar.pack(side="left", padx=(5, 10))
        avatar.pack_propagate(False)
        
        # Icono de avatar genérico o cargar avatar del usuario si es posible
        avatar_icon_img = self.load_icon("user_avatar.png") # Asumiendo que tienes un user_avatar.png
        if avatar_icon_img:
            avatar_icon = ctk.CTkLabel(avatar, image=avatar_icon_img, text="")
            avatar_icon.place(relx=0.5, rely=0.5, anchor="center")
            self.icon_images['user_avatar'] = avatar_icon_img # Almacenar imagen
        else:
            avatar_icon = ctk.CTkLabel(avatar, text="👤", font=ctk.CTkFont(size=18))
            avatar_icon.place(relx=0.5, rely=0.5, anchor="center")
        
        # Info usuario
        info_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="y", pady=5)
        
        name_label = ctk.CTkLabel(
            info_frame, text=self.user_data.get('nombre', 'Usuario'),
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#1E293B"
        )
        name_label.pack(anchor="w")
        
        role_label = ctk.CTkLabel(
            info_frame, text=self.user_data.get('rol', 'Rol'),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#94A3B8"
        )
        role_label.pack(anchor="w")
        
        # Botón cerrar sesión
        logout_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        logout_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Icono de logout
        logout_icon_img = self.load_icon("logout.png") # Asumiendo que tienes un logout.png
        logout_btn = ctk.CTkButton(
            logout_frame, text="Cerrar Sesión", # Quitamos el emoji
            font=ctk.CTkFont(size=12), fg_color="transparent",
            text_color="#EF4444", hover_color="#FEE2E2",
            anchor="w", height=35, command=self.on_logout,
            image=logout_icon_img # Añadir ícono
        )
        if logout_icon_img:
            self.icon_images['logout'] = logout_icon_img # Almacenar imagen
        logout_btn.pack(fill="x")
    
    def set_active(self, page_id):
        """Cambia la página activa (para actualizar estilos)."""
        self.active_page = page_id
        # Reconstruir menú para actualizar estilos
        for widget in self.winfo_children():
            widget.destroy()
        self.icon_images = {} # Limpiar el diccionario de imágenes
        self.menu_buttons = {}
        self.create_sidebar()