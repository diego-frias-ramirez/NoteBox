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
            notification_count=self.get_notification_count()
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
        """Muestra un popup con las notificaciones."""
        # Crear ventana modal
        popup = ctk.CTkToplevel(self)
        popup.title("Notificaciones")
        popup.geometry("500x600")
        popup.resizable(True, True)
        popup.configure(fg_color="#FAFAFA")
        
        # Centrar popup respecto a la ventana principal
        popup.transient(self)
        popup.grab_set()
        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 500) // 2
        y = self.winfo_y() + (self.winfo_height() - 600) // 2
        popup.geometry(f"+{x}+{y}")
        
        # Header del popup
        header_frame = ctk.CTkFrame(popup, fg_color="#FFFFFF", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="Notificaciones",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1E293B"
        ).pack(side="left", padx=20, pady=15)
        
        # Contenedor de notificaciones
        content_frame = ctk.CTkScrollableFrame(
            popup,
            fg_color="transparent",
            scrollbar_button_color="#CBD5E1"
        )
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Obtener notificaciones
        try:
            from model.alert_model import AlertModel
            alert_model = AlertModel()
            notifications = alert_model.get_unread_alerts()
            
            if not notifications:
                no_notif_label = ctk.CTkLabel(
                    content_frame,
                    text="No hay notificaciones nuevas",
                    font=ctk.CTkFont(size=14),
                    text_color="#6B7280"
                )
                no_notif_label.pack(expand=True)
            else:
                for alert in notifications:
                    # Frame para cada notificación
                    notif_frame = ctk.CTkFrame(
                        content_frame,
                        fg_color="#F8FAFC",
                        corner_radius=8,
                        border_width=1,
                        border_color="#E2E8F0"
                    )
                    notif_frame.pack(fill="x", pady=8)
                    
                    # Contenido
                    inner_frame = ctk.CTkFrame(notif_frame, fg_color="transparent")
                    inner_frame.pack(fill="both", expand=True, padx=12, pady=12)
                    
                    # Tipo de alerta
                    tipo_label = ctk.CTkLabel(
                        inner_frame,
                        text=f"[{alert.get('tipo', 'General')}]",
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color="#00B4D8"
                    )
                    tipo_label.pack(anchor="w")
                    
                    # Descripción
                    desc_label = ctk.CTkLabel(
                        inner_frame,
                        text=alert.get('descripcion', 'Sin descripción'),
                        font=ctk.CTkFont(size=12),
                        text_color="#1E293B",
                        wraplength=420,
                        justify="left"
                    )
                    desc_label.pack(anchor="w", pady=(5, 0))
                    
                    # Fecha
                    fecha_label = ctk.CTkLabel(
                        inner_frame,
                        text=alert.get('fecha_alerta', 'Fecha desconocida'),
                        font=ctk.CTkFont(size=10),
                        text_color="#9CA3AF"
                    )
                    fecha_label.pack(anchor="w", pady=(5, 0))
                    
        except Exception as e:
            error_label = ctk.CTkLabel(
                content_frame,
                text="Error al cargar notificaciones",
                font=ctk.CTkFont(size=14),
                text_color="#EF4444"
            )
            error_label.pack(expand=True)
            print(f"Error en show_notifications: {e}")
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            popup,
            text="Cerrar",
            command=popup.destroy,
            fg_color="#00B4D8",
            text_color="white",
            hover_color="#0099B3",
            height=35
        )
        close_btn.pack(fill="x", padx=15, pady=(0, 15))
    
    def get_notification_count(self):
        """Obtiene el número de notificaciones (sobreescribir en subclases)."""
        return 0
    
    def run(self):
        self.mainloop()