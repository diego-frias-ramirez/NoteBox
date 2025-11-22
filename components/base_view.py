"""
NoteBox - Clase Base para Vistas con Sidebar y Header
Ubicación: components/base_view.py

Todas las vistas (Dashboard, Inventario, etc.) heredan de esta clase
para tener automáticamente el sidebar y header.
"""

import customtkinter as ctk
from components.sidebar import Sidebar
from components.header import Header
import os

class BaseView(ctk.CTk):
    """Clase base para todas las vistas con sidebar y header."""
    
    def __init__(self, user_data, page_id="dashboard", page_title="Dashboard", 
                 page_subtitle="Bienvenido al sistema de gestión"):
        super().__init__()
        
        self.user_data = user_data
        self.page_id = page_id
        self.page_title = page_title
        self.page_subtitle = page_subtitle
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Configuración de ventana
        self.title(f"NoteBox - {page_title}")
        self.geometry("1280x720")
        self.minsize(1024, 600)
        self.configure(fg_color="#F8FAFC")
        
        # Centrar ventana
        self.center_window()
        
        # Crear layout
        self.create_layout()
    
    def center_window(self):
        self.update_idletasks()
        w, h = 1280, 720
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
    
    def create_layout(self):
        """Crea el layout principal con sidebar y header."""
        # ===== SIDEBAR (Izquierda) =====
        self.sidebar = Sidebar(
            self, 
            user_data=self.user_data,
            on_navigate=self.navigate_to,
            on_logout=self.logout,
            active_page=self.page_id
        )
        self.sidebar.pack(side="left", fill="y")
        
        # ===== CONTENEDOR PRINCIPAL (Derecha) =====
        self.main_container = ctk.CTkFrame(self, fg_color="#F8FAFC", corner_radius=0)
        self.main_container.pack(side="right", fill="both", expand=True)
        
        # ===== HEADER (Arriba) =====
        self.header = Header(
            self.main_container,
            title=self.page_title,
            subtitle=self.page_subtitle,
            on_menu_toggle=self.toggle_sidebar,
            on_notifications=self.show_notifications,
        )
        self.header.pack(fill="x")
        
        # ===== CONTENT AREA (Área de contenido) =====
        self.content_frame = ctk.CTkScrollableFrame(
            self.main_container, 
            fg_color="transparent",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Llamar al método que las subclases sobreescriben
        self.create_content()
    
    def create_content(self):
        """Método a sobreescribir por las subclases para crear el contenido."""
        pass
    
    def navigate_to(self, page_id):
        """Navega a otra página."""
        self.destroy()
        
        # Importar y abrir la vista correspondiente (USANDO LOS NOMBRES REALES DE TUS ARCHIVOS)
        if page_id == "dashboard":
            from view.dashboard_view import DashboardView
            DashboardView(self.user_data).run()
        elif page_id == "inventario":
            from view.inventory_view import InventoryView  # Clase debe coincidir con el archivo
            InventoryView(self.user_data).run()
        elif page_id == "movimientos":
            from view.movements_view import MovementsView
            MovementsView(self.user_data).run()
        elif page_id == "reportes":
            from view.reports_view import ReportsView
            ReportsView(self.user_data).run()
        elif page_id == "usuarios":
            from view.users_view import UsersView
            UsersView(self.user_data).run()
        elif page_id == "configuracion":
            from view.settings_view import SettingsView
            SettingsView(self.user_data).run()
        elif page_id == "ayuda":
            from view.help_view import HelpView
            HelpView(self.user_data).run()
    
    def logout(self):
        """Cierra sesión y vuelve al login."""
        # Eliminar archivo de sesión si existe
        session_file = os.path.join(self.base_path, "..", "temp", "session.json")
        if os.path.exists(session_file):
            os.remove(session_file)
        
        self.destroy()
        from view.login_view import NoteBoxLogin
        NoteBoxLogin().run()
    
    def toggle_sidebar(self):
        """Muestra/oculta el sidebar (para responsive)."""
        if self.sidebar.winfo_viewable():
            self.sidebar.pack_forget()
        else:
            self.sidebar.pack(side="left", fill="y", before=self.main_container)
    
    def show_notifications(self):
        """Muestra el panel de notificaciones."""
        # Implementar popup de notificaciones
        print("Mostrar notificaciones")
    
    def get_notification_count(self):
        """Obtiene el número de notificaciones (sobreescribir en subclases)."""
        return 0
    
    def run(self):
        self.mainloop()