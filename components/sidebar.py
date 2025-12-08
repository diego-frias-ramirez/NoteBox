"""
NoteBox - Componente Sidebar (Barra Lateral) con Chat AI
Ubicación: components/sidebar.py
"""

import customtkinter as ctk
from PIL import Image
import os

class Sidebar(ctk.CTkFrame):
    """Barra lateral de navegación reutilizable con Chat AI."""

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
        self.icon_images = {}
        self.chat_ai_window = None  # Referencia a la ventana de chat
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
            print(f"Error: Logo no encontrado en {logo_path}")
            return None

    def load_icon(self, icon_filename):
        """Carga un ícono desde assets/icons/."""
        icon_path = os.path.join(self.base_path, "..", "assets", "icons", icon_filename)
        try:
            img = Image.open(icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img)
            return ctk_img
        except FileNotFoundError:
            print(f"Error: Ícono no encontrado en {icon_path}")
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

        # ===== BOTÓN CHAT AI =====
        chat_ai_button = ctk.CTkButton(
            self,
            text="💬 Chat AI",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#00B4D8",
            hover_color="#0096C7",
            corner_radius=10,
            height=45,
            command=self.open_chat_ai
        )
        chat_ai_button.pack(fill="x", padx=15, pady=(10, 20))

        # ===== MENÚ DE NAVEGACIÓN =====
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=10)

        for item in self.menu_items:
            btn = self.create_menu_button(menu_frame, item)
            self.menu_buttons[item["id"]] = btn

        # ===== FOOTER CON USUARIO =====
        self.create_user_footer()

    def open_chat_ai(self):
        """Abre la ventana de Chat AI."""
        # Si ya existe una ventana, la traemos al frente
        if self.chat_ai_window and self.chat_ai_window.winfo_exists():
            self.chat_ai_window.lift()
            self.chat_ai_window.focus_force()
            self.chat_ai_window.attributes('-topmost', True)
            self.chat_ai_window.after(100, lambda: self.chat_ai_window.attributes('-topmost', False))
            return

        # Importar el módulo de IA
        try:
            from components.ia import ChatAIWindow
            self.chat_ai_window = ChatAIWindow(self, self.user_data)
            
            # Forzar que la ventana aparezca al frente
            self.chat_ai_window.lift()
            self.chat_ai_window.focus_force()
            self.chat_ai_window.attributes('-topmost', True)
            self.chat_ai_window.after(100, lambda: self.chat_ai_window.attributes('-topmost', False))
            
        except ImportError as e:
            print(f"Error al importar ChatAIWindow: {e}")
            # Mostrar mensaje de error al usuario
            error_win = ctk.CTkToplevel(self)
            error_win.geometry("350x150")
            error_win.title("Error")
            error_win.grab_set()
            
            # Forzar ventana de error al frente también
            error_win.lift()
            error_win.focus_force()
            error_win.attributes('-topmost', True)
            
            error_win.update_idletasks()
            x = (error_win.winfo_screenwidth() - error_win.winfo_width()) // 2
            y = (error_win.winfo_screenheight() - error_win.winfo_height()) // 2
            error_win.geometry(f"+{x}+{y}")
            
            label = ctk.CTkLabel(
                error_win,
                text="Error: No se pudo cargar\nel módulo de Chat AI",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            label.pack(expand=True, pady=20)
            
            ok_btn = ctk.CTkButton(
                error_win,
                text="OK",
                width=100,
                command=error_win.destroy
            )
            ok_btn.pack(pady=(0, 20))

    def create_menu_button(self, parent, item):
        is_active = item["id"] == self.active_page

        btn_frame = ctk.CTkFrame(
            parent, fg_color=self.colors["active_bg"] if is_active else "transparent",
            corner_radius=10, height=45
        )
        btn_frame.pack(fill="x", pady=2)
        btn_frame.pack_propagate(False)

        if is_active:
            indicator = ctk.CTkFrame(btn_frame, fg_color=self.colors["active_text"], width=4, corner_radius=2)
            indicator.pack(side="left", fill="y", padx=(0, 0), pady=8)

        content = ctk.CTkFrame(btn_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15)

        icon_ctk = self.load_icon(item["icon"])
        if icon_ctk:
            icon_label = ctk.CTkLabel(content, image=icon_ctk, text="")
            icon_label.pack(side="left", padx=(0, 12))
            self.icon_images[item["id"]] = icon_ctk
        else:
            icon_label = ctk.CTkLabel(content, text="📁", font=ctk.CTkFont(size=16))
            icon_label.pack(side="left", padx=(0, 12))

        label = ctk.CTkLabel(
            content, text=item["label"],
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold" if is_active else "normal"),
            text_color=self.colors["active_text"] if is_active else self.colors["text"]
        )
        label.pack(side="left")

        for widget in [btn_frame, content, icon_label, label]:
            widget.bind("<Enter>", lambda e, f=btn_frame, i=item: self.on_hover(f, i, True))
            widget.bind("<Leave>", lambda e, f=btn_frame, i=item: self.on_hover(f, i, False))
            widget.bind("<Button-1>", lambda e, i=item: self.navigate(i["id"]))

        return btn_frame

    def on_hover(self, frame, item, entering):
        if item["id"] != self.active_page:
            frame.configure(fg_color=self.colors["hover"] if entering else "transparent")

    def navigate(self, page_id):
        if page_id != self.active_page:
            self.on_navigate(page_id)

    def create_user_footer(self):
        sep = ctk.CTkFrame(self, fg_color=self.colors["border"], height=1)
        sep.pack(fill="x", padx=20, pady=(10, 0))

        user_frame = ctk.CTkFrame(self, fg_color="transparent", height=70)
        user_frame.pack(fill="x", padx=15, pady=15)
        user_frame.pack_propagate(False)

        avatar = ctk.CTkFrame(user_frame, width=40, height=40, fg_color="#E0F7FA", corner_radius=20)
        avatar.pack(side="left", padx=(5, 10))
        avatar.pack_propagate(False)

        avatar_icon_img = self.load_icon("user_avatar.png")
        if avatar_icon_img:
            avatar_icon = ctk.CTkLabel(avatar, image=avatar_icon_img, text="")
            avatar_icon.place(relx=0.5, rely=0.5, anchor="center")
            self.icon_images['user_avatar'] = avatar_icon_img
        else:
            avatar_icon = ctk.CTkLabel(avatar, text="👤", font=ctk.CTkFont(size=18))
            avatar_icon.place(relx=0.5, rely=0.5, anchor="center")

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

        logout_icon_img = self.load_icon("logout.png")
        logout_btn = ctk.CTkButton(
            logout_frame,
            text="Cerrar Sesión",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color="#EF4444",
            hover_color="#FEE2E2",
            anchor="w",
            height=35,
            image=logout_icon_img,
            command=self.confirm_logout
        )
        if logout_icon_img:
            self.icon_images['logout'] = logout_icon_img
        logout_btn.pack(fill="x")

    def confirm_logout(self):
        """Muestra confirmación centrada antes de cerrar sesión."""
        confirm_win = ctk.CTkToplevel(self)
        confirm_win.geometry("300x150")
        confirm_win.title("Confirmar")
        confirm_win.grab_set()

        confirm_win.update_idletasks()
        x = (confirm_win.winfo_screenwidth() - confirm_win.winfo_width()) // 2
        y = (confirm_win.winfo_screenheight() - confirm_win.winfo_height()) // 2
        confirm_win.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(
            confirm_win,
            text="¿Deseas cerrar sesión?",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(expand=True, pady=(30, 10))

        btn_frame = ctk.CTkFrame(confirm_win, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        yes_btn = ctk.CTkButton(
            btn_frame, text="Sí", width=80, fg_color="#22C55E",
            hover_color="#4ADE80",
            command=lambda: self.logout_and_farewell(confirm_win)
        )
        yes_btn.pack(side="left", padx=10)

        no_btn = ctk.CTkButton(
            btn_frame, text="No", width=80, fg_color="#EF4444",
            hover_color="#F87171",
            command=confirm_win.destroy
        )
        no_btn.pack(side="left", padx=10)

    def logout_and_farewell(self, confirm_win):
        """Muestra mensaje de despedida y luego cierra sesión."""
        confirm_win.destroy()

        farewell_win = ctk.CTkToplevel(self)
        farewell_win.geometry("300x150")
        farewell_win.title("Nos vemos")
        farewell_win.grab_set()

        farewell_win.update_idletasks()
        x = (farewell_win.winfo_screenwidth() - farewell_win.winfo_width()) // 2
        y = (farewell_win.winfo_screenheight() - farewell_win.winfo_height()) // 2
        farewell_win.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(
            farewell_win,
            text="¡Nos vemos! 👋",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(expand=True)

        farewell_win.after(1500, lambda: [farewell_win.destroy(), self.on_logout()])

    def set_active(self, page_id):
        self.active_page = page_id
        for widget in self.winfo_children():
            widget.destroy()
        self.icon_images = {}
        self.menu_buttons = {}
        self.create_sidebar()