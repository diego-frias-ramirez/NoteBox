"""
NoteBox - Vista del Módulo de Notificaciones
Ubicación: view/notifications_view.py
"""

import customtkinter as ctk
from components.base_view import BaseView
from model.alert_model import AlertModel
from utils.logger import Logger
from datetime import datetime

class NotificationsView(BaseView):
    """Vista del Módulo de Notificaciones."""

    def __init__(self, user_data):
        super().__init__(user_data)
        self.alert_model = AlertModel()
        self.show_only_unread = False  # Por defecto mostrar todas

    def create_content(self):
        """Crea el contenido de la vista de notificaciones."""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Header con título y controles
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="📬 Notificaciones del Sistema",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1E293B"
        )
        title_label.pack(side="left")

        # Controles a la derecha
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.pack(side="right")

        # Botón para alternar entre todas y no leídas
        self.toggle_btn = ctk.CTkButton(
            controls_frame,
            text="Mostrar solo no leídas",
            command=self.toggle_filter,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            height=35,
            corner_radius=8
        )
        self.toggle_btn.pack(side="left", padx=5)

        # Botón para refrescar
        refresh_btn = ctk.CTkButton(
            controls_frame,
            text="🔄 Refrescar",
            command=self.load_notifications,
            fg_color="#10B981",
            hover_color="#059669",
            height=35,
            corner_radius=8,
            width=120
        )
        refresh_btn.pack(side="left", padx=5)

        # Botón para marcar todas como leídas
        mark_all_read_btn = ctk.CTkButton(
            controls_frame,
            text="✓ Marcar todas como leídas",
            command=self.mark_all_as_read,
            fg_color="transparent",
            border_width=2,
            border_color="#00B4D8",
            text_color="#00B4D8",
            hover_color="#E0F7FA",
            height=35,
            corner_radius=8
        )
        mark_all_read_btn.pack(side="left", padx=5)

        # Botón para limpiar notificaciones antiguas
        clean_btn = ctk.CTkButton(
            controls_frame,
            text="🗑️ Limpiar Antiguas",
            command=self.clean_old_notifications,
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            height=35,
            corner_radius=8,
            width=160
        )
        clean_btn.pack(side="left", padx=5)

        # Contenedor para estadísticas
        stats_frame = ctk.CTkFrame(content_frame, fg_color="#F8FAFC", corner_radius=12)
        stats_frame.pack(fill="x", pady=(0, 15))

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Cargando estadísticas...",
            font=ctk.CTkFont(size=14),
            text_color="#64748B"
        )
        self.stats_label.pack(pady=12)

        # Contenedor scrollable para la lista de notificaciones
        self.notifications_container = ctk.CTkScrollableFrame(
            content_frame, 
            fg_color="transparent",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        self.notifications_container.pack(fill="both", expand=True)

        # Cargar notificaciones al crear el contenido
        self.load_notifications()

    def toggle_filter(self):
        """Alterna entre mostrar todas las notificaciones y solo las no leídas."""
        self.show_only_unread = not self.show_only_unread
        
        if self.show_only_unread:
            self.toggle_btn.configure(text="Mostrar todas")
        else:
            self.toggle_btn.configure(text="Mostrar solo no leídas")
        
        self.load_notifications()

    def get_alert_icon_and_color(self, tipo):
        """Retorna el icono y color según el tipo de alerta."""
        alert_types = {
            'Stock bajo': ('⚠️', '#F59E0B', '#FEF3C7'),
            'Producto agotado': ('🚫', '#EF4444', '#FEE2E2'),
            'Sin movimiento': ('📦', '#8B5CF6', '#EDE9FE'),
            'Entrada de inventario': ('📥', '#10B981', '#D1FAE5'),
            'Salida de inventario': ('📤', '#3B82F6', '#DBEAFE'),
        }
        
        return alert_types.get(tipo, ('ℹ️', '#6B7280', '#F3F4F6'))

    def format_date(self, fecha):
        """Formatea la fecha de manera amigable."""
        try:
            if isinstance(fecha, str):
                fecha_dt = datetime.fromisoformat(str(fecha).replace('Z', '+00:00'))
            else:
                fecha_dt = fecha
            
            now = datetime.now()
            diff = now - fecha_dt.replace(tzinfo=None)
            
            if diff.days == 0:
                if diff.seconds < 60:
                    return "Hace un momento"
                elif diff.seconds < 3600:
                    mins = diff.seconds // 60
                    return f"Hace {mins} minuto{'s' if mins > 1 else ''}"
                else:
                    hours = diff.seconds // 3600
                    return f"Hace {hours} hora{'s' if hours > 1 else ''}"
            elif diff.days == 1:
                return "Ayer"
            elif diff.days < 7:
                return f"Hace {diff.days} días"
            else:
                return fecha_dt.strftime("%d/%m/%Y %H:%M")
        except:
            return str(fecha)

    def load_notifications(self):
        """Carga y muestra las notificaciones en el contenedor."""
        # Limpiar notificaciones anteriores
        for widget in self.notifications_container.winfo_children():
            widget.destroy()

        try:
            # Obtener notificaciones según el filtro
            if self.show_only_unread:
                notifications = self.alert_model.get_unread_alerts()
            else:
                notifications = self.alert_model.get_all_alerts(limit=200)

            # Actualizar estadísticas
            total = len(notifications)
            unread = sum(1 for n in notifications if not n.get('leida', False))
            self.stats_label.configure(
                text=f"📊 Total: {total} notificaciones | 🔔 No leídas: {unread}"
            )

            if not notifications:
                no_notifications_frame = ctk.CTkFrame(
                    self.notifications_container,
                    fg_color="#F8FAFC",
                    corner_radius=12
                )
                no_notifications_frame.pack(fill="both", expand=True, pady=20)

                no_notifications_label = ctk.CTkLabel(
                    no_notifications_frame,
                    text="✨ No hay notificaciones" + (" nuevas" if self.show_only_unread else ""),
                    font=ctk.CTkFont(size=18),
                    text_color="#94A3B8"
                )
                no_notifications_label.pack(expand=True, pady=60)
                return

            for alert in notifications:
                self.create_notification_card(alert)

        except Exception as e:
            Logger.error(f"Error al cargar notificaciones: {e}", "NOTIFICATIONS_VIEW")
            error_label = ctk.CTkLabel(
                self.notifications_container,
                text="❌ Error al cargar las notificaciones.",
                text_color="#EF4444",
                font=ctk.CTkFont(size=16)
            )
            error_label.pack(expand=True, pady=20)

    def create_notification_card(self, alert):
        """Crea una tarjeta individual para una notificación."""
        is_read = alert.get('leida', False)
        tipo = alert.get('tipo', 'General')
        icon, color, bg_color = self.get_alert_icon_and_color(tipo)

        # Frame principal de la notificación
        notification_frame = ctk.CTkFrame(
            self.notifications_container,
            fg_color=bg_color if not is_read else "#F8FAFC",
            corner_radius=12,
            border_width=2 if not is_read else 0,
            border_color=color if not is_read else "transparent"
        )
        notification_frame.pack(fill="x", pady=6, padx=5)

        # Contenido interno
        content_inner = ctk.CTkFrame(notification_frame, fg_color="transparent")
        content_inner.pack(fill="both", expand=True, padx=20, pady=15)

        # Header con tipo e icono
        header_frame = ctk.CTkFrame(content_inner, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 8))

        type_label = ctk.CTkLabel(
            header_frame,
            text=f"{icon} {tipo}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=color
        )
        type_label.pack(side="left")

        # Badge de "No leída"
        if not is_read:
            unread_badge = ctk.CTkLabel(
                header_frame,
                text="NUEVO",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="white",
                fg_color=color,
                corner_radius=4,
                padx=8,
                pady=2
            )
            unread_badge.pack(side="left", padx=10)

        # Información del producto (si existe)
        if alert.get('producto_nombre'):
            product_frame = ctk.CTkFrame(content_inner, fg_color="transparent")
            product_frame.pack(fill="x", pady=(0, 5))

            product_label = ctk.CTkLabel(
                product_frame,
                text=f"🏷️ Producto: {alert['producto_nombre']} (Código: {alert.get('producto_codigo', 'N/A')})",
                font=ctk.CTkFont(size=13),
                text_color="#475569"
            )
            product_label.pack(side="left")

            if alert.get('producto_stock') is not None:
                stock_label = ctk.CTkLabel(
                    product_frame,
                    text=f"Stock: {alert['producto_stock']}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#0F172A",
                    fg_color="#E2E8F0",
                    corner_radius=6,
                    padx=10,
                    pady=4
                )
                stock_label.pack(side="right")

        # Descripción
        description_label = ctk.CTkLabel(
            content_inner,
            text=alert.get('descripcion', 'Sin descripción'),
            wraplength=900,
            justify="left",
            font=ctk.CTkFont(size=13),
            text_color="#1E293B"
        )
        description_label.pack(anchor="w", pady=(5, 8))

        # Footer con fecha y acciones
        footer_frame = ctk.CTkFrame(content_inner, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(5, 0))

        # Fecha
        date_str = self.format_date(alert.get('fecha_alerta', 'Fecha desconocida'))
        date_label = ctk.CTkLabel(
            footer_frame,
            text=f"🕐 {date_str}",
            font=ctk.CTkFont(size=12),
            text_color="#94A3B8"
        )
        date_label.pack(side="left")

        # Botón para marcar como leída (solo si no está leída)
        if not is_read:
            mark_read_btn = ctk.CTkButton(
                footer_frame,
                text="✓ Marcar como leída",
                command=lambda a_id=alert['id']: self.mark_single_as_read(a_id),
                width=140,
                height=28,
                font=ctk.CTkFont(size=12),
                fg_color=color,
                hover_color=color,
                corner_radius=6
            )
            mark_read_btn.pack(side="right")

    def mark_single_as_read(self, alert_id):
        """Marca una sola notificación como leída."""
        try:
            success = self.alert_model.mark_alert_as_read(alert_id)
            if success:
                Logger.info(f"Notificación {alert_id} marcada como leída.", "NOTIFICATIONS_VIEW")
                self.load_notifications()
            else:
                Logger.warning(f"No se pudo marcar la notificación {alert_id} como leída.", "NOTIFICATIONS_VIEW")
        except Exception as e:
            Logger.error(f"Error al marcar notificación como leída: {e}", "NOTIFICATIONS_VIEW")

    def mark_all_as_read(self):
        """Marca todas las notificaciones como leídas."""
        try:
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
                self.load_notifications()
            else:
                Logger.warning("No se pudo marcar ninguna notificación como leída.", "NOTIFICATIONS_VIEW")

        except Exception as e:
            Logger.error(f"Error al marcar todas las notificaciones como leídas: {e}", "NOTIFICATIONS_VIEW")

    def clean_old_notifications(self):
        """Limpia notificaciones antiguas (leídas y con más de 30 días)."""
        try:
            from tkinter import messagebox
            
            # Confirmar con el usuario
            confirm = messagebox.askyesno(
                "Limpiar Notificaciones Antiguas",
                "¿Está seguro que desea eliminar todas las notificaciones leídas con más de 30 días?\n\nEsta acción no se puede deshacer."
            )
            
            if not confirm:
                return
            
            # Eliminar alertas antiguas
            deleted = self.alert_model.delete_old_alerts(days=30)
            
            if deleted > 0:
                Logger.info(f"{deleted} notificaciones antiguas eliminadas.", "NOTIFICATIONS_VIEW")
                messagebox.showinfo(
                    "Limpieza Completada",
                    f"✓ Se eliminaron {deleted} notificaciones antiguas correctamente."
                )
                self.load_notifications()
            else:
                Logger.info("No hay notificaciones antiguas para eliminar.", "NOTIFICATIONS_VIEW")
                messagebox.showinfo(
                    "Sin Notificaciones Antiguas",
                    "No hay notificaciones leídas con más de 30 días para eliminar."
                )
                
        except Exception as e:
            Logger.error(f"Error al limpiar notificaciones antiguas: {e}", "NOTIFICATIONS_VIEW")
            from tkinter import messagebox
            messagebox.showerror(
                "Error",
                "No se pudieron eliminar las notificaciones antiguas."
            )

    def get_notification_count(self):
        """Obtiene el número de notificaciones no leídas."""
        try:
            unread_alerts = self.alert_model.get_unread_alerts()
            return len(unread_alerts) if unread_alerts else 0
        except Exception as e:
            Logger.error(f"Error al contar notificaciones no leídas: {e}", "NOTIFICATIONS_VIEW")
            return 0
