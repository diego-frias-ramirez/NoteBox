"""
NoteBox - Vista del Módulo de Notificaciones
Ubicación: view/notifications_view.py
"""

import customtkinter as ctk
from components.base_view import BaseView
from model.alert_model import AlertModel # Asumiendo que tienes este modelo
from utils.logger import Logger
# Opcional: Importar el gestor de alertas si necesitas funcionalidades específicas
# from utils.alerts import alert_manager

class NotificationsView(BaseView):
    """Vista del Módulo de Notificaciones."""

    def __init__(self, user_data):
        super().__init__(
            user_data=user_data,
            page_id="notificaciones", # Este ID debe coincidir con el del sidebar (si lo agregas ahí)
            page_title="Centro de Notificaciones",
            page_subtitle="Gestiona tus alertas y avisos"
        )
        
        # Instancia del modelo de alertas
        self.alert_model = AlertModel()

    def create_content(self):
        """Crea el contenido específico del módulo de notificaciones."""
        # Frame principal para el contenido
        content_frame = self.content_frame # Heredado de BaseView

        # Título principal
        title_label = ctk.CTkLabel(
            content_frame,
            text="Tus Notificaciones",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # Botón para marcar todas como leídas (opcional)
        mark_all_read_btn = ctk.CTkButton(
            content_frame,
            text="Marcar todas como leídas",
            command=self.mark_all_as_read,
            fg_color="transparent",
            border_width=1,
            text_color="#00B4D8",
            hover_color="#E0F7FA"
        )
        mark_all_read_btn.pack(anchor="e", pady=(0, 10))

        # Contenedor para la lista de notificaciones
        self.notifications_container = ctk.CTkScrollableFrame(content_frame, fg_color="transparent")
        self.notifications_container.pack(fill="both", expand=True)

        # Cargar notificaciones al crear el contenido
        self.load_notifications()

    def load_notifications(self):
        """Carga y muestra las notificaciones en el contenedor."""
        # Limpiar notificaciones anteriores
        for widget in self.notifications_container.winfo_children():
            widget.destroy()

        try:
            # Obtener notificaciones del modelo (pueden ser todas o solo las no leídas)
            # Por ejemplo, para cargar solo las no leídas:
            notifications = self.alert_model.get_unread_alerts()
            
            # O para cargar TODAS las alertas (como notificaciones):
            # notifications = self.alert_model.get_all_alerts()

            if not notifications:
                no_notifications_label = ctk.CTkLabel(
                    self.notifications_container,
                    text="No tienes notificaciones nuevas.",
                    font=ctk.CTkFont(size=16),
                    text_color="#6B7280"
                )
                no_notifications_label.pack(expand=True)
                return

            for alert in notifications:
                # Crear un frame para cada notificación
                notification_frame = ctk.CTkFrame(self.notifications_container, fg_color="#F8FAFC", corner_radius=8)
                notification_frame.pack(fill="x", pady=5, padx=5)

                # Contenido de la notificación
                content_inner = ctk.CTkFrame(notification_frame, fg_color="transparent")
                content_inner.pack(fill="both", expand=True, padx=15, pady=10)

                # Tipo y descripción
                type_label = ctk.CTkLabel(
                    content_inner,
                    text=f"[{alert.get('tipo', 'General')}]",
                    font=ctk.CTkFont(weight="bold"),
                    text_color="#00B4D8"
                )
                type_label.pack(anchor="w")

                description_label = ctk.CTkLabel(
                    content_inner,
                    text=alert.get('descripcion', 'Sin descripción'),
                    wraplength=600, # Ajusta según el ancho de tu frame
                    justify="left"
                )
                description_label.pack(anchor="w", pady=(5, 0))

                # Fecha (si está disponible)
                date_str = alert.get('fecha_alerta', 'Fecha desconocida')
                date_label = ctk.CTkLabel(
                    content_inner,
                    text=date_str,
                    font=ctk.CTkFont(size=11),
                    text_color="#9CA3AF"
                )
                date_label.pack(anchor="w", pady=(2, 0))

                # Botón para marcar como leída (individual)
                mark_read_btn = ctk.CTkButton(
                    content_inner,
                    text="Marcar como leída",
                    command=lambda a_id=alert['id']: self.mark_single_as_read(a_id),
                    width=100,
                    height=25,
                    font=ctk.CTkFont(size=11),
                    fg_color="transparent",
                    border_width=1,
                    text_color="#10B981",
                    hover_color="#D1FAE5"
                )
                mark_read_btn.pack(anchor="e", pady=(10, 0))

        except Exception as e:
            Logger.error(f"Error al cargar notificaciones: {e}", "NOTIFICATIONS_VIEW")
            error_label = ctk.CTkLabel(
                self.notifications_container,
                text="Error al cargar las notificaciones.",
                text_color="#EF4444"
            )
            error_label.pack(expand=True)


    def mark_single_as_read(self, alert_id):
        """Marca una sola notificación como leída."""
        try:
            success = self.alert_model.mark_alert_as_read(alert_id)
            if success:
                Logger.info(f"Notificación {alert_id} marcada como leída.", "NOTIFICATIONS_VIEW")
                # Refrescar la lista de notificaciones
                self.load_notifications()
                # Opcional: Actualizar el contador en el header
                # self.header.update_notifications(self.get_notification_count())
            else:
                Logger.warning(f"No se pudo marcar la notificación {alert_id} como leída.", "NOTIFICATIONS_VIEW")
        except Exception as e:
            Logger.error(f"Error al marcar notificación como leída: {e}", "NOTIFICATIONS_VIEW")


    def mark_all_as_read(self):
        """Marca todas las notificaciones como leídas."""
        try:
            # Obtener todas las alertas no leídas
            unread_alerts = self.alert_model.get_unread_alerts()
            if not unread_alerts:
                Logger.info("No hay notificaciones por marcar como leídas.", "NOTIFICATIONS_VIEW")
                return

            success_count = 0
            for alert in unread_alerts:
                if self.alert_model.mark_alert_as_read(alert['id']):
                    success_count += 1

            if success_count > 0:
                Logger.info(f"{success_count} notificaciones marcadas como leídas.", "NOTIFICATIONS_VIEW")
                # Refrescar la lista de notificaciones
                self.load_notifications()
                # Opcional: Actualizar el contador en el header
                # self.header.update_notifications(self.get_notification_count())
            else:
                Logger.warning("No se pudo marcar ninguna notificación como leída.", "NOTIFICATIONS_VIEW")

        except Exception as e:
            Logger.error(f"Error al marcar todas las notificaciones como leídas: {e}", "NOTIFICATIONS_VIEW")

    # Opcional: Método para obtener el contador de notificaciones no leídas
    def get_notification_count(self):
        """Obtiene el número de notificaciones no leídas."""
        try:
            unread_alerts = self.alert_model.get_unread_alerts()
            return len(unread_alerts) if unread_alerts else 0
        except Exception as e:
            Logger.error(f"Error al contar notificaciones no leídas: {e}", "NOTIFICATIONS_VIEW")
            return 0

if __name__ == "__main__":
    example_user = {"id": 1, "nombre": "Admin", "rol": "Admin"}
    app = NotificationsView(example_user)
    app.run()