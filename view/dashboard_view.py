"""
NoteBox - Vista del Dashboard
"""

import customtkinter as ctk
from PIL import Image
import os

# Configuración del tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class NoteBoxDashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()

        # Configuración de ventana
        self.title("NoteBox - Dashboard")
        self.geometry("1200x700")
        self.resizable(True, True)
        self.configure(fg_color="#F3F4F6")

        # Datos del usuario
        self.user_data = user_data

        # Centrar ventana
        self.center_window()

        # Crear controlador
        from controller.dashboard_controller import DashboardController
        self.controller = DashboardController(user_data)

        # Crear UI
        self.create_widgets()

        # Cargar datos del dashboard
        self.load_dashboard_data()

    def center_window(self):
        self.update_idletasks()
        w, h = 1200, 700
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def create_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=60)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        # Logo
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "icons", "logo.png")
        try:
            img = Image.open(logo_path)
            logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
            logo_label = ctk.CTkLabel(header_frame, image=logo_img, text="")
            logo_label.pack(side="left", padx=(0, 10))
        except FileNotFoundError:
            logo_label = ctk.CTkLabel(header_frame, text="📦", font=ctk.CTkFont(size=20))
            logo_label.pack(side="left", padx=(0, 10))

        # Título
        title = ctk.CTkLabel(
            header_frame, text="NoteBox - Dashboard",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#1a1a2e"
        )
        title.pack(side="left")

        # Espaciador
        ctk.CTkLabel(header_frame, text="").pack(side="left", expand=True)

        # Información del usuario
        user_info = ctk.CTkLabel(
            header_frame, text=f"{self.user_data['nombre']} ({self.user_data['rol']})",
            font=ctk.CTkFont(size=12),
            text_color="#6b7280"
        )
        user_info.pack(side="right", padx=(0, 10))

        # Contenido principal
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Sidebar (opcional)
        sidebar_frame = ctk.CTkFrame(content_frame, width=200, fg_color="#FFFFFF", corner_radius=10)
        sidebar_frame.pack(side="left", fill="y", padx=(0, 20))
        sidebar_frame.pack_propagate(False)

        # Botones del sidebar
        sidebar_buttons = [
            ("Dashboard", self.refresh_dashboard),
            ("Inventario", self.go_to_inventory),
            ("Movimientos", self.go_to_movements),
            ("Reportes", self.go_to_reports),
            ("Usuarios", self.go_to_users),
            ("Configuración", self.go_to_settings)
        ]

        for text, command in sidebar_buttons:
            btn = ctk.CTkButton(
                sidebar_frame, text=text, height=40,
                fg_color="transparent", text_color="#374151",
                hover_color="#F3F4F6", anchor="w",
                command=command
            )
            btn.pack(fill="x", pady=2, padx=10)

        # Área principal del dashboard
        self.main_area = ctk.CTkFrame(content_frame, fg_color="#FFFFFF", corner_radius=10)
        self.main_area.pack(side="right", fill="both", expand=True)

        # Contenido del dashboard (inicialmente vacío)
        self.dashboard_content = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.dashboard_content.pack(fill="both", expand=True, padx=20, pady=20)

    def load_dashboard_data(self):
        """Carga y muestra los datos del dashboard."""
        data = self.controller.get_dashboard_summary()

        # Limpiar contenido anterior
        for widget in self.dashboard_content.winfo_children():
            widget.destroy()

        # Mostrar resumen general
        summary_frame = ctk.CTkFrame(self.dashboard_content, fg_color="#FFFFFF", corner_radius=10)
        summary_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            summary_frame, text="Resumen General del Inventario",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        if data['inventory_summary']:
            # Mostrar estadísticas generales
            stats_frame = ctk.CTkFrame(summary_frame, fg_color="transparent")
            stats_frame.pack(fill="x", padx=20, pady=10)

            # Ejemplo de estadísticas (ajusta según tu modelo)
            total_products = data['inventory_summary'].get('total_productos', 0)
            available_products = data['inventory_summary'].get('productos_disponibles', 0)
            low_stock_products = data['inventory_summary'].get('productos_stock_bajo', 0)
            out_of_stock_products = data['inventory_summary'].get('productos_agotados', 0)

            stats = [
                ("Total de Productos", total_products),
                ("Disponibles", available_products),
                ("Stock Bajo", low_stock_products),
                ("Agotados", out_of_stock_products)
            ]

            for i, (label, value) in enumerate(stats):
                stat_frame = ctk.CTkFrame(stats_frame, fg_color="#F9FAFB", corner_radius=8)
                stat_frame.grid(row=0, column=i, padx=5, sticky="ew", ipady=10)
                stats_frame.grid_columnconfigure(i, weight=1)

                ctk.CTkLabel(
                    stat_frame, text=label,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#6B7280"
                ).pack(pady=2)

                ctk.CTkLabel(
                    stat_frame, text=str(value),
                    font=ctk.CTkFont(size=18, weight="bold"),
                    text_color="#111827"
                ).pack(pady=2)
        else:
            ctk.CTkLabel(
                summary_frame, text="No se pudieron cargar los datos del inventario",
                text_color="#EF4444"
            ).pack(pady=20)

        # Mostrar productos con stock bajo
        if data['low_stock_products']:
            low_stock_frame = ctk.CTkFrame(self.dashboard_content, fg_color="#FFFFFF", corner_radius=10)
            low_stock_frame.pack(fill="x", pady=(0, 20))

            ctk.CTkLabel(
                low_stock_frame, text="Productos con Stock Bajo",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=10)

            # Crear tabla (simplificada con CTkFrame)
            table_header = ctk.CTkFrame(low_stock_frame, fg_color="#F3F4F6")
            table_header.pack(fill="x", padx=20, pady=(0, 10))

            headers = ["Código", "Nombre", "Categoría", "Stock Actual", "Stock Mínimo"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(
                    table_header, text=header, width=100,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    anchor="w"
                ).grid(row=0, column=i, padx=5, sticky="w")

            for i, product in enumerate(data['low_stock_products'][:5]): # Mostrar solo los primeros 5
                row_frame = ctk.CTkFrame(low_stock_frame, fg_color="transparent")
                row_frame.pack(fill="x", padx=20, pady=2)

                values = [
                    product.get('codigo', 'N/A'),
                    product.get('nombre', 'N/A'),
                    product.get('categoria_nombre', 'N/A'),
                    str(product.get('stock', 0)),
                    str(product.get('stock_minimo', 0))
                ]

                for j, value in enumerate(values):
                    ctk.CTkLabel(
                        row_frame, text=value, width=100,
                        font=ctk.CTkFont(size=12),
                        anchor="w"
                    ).grid(row=0, column=j, padx=5, sticky="w")
        else:
            low_stock_frame = ctk.CTkFrame(self.dashboard_content, fg_color="#FFFFFF", corner_radius=10)
            low_stock_frame.pack(fill="x", pady=(0, 20))

            ctk.CTkLabel(
                low_stock_frame, text="No hay productos con stock bajo",
                font=ctk.CTkFont(size=14),
                text_color="#10B981"
            ).pack(pady=20)

        # Mostrar alertas activas (usando los datos del modelo)
        if data['active_alerts']:
            alerts_frame = ctk.CTkFrame(self.dashboard_content, fg_color="#FFFFFF", corner_radius=10)
            alerts_frame.pack(fill="x", pady=(0, 20))

            ctk.CTkLabel(
                alerts_frame, text="Alertas Activas",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=10)

            for alert in data['active_alerts'][:5]: # Mostrar solo las primeras 5
                alert_text = f"[{alert['tipo']}] {alert['descripcion']}"
                # Opcional: Si quieres que al hacer clic se marque como leída, necesitas el ID
                alert_label = ctk.CTkLabel(
                    alerts_frame, text=alert_text,
                    font=ctk.CTkFont(size=12),
                    text_color="#111827",
                    # command=lambda a_id=alert['id']: self.mark_alert_read(a_id) # Descomentar si se quiere esta funcionalidad
                )
                alert_label.pack(pady=2, padx=20, anchor="w")

        else:
            alerts_frame = ctk.CTkFrame(self.dashboard_content, fg_color="#FFFFFF", corner_radius=10)
            alerts_frame.pack(fill="x", pady=(0, 20))

            ctk.CTkLabel(
                alerts_frame, text="No hay alertas activas",
                font=ctk.CTkFont(size=14),
                text_color="#10B981"
            ).pack(pady=20)

    def refresh_dashboard(self):
        """Refresca los datos del dashboard."""
        self.load_dashboard_data()

    def go_to_inventory(self):
        """Lógica para ir al módulo de inventario."""
        self.show_message("Ir a Inventario", "info")

    def go_to_movements(self):
        """Lógica para ir al módulo de movimientos."""
        self.show_message("Ir a Movimientos", "info")

    def go_to_reports(self):
        """Lógica para ir al módulo de reportes."""
        self.show_message("Ir a Reportes", "info")

    def go_to_users(self):
        """Lógica para ir al módulo de usuarios."""
        self.show_message("Ir a Usuarios", "info")

    def go_to_settings(self):
        """Lógica para ir al módulo de configuración."""
        self.show_message("Ir a Configuración", "info")

    def mark_alert_read(self, alert_id):
        """Marca una alerta como leída."""
        success = self.controller.alert_model.mark_alert_as_read(alert_id) # Llama al modelo directamente
        if success:
            self.load_dashboard_data() # Refrescar datos
            # Opcional: Usar utils.alerts para mostrar mensaje de éxito
            from utils.alerts import alert_manager
            alert_manager.show_success("Éxito", "Alerta marcada como leída.")
        else:
            from utils.alerts import alert_manager
            alert_manager.show_error("Error", "No se pudo marcar la alerta como leída.")

    def show_message(self, msg, type="info"):
        """Muestra un mensaje temporal."""
        colors = {
            "success": "#10B981", "error": "#EF4444",
            "warning": "#F59E0B", "info": "#3B82F6"
        }

        popup = ctk.CTkToplevel(self)
        popup.title("")
        popup.geometry("300x100")
        popup.resizable(False, False)
        popup.configure(fg_color="#FFFFFF")
        popup.transient(self)
        popup.grab_set()

        # Centrar popup
        popup.update_idletasks()
        x = self.winfo_x() + (1200 - 300) // 2
        y = self.winfo_y() + (700 - 100) // 2
        popup.geometry(f"300x100+{x}+{y}")

        label = ctk.CTkLabel(
            popup, text=msg,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=colors.get(type, "#374151")
        )
        label.pack(expand=True)

        popup.after(2000, popup.destroy)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    # Para pruebas, usar un usuario de ejemplo
    example_user = {
        "id": 1,
        "nombre": "Administrador",
        "rol": "Admin",
        "estado": "Activo"
    }
    app = NoteBoxDashboard(example_user)
    app.run()