# view/help_view.py

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class HelpView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox - Ayuda")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Variables para switches
        self.stock_alerts = tk.BooleanVar(value=True)
        self.no_movement = tk.BooleanVar(value=True)
        self.backup_confirm = tk.BooleanVar(value=True)
        
        # Datos de notificaciones
        self.notifications = [
            ("warning", "⚠️", "Stock bajo detectado", "El producto 'Tornillo 1/2\"' tiene solo 8 unidades disponibles.", "Hace 5 minutos", "#fff4e6", "#ffc107"),
            ("critical", "📦", "Producto agotado", "El producto 'Arroz 1kg' se ha agotado completamente.", "Hace 15 minutos", "#ffe5e5", "#ef233c"),
            ("info", "📉", "Producto sin movimiento", "El producto 'Pintura Azul' lleva 45 días sin rotación.", "Hace 1 hora", "#e8f4f8", "#00b4d8"),
            ("success", "✓", "Backup completado", "El respaldo automático se realizó exitosamente.", "Hace 2 horas", "#d4edda", "#10b981"),
            ("warning", "⚠️", "Stock bajo detectado", "El producto 'Martillo' tiene solo 12 unidades disponibles.", "Hace 3 horas", "#fff4e6", "#ffc107"),
            ("info", "ℹ️", "Actualización disponible", "Hay una nueva versión del sistema disponible (v1.0.1).", "Hace 5 horas", "#e8f4f8", "#00b4d8"),
            ("success", "✓", "Entrada registrada", "Se registraron 50 unidades de 'Cuaderno A4'.", "Hace 1 día", "#d4edda", "#10b981"),
            ("warning", "⏰", "Recordatorio", "Es recomendable realizar un inventario físico mensual.", "Hace 2 días", "#fff4e6", "#ffc107"),
        ]
        
        self.create_layout()
    
    def create_layout(self):
        # === SIDEBAR ===
        sidebar = ctk.CTkFrame(self.root, width=240, fg_color="white", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="white", height=80)
        logo_frame.pack(fill="x", pady=(20, 30))
        
        logo_icon = ctk.CTkLabel(logo_frame, text="📦", font=("Segoe UI Emoji", 24))
        logo_icon.pack(side="left", padx=(20, 10))
        
        logo_text_frame = ctk.CTkFrame(logo_frame, fg_color="white")
        logo_text_frame.pack(side="left")
        
        ctk.CTkLabel(
            logo_text_frame,
            text="NoteBox",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_text_frame,
            text="Admin Panel",
            font=("Arial", 10),
            text_color="#8d99ae",
            anchor="w"
        ).pack(anchor="w")
        
        # Buscador
        search_frame = ctk.CTkFrame(sidebar, fg_color="white", height=50)
        search_frame.pack(fill="x", padx=15, pady=(0, 20))
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar...",
            height=40,
            font=("Arial", 12),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        search_entry.pack(fill="x")
        
        # Menú
        menu_items = [
            ("📊", "Dashboard", False),
            ("📦", "Inventario", False),
            ("🔄", "Movimientos", False),
            ("📈", "Reportes", False),
            ("👥", "Usuarios", False),
            ("⚙️", "Configuración", False),
            ("❓", "Ayuda", True)
        ]
        
        for icon, text, active in menu_items:
            self.create_menu_item(sidebar, icon, text, active)
        
        # Usuario
        user_frame = ctk.CTkFrame(sidebar, fg_color="white")
        user_frame.pack(side="bottom", fill="x", pady=20, padx=15)
        
        user_avatar = ctk.CTkFrame(
            user_frame,
            fg_color="#2b2d42",
            corner_radius=20,
            width=40,
            height=40
        )
        user_avatar.pack(side="left", padx=(0, 10))
        user_avatar.pack_propagate(False)
        
        ctk.CTkLabel(
            user_avatar,
            text="👤",
            font=("Segoe UI Emoji", 18),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        user_info = ctk.CTkFrame(user_frame, fg_color="white")
        user_info.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            user_info,
            text="Admin User",
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            user_info,
            text="Administrador",
            font=("Arial", 10),
            text_color="#8d99ae",
            anchor="w"
        ).pack(anchor="w")
        
        # === MAIN CONTENT ===
        main_container = ctk.CTkFrame(self.root, fg_color="#f8f9fa", corner_radius=0)
        main_container.pack(side="right", fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="white", height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_left = ctk.CTkFrame(header, fg_color="white")
        header_left.pack(side="left", padx=30, pady=15)
        
        ctk.CTkButton(
            header_left,
            text="☰",
            width=40,
            height=40,
            fg_color="transparent",
            text_color="#2b2d42",
            hover_color="#f8f9fa",
            font=("Arial", 20)
        ).pack(side="left", padx=(0, 20))
        
        header_text = ctk.CTkFrame(header_left, fg_color="white")
        header_text.pack(side="left")
        
        ctk.CTkLabel(
            header_text,
            text="Dashboard Principal",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_text,
            text="Bienvenido al sistema de gestión",
            font=("Arial", 12),
            text_color="#8d99ae",
            anchor="w"
        ).pack(anchor="w")
        
        # Notificación
        notif_btn = ctk.CTkButton(
            header,
            text="🔔",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#f8f9fa",
            font=("Segoe UI Emoji", 18),
            corner_radius=8
        )
        notif_btn.pack(side="right", padx=30)
        
        badge = ctk.CTkLabel(
            notif_btn,
            text="3",
            font=("Arial", 9, "bold"),
            text_color="white",
            fg_color="#ef233c",
            corner_radius=10,
            width=18,
            height=18
        )
        badge.place(relx=0.7, rely=0.2, anchor="center")
        
        # === CONTENT ===
        content = ctk.CTkScrollableFrame(main_container, fg_color="#f8f9fa")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # === TARJETAS DE RESUMEN (4 columnas) ===
        summary_row = ctk.CTkFrame(content, fg_color="transparent")
        summary_row.pack(fill="x", pady=(0, 20))
        
        # Total
        self.create_summary_card(summary_row, "Total", "8", "🔔", "#e8f4f8", 0)
        
        # No Leídas
        self.create_summary_card(summary_row, "No Leídas", "3", "🔔", "#e8f4f8", 1)
        
        # Advertencias
        self.create_summary_card(summary_row, "Advertencias", "3", "⚠️", "#fff4e6", 2)
        
        # Críticas
        self.create_summary_card(summary_row, "Críticas", "1", "📦", "#ffe5e5", 3)
        
        # === FILTROS Y ACCIONES ===
        filters_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12, height=80)
        filters_card.pack(fill="x", pady=(0, 20))
        filters_card.pack_propagate(False)
        
        filters_content = ctk.CTkFrame(filters_card, fg_color="white")
        filters_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Tabs de filtros
        tabs_frame = ctk.CTkFrame(filters_content, fg_color="white")
        tabs_frame.pack(side="left")
        
        tabs = [
            ("Todas", True),
            ("No leídas", False),
            ("Advertencias", False),
            ("Críticas", False)
        ]
        
        for i, (tab_text, active) in enumerate(tabs):
            bg = "#00b4d8" if active else "white"
            text_color = "white" if active else "#6c757d"
            
            tab_btn = ctk.CTkButton(
                tabs_frame,
                text=tab_text,
                width=100,
                height=40,
                font=("Arial", 12, "bold" if active else "normal"),
                fg_color=bg,
                text_color=text_color,
                hover_color="#0096c7" if active else "#f8f9fa",
                corner_radius=8,
                border_width=0 if active else 1,
                border_color="#e0e0e0"
            )
            tab_btn.pack(side="left", padx=(0 if i == 0 else 5, 0))
        
        # Acciones
        actions_frame = ctk.CTkFrame(filters_content, fg_color="white")
        actions_frame.pack(side="right")
        
        ctk.CTkLabel(
            actions_frame,
            text="Marcar todas como leídas",
            font=("Arial", 12),
            text_color="#6c757d",
            cursor="hand2"
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(
            actions_frame,
            text="🗑️ Limpiar",
            width=100,
            height=40,
            font=("Arial", 12),
            fg_color="white",
            text_color="#ef233c",
            border_width=1,
            border_color="#ef233c",
            hover_color="#ffe5e5",
            corner_radius=8
        ).pack(side="left")
        
        # === LISTA DE NOTIFICACIONES ===
        notifications_container = ctk.CTkFrame(content, fg_color="transparent")
        notifications_container.pack(fill="both", expand=True, pady=(0, 20))
        
        for notification in self.notifications:
            self.create_notification_card(notifications_container, notification)
        
        # === CONFIGURACIÓN DE NOTIFICACIONES ===
        config_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        config_card.pack(fill="x")
        
        config_content = ctk.CTkFrame(config_card, fg_color="white")
        config_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título
        ctk.CTkLabel(
            config_content,
            text="Configuración de Notificaciones",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 20))
        
        # Opción 1: Alertas de Stock Bajo
        option1 = ctk.CTkFrame(config_content, fg_color="white", height=70)
        option1.pack(fill="x", pady=(0, 15))
        option1.pack_propagate(False)
        
        option1_text = ctk.CTkFrame(option1, fg_color="white")
        option1_text.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            option1_text,
            text="Alertas de Stock Bajo",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            option1_text,
            text="Notificar cuando el stock esté por debajo del mínimo",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        switch1 = ctk.CTkSwitch(
            option1,
            text="",
            variable=self.stock_alerts,
            onvalue=True,
            offvalue=False,
            fg_color="#00b4d8",
            progress_color="#00b4d8",
            button_color="white",
            button_hover_color="#f0f0f0"
        )
        switch1.pack(side="right")
        
        # Opción 2: Productos sin Movimiento
        option2 = ctk.CTkFrame(config_content, fg_color="white", height=70)
        option2.pack(fill="x", pady=(0, 15))
        option2.pack_propagate(False)
        
        option2_text = ctk.CTkFrame(option2, fg_color="white")
        option2_text.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            option2_text,
            text="Productos sin Movimiento",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            option2_text,
            text="Notificar productos con más de 30 días sin rotación",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        switch2 = ctk.CTkSwitch(
            option2,
            text="",
            variable=self.no_movement,
            onvalue=True,
            offvalue=False,
            fg_color="#00b4d8",
            progress_color="#00b4d8",
            button_color="white",
            button_hover_color="#f0f0f0"
        )
        switch2.pack(side="right")
        
        # Opción 3: Confirmaciones de Backup
        option3 = ctk.CTkFrame(config_content, fg_color="white", height=70)
        option3.pack(fill="x")
        option3.pack_propagate(False)
        
        option3_text = ctk.CTkFrame(option3, fg_color="white")
        option3_text.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            option3_text,
            text="Confirmaciones de Backup",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            option3_text,
            text="Notificar cuando se complete un respaldo",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        switch3 = ctk.CTkSwitch(
            option3,
            text="",
            variable=self.backup_confirm,
            onvalue=True,
            offvalue=False,
            fg_color="#00b4d8",
            progress_color="#00b4d8",
            button_color="white",
            button_hover_color="#f0f0f0"
        )
        switch3.pack(side="right")
        
        # Footer
        footer = ctk.CTkLabel(
            main_container,
            text="NoteBox v1.0 - 2025",
            font=("Arial", 10),
            text_color="#adb5bd",
            fg_color="#f8f9fa",
            height=40
        )
        footer.pack(side="bottom", fill="x")
    
    def create_menu_item(self, parent, icon, text, active):
        """Crear item del menú"""
        bg_color = "#e8f4f8" if active else "white"
        text_color = "#00b4d8" if active else "#6c757d"
        
        item = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=8, height=45)
        item.pack(fill="x", padx=15, pady=2)
        item.pack_propagate(False)
        
        ctk.CTkLabel(
            item,
            text=icon,
            font=("Segoe UI Emoji", 16),
            width=30
        ).pack(side="left", padx=(15, 10))
        
        ctk.CTkLabel(
            item,
            text=text,
            font=("Arial", 13, "bold" if active else "normal"),
            text_color=text_color,
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
    
    def create_summary_card(self, parent, title, value, icon, bg_color, position):
        """Crear tarjeta de resumen"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        
        if position == 0:
            card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        elif position == 3:
            card.pack(side="left", fill="both", expand=True, padx=(8, 0))
        else:
            card.pack(side="left", fill="both", expand=True, padx=8)
        
        content = ctk.CTkFrame(card, fg_color="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="white")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 12),
            text_color="#8d99ae",
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=icon,
            font=("Segoe UI Emoji", 20),
            fg_color=bg_color,
            corner_radius=8,
            width=40,
            height=40
        ).pack(side="right")
        
        # Value
        ctk.CTkLabel(
            content,
            text=value,
            font=("Arial", 32, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w", pady=(10, 0))
    
    def create_notification_card(self, parent, notification):
        """Crear tarjeta de notificación"""
        notif_type, icon, title, description, time, bg_color, border_color = notification
        
        card = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=12,
            border_width=0,
            border_color=border_color
        )
        card.pack(fill="x", pady=(0, 10))
        
        # Barra lateral de color
        color_bar = ctk.CTkFrame(card, fg_color=border_color, width=5, corner_radius=0)
        color_bar.pack(side="left", fill="y")
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header con icono
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header,
            text=icon,
            font=("Segoe UI Emoji", 24)
        ).pack(side="left", padx=(0, 15))
        
        text_frame = ctk.CTkFrame(header, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Arial", 14, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        # Indicador de no leída
        if notif_type in ["warning", "critical", "info"]:
            unread_dot = ctk.CTkLabel(
                header,
                text="●",
                font=("Arial", 16),
                text_color="#00b4d8"
            )
            unread_dot.pack(side="right")
        
        # Descripción
        ctk.CTkLabel(
            content,
            text=description,
            font=("Arial", 12),
            text_color="#6c757d",
            anchor="w",
            wraplength=700
        ).pack(anchor="w", pady=(0, 10))
        
        # Footer con tiempo y acciones
        footer = ctk.CTkFrame(content, fg_color="transparent")
        footer.pack(fill="x")
        
        ctk.CTkLabel(
            footer,
            text=f"🕒 {time}",
            font=("Arial", 11),
            text_color="#6c757d"
        ).pack(side="left")
        
        actions = ctk.CTkFrame(footer, fg_color="transparent")
        actions.pack(side="right")
        
        if notif_type != "success":
            ctk.CTkLabel(
                actions,
                text="Marcar como leída",
                font=("Arial", 11),
                text_color="#00b4d8",
                cursor="hand2"
            ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            actions,
            text="Eliminar",
            font=("Arial", 11),
            text_color="#ef233c",
            cursor="hand2"
        ).pack(side="left")


if __name__ == "__main__":
    root = ctk.CTk()
    app = HelpView(root)
    root.mainloop()