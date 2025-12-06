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
from utils.logger import Logger

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
     self.state('zoomed')  # Primera llamada al maximizar
     self.minsize(1024, 600)
     self.configure(fg_color="#F8FAFC")
    
    # Crear layout
     self.create_layout()
    
    # ========= FORZAR MAXIMIZADO MÚLTIPLES VECES #ESTO ES PARA LAS VENTANAS NO APAREZCAN MAS CHICAS ========= 
     self.update_idletasks()
     self.state('zoomed')  # Segunda llamada
     self.after(10, lambda: self.state('zoomed'))  # Tercera llamada
     self.after(50, lambda: self.state('zoomed'))  # Cuarta llamada
     self.after(150, lambda: self.state('zoomed'))  # Quinta llamada
    # =====================================================
        
    
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
        # Start polling notifications to update header badge in real-time
        try:
            # initialize poller id
            self._poller_id = None
            self.start_notification_poller()
        except Exception:
            self._poller_id = None
            pass
        # Register for immediate alert notifications (real-time updates)
        try:
            from utils.alerts import alert_manager
            # add a listener that increments the header badge when a new alert arrives
            def _listener(alert):
                try:
                    # If it's a broadcast count update, set exactly that count
                    if isinstance(alert, dict) and alert.get('type') == 'count_update':
                        cnt = alert.get('count', None)
                        if cnt is not None:
                            try:
                                self.after(20, lambda: self.header.update_notifications(cnt))
                            except Exception:
                                pass
                        return

                    # Regular alert item -> increment the badge visually (schedule on mainloop)
                    def _inc():
                        try:
                            current = getattr(self.header, 'notification_count', None)
                            if current is None:
                                self.header.update_notifications(self.get_notification_count())
                            else:
                                self.header.update_notifications(current + 1)
                        except Exception:
                            try:
                                self.header.update_notifications(self.get_notification_count())
                            except Exception:
                                pass

                    try:
                        self.after(20, _inc)
                    except Exception:
                        pass
                except Exception:
                    pass

            # store listener to remove later
            self._alert_listener = _listener
            alert_manager.add_listener(self._alert_listener)
        except Exception:
            self._alert_listener = None
            pass
        
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
     """Navega a otra página manteniendo maximizado."""
     # Guardar user_data ANTES de destruir
     user_data = self.user_data
    
     self.destroy()
    
     # Crear nueva vista
     if page_id == "dashboard":
        from view.dashboard_view import DashboardView
        new_view = DashboardView(user_data)
     elif page_id == "inventario":
        from view.inventory_view import InventoryView
        new_view = InventoryView(user_data)
     elif page_id == "movimientos":
        from view.movements_view import MovementsView
        new_view = MovementsView(user_data)
     elif page_id == "reportes":
        from view.reports_view import ReportsView
        new_view = ReportsView(user_data)
     elif page_id == "usuarios":
        from view.users_view import UsersView
        new_view = UsersView(user_data)
      
     elif page_id == "configuracion":
        from view.settings_view import SettingsView
        new_view = SettingsView(user_data)
     elif page_id == "ayuda":
        from view.help_view import HelpView
        new_view = HelpView(user_data)
     else:
        return
    
    # Forzar maximizado antes de run()
     new_view.update()
     new_view.state('zoomed')
     new_view.run()
    
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
        
        # Botón para limpiar notificaciones antiguas (esquina superior derecha del popup)
        clean_btn = ctk.CTkButton(
            header_frame,
            text="🗑️ Limpiar",
            command=lambda: self.clean_old_notifications_popup(popup),
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            height=35,
            corner_radius=8,
            width=120
        )
        clean_btn.pack(side="right", padx=20, pady=12)

        
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
            
            
            def populate_notifications():
                # Limpiar contenido previo
                for w in content_frame.winfo_children():
                    w.destroy()

                notifs = alert_model.get_unread_alerts()
                if not notifs:
                    no_notif_label = ctk.CTkLabel(
                        content_frame,
                        text="No hay notificaciones nuevas",
                        font=ctk.CTkFont(size=14),
                        text_color="#6B7280"
                    )
                    no_notif_label.pack(expand=True)
                    return

                for alert in notifs:
                    # Frame para cada notificación
                    notif_frame = ctk.CTkFrame(
                        content_frame,
                        fg_color="#F8FAFC",
                        corner_radius=8,
                        border_width=1,
                        border_color="#E2E8F0"
                    )
                    notif_frame.pack(fill="x", pady=8)
                    inner_frame = ctk.CTkFrame(notif_frame, fg_color="transparent")
                    inner_frame.pack(fill="both", expand=True, padx=12, pady=12)
                    tipo_label = ctk.CTkLabel(
                        inner_frame,
                        text=f"[{alert.get('tipo', 'General')}]",
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color="#00B4D8"
                    )
                    tipo_label.pack(anchor="w")
                    desc_label = ctk.CTkLabel(
                        inner_frame,
                        text=alert.get('descripcion', 'Sin descripción'),
                        font=ctk.CTkFont(size=12),
                        text_color="#1E293B",
                        wraplength=420,
                        justify="left"
                    )
                    desc_label.pack(anchor="w", pady=(5, 0))
                    fecha_label = ctk.CTkLabel(
                        inner_frame,
                        text=alert.get('fecha_alerta', 'Fecha desconocida'),
                        font=ctk.CTkFont(size=10),
                        text_color="#9CA3AF"
                    )
                    fecha_label.pack(anchor="w", pady=(5, 0))

            # Botón refrescar (junto al botón limpiar)
            refresh_btn = ctk.CTkButton(
                header_frame,
                text="🔄",
                command=lambda: populate_notifications(),
                fg_color="#F1F5F9",
                hover_color="#E2E8F0",
                text_color="#475569",
                height=35,
                corner_radius=8,
                width=48
            )
            refresh_btn.pack(side="right", padx=(0, 8), pady=12)

            # Llenar inicialmente
            populate_notifications()
                    
                    
        except Exception as e:
            error_label = ctk.CTkLabel(
                content_frame,
                text="Error al cargar notificaciones",
                font=ctk.CTkFont(size=14),
                text_color="#EF4444"
            )
            error_label.pack(expand=True)
            Logger.log_error_exception(e, "BASE_VIEW")
        
        
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
    
    def clean_old_notifications_popup(self, popup):
        """Limpia todas las notificaciones manualmente desde el popup."""
        try:
            from tkinter import messagebox
            from model.alert_model import AlertModel
            
            # Confirmar con el usuario
            confirm = messagebox.askyesno(
                "Limpiar Notificaciones",
                "¿Está seguro que desea eliminar TODAS las notificaciones?\n\nEsta acción no se puede deshacer."
            )
            
            if not confirm:
                return
            
            # Marcar todas las alertas como leídas y luego eliminar las leídas
            alert_model = AlertModel()
            marked = alert_model.mark_all_as_read()
            # Luego eliminar las alertas (limpieza completa)
            deleted = alert_model.delete_read_alerts()
            
            if deleted > 0 or marked > 0:
                messagebox.showinfo(
                    "Limpieza Completada",
                    f"Se eliminaron {deleted} notificaciones correctamente."
                )
                # Cerrar el popup
                popup.destroy()
                # Forzar actualización del badge a 0 para evitar que aparezca número rojo
                try:
                    try:
                        self.header.update_notifications(0)
                    except Exception:
                        pass
                    # Re-evaluar en breve el conteo real y actualizar (por si hay race-conditions)
                    try:
                        # Also notify alert_manager listeners so UI can react immediately
                        try:
                            from utils.alerts import alert_manager
                            alert_manager.broadcast_count_update()
                        except Exception:
                            pass
                        # Re-evaluar en breve el conteo real y actualizar (por si hay race-conditions)
                        self.after(300, lambda: self.header.update_notifications(self.get_notification_count()))
                    except Exception:
                        pass
                except Exception:
                    pass
            else:
                messagebox.showinfo(
                    "Sin Notificaciones",
                    "No hay notificaciones para eliminar."
                )
                
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror(
                "Error",
                "No se pudieron eliminar las notificaciones."
            )
            Logger.log_error_exception(e, "BASE_VIEW")
    
    def get_notification_count(self):
        """Obtiene el número de notificaciones no leídas desde el modelo de alertas."""
        try:
            from model.alert_model import AlertModel
            alert_model = AlertModel()
            unread = alert_model.get_unread_alerts()
            return len(unread) if unread else 0
        except Exception as e:
            Logger.log_error_exception(e, "BASE_VIEW")
            return 0

    def start_notification_poller(self, interval_ms=5000):
        """Inicia un poller que actualiza el contador de notificaciones en el header cada X ms."""
        def _poll():
            try:
                cnt = self.get_notification_count()
                try:
                    if hasattr(self, 'header') and self.header:
                        self.header.update_notifications(cnt)
                except Exception:
                    pass
            except Exception as e:
                Logger.log_error_exception(e, "BASE_VIEW")
            finally:
                try:
                    # store id so it can be cancelled on destroy
                    self._poller_id = self.after(interval_ms, _poll)
                except Exception:
                    self._poller_id = None
                    pass
        # Lanzar el primer poll y save id
        try:
            self._poller_id = self.after(interval_ms, _poll)
        except Exception as e:
            self._poller_id = None
            Logger.log_error_exception(e, "BASE_VIEW")
    
    def run(self):
        self.mainloop()
    def destroy(self):
        """Limpia listeners registrados y destruye la ventana."""
        try:
            from utils.alerts import alert_manager
            if hasattr(self, '_alert_listener') and self._alert_listener:
                try:
                    alert_manager.remove_listener(self._alert_listener)
                except Exception:
                    pass
        except Exception:
            pass
        # Cancel notification poller if running to avoid after callbacks after destroy
        try:
            if hasattr(self, '_poller_id') and self._poller_id:
                try:
                    self.after_cancel(self._poller_id)
                except Exception:
                    pass
        except Exception:
            pass
        try:
            super().destroy()
        except Exception:
            # Fallback: call base destroy
            try:
                ctk.CTk.destroy(self)
            except Exception:
                pass