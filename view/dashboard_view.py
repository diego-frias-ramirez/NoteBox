# view/dashboard_view.py

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox - Dashboard")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximizar ventana
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.create_layout()
    
    def create_layout(self):
        # === SIDEBAR ===
        sidebar = ctk.CTkFrame(self.root, width=240, fg_color="white", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo y título
        logo_frame = ctk.CTkFrame(sidebar, fg_color="white", height=80)
        logo_frame.pack(fill="x", pady=(20, 30))
        
        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="📦",
            font=("Segoe UI Emoji", 24)
        )
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
        
        # Menú de navegación
        menu_items = [
            ("📊", "Dashboard", True),
            ("📦", "Inventario", False),
            ("🔄", "Movimientos", False),
            ("📈", "Reportes", False),
            ("👥", "Usuarios", False),
            ("⚙️", "Configuración", False),
            ("❓", "Ayuda", False)
        ]
        
        for icon, text, active in menu_items:
            self.create_menu_item(sidebar, icon, text, active)
        
        # Usuario en footer
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
        
        logout_btn = ctk.CTkButton(
            user_frame,
            text="🚪",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#f8f9fa",
            corner_radius=6,
            font=("Segoe UI Emoji", 14)
        )
        logout_btn.pack(side="right")
        
        # === MAIN CONTENT ===
        main_container = ctk.CTkFrame(self.root, fg_color="#f8f9fa", corner_radius=0)
        main_container.pack(side="right", fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_container, fg_color="white", height=70, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
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
        
        # Notificaciones
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
        
        # Badge de notificación
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
        
        # Content scroll
        content = ctk.CTkScrollableFrame(
            main_container,
            fg_color="#f8f9fa",
            corner_radius=0
        )
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Banner de bienvenida
        banner = ctk.CTkFrame(content, fg_color="white", corner_radius=12, height=140)
        banner.pack(fill="x", pady=(0, 20))
        banner.pack_propagate(False)
        
        banner_text = ctk.CTkFrame(banner, fg_color="white")
        banner_text.pack(side="left", padx=40, pady=30)
        
        ctk.CTkLabel(
            banner_text,
            text="Hola ! bienvenido",
            font=("Arial", 32, "bold"),
            text_color="#2b2d42"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            banner_text,
            text="De nuevo Juan",
            font=("Arial", 32, "bold"),
            text_color="#2b2d42"
        ).pack(anchor="w")
        
        # Imagen de lápices (placeholder)
        banner_img = ctk.CTkLabel(
            banner,
            text="✏️🎨📐",
            font=("Segoe UI Emoji", 60),
            fg_color="#ffd6a5",
            corner_radius=12,
            width=400,
            height=100
        )
        banner_img.pack(side="right", padx=20, pady=20)
        
        # Grid de tarjetas (2 columnas)
        cards_row1 = ctk.CTkFrame(content, fg_color="transparent")
        cards_row1.pack(fill="x", pady=(0, 20))
        
        # Tarjeta 1: Productos Totales
        self.create_stat_card(
            cards_row1,
            "Productos Totales",
            "1,245",
            "↑ 12% vs. mes anterior",
            "📦",
            "#e8f4f8",
            "#00b4d8",
            True
        )
        
        # Tarjeta 2: Stock Bajo
        self.create_stat_card(
            cards_row1,
            "Stock Bajo",
            "23",
            "Requieren reabastecimiento",
            "📉",
            "#fff4e6",
            "#fb8500",
            False
        )
        
        cards_row2 = ctk.CTkFrame(content, fg_color="transparent")
        cards_row2.pack(fill="x", pady=(0, 20))
        
        # Tarjeta 3: Ventas del Día
        self.create_sales_card(cards_row2)
        
        # Tarjeta 4: Alertas Activas
        self.create_alert_card(cards_row2)
        
        # Grid inferior (Gráfico + Alertas)
        bottom_grid = ctk.CTkFrame(content, fg_color="transparent")
        bottom_grid.pack(fill="both", expand=True)
        
        # Gráfico de barras
        self.create_chart(bottom_grid)
        
        # Lista de alertas
        self.create_alerts_list(bottom_grid)
        
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
        """Crear item del menú lateral"""
        bg_color = "#e8f4f8" if active else "white"
        text_color = "#00b4d8" if active else "#6c757d"
        
        item = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=8,
            height=45
        )
        item.pack(fill="x", padx=15, pady=2)
        item.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            item,
            text=icon,
            font=("Segoe UI Emoji", 16),
            width=30
        )
        icon_label.pack(side="left", padx=(15, 10))
        
        text_label = ctk.CTkLabel(
            item,
            text=text,
            font=("Arial", 13, "bold" if active else "normal"),
            text_color=text_color,
            anchor="w"
        )
        text_label.pack(side="left", fill="x", expand=True)
    
    def create_stat_card(self, parent, title, value, subtitle, icon, bg_color, icon_color, is_left):
        """Crear tarjeta de estadística"""
        # Crear frame principal sin border si es la de la izquierda
        if is_left:
            card = ctk.CTkFrame(
                parent,
                fg_color="white",
                corner_radius=12
            )
        else:
            card = ctk.CTkFrame(
                parent,
                fg_color="white",
                corner_radius=12,
                border_width=2,
                border_color="#ffd60a"
            )
        
        if is_left:
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        else:
            card.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        content_frame = ctk.CTkFrame(card, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(content_frame, fg_color="white")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 13),
            text_color="#8d99ae",
            anchor="w"
        ).pack(side="left")
        
        icon_box = ctk.CTkLabel(
            header,
            text=icon,
            font=("Segoe UI Emoji", 24),
            fg_color=bg_color,
            corner_radius=8,
            width=40,
            height=40
        )
        icon_box.pack(side="right")
        
        # Value
        ctk.CTkLabel(
            content_frame,
            text=value,
            font=("Arial", 36, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w", pady=(10, 5))
        
        # Subtitle
        ctk.CTkLabel(
            content_frame,
            text=subtitle,
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w")
    
    def create_sales_card(self, parent):
        """Tarjeta de ventas"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#00b4d8",
            corner_radius=12
        )
        card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="Ventas del Día",
            font=("Arial", 13),
            text_color="white",
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text="💵",
            font=("Segoe UI Emoji", 24),
            text_color="white"
        ).pack(side="right")
        
        # Value
        ctk.CTkLabel(
            content,
            text="$12,450",
            font=("Arial", 36, "bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(10, 5))
        
        # Subtitle
        ctk.CTkLabel(
            content,
            text="45 transacciones",
            font=("Arial", 11),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")
    
    def create_alert_card(self, parent):
        """Tarjeta de alertas"""
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=12,
            border_width=2,
            border_color="#ef233c"
        )
        card.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        content = ctk.CTkFrame(card, fg_color="white")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header
        header = ctk.CTkFrame(content, fg_color="white")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="Alertas Activas",
            font=("Arial", 13),
            text_color="#8d99ae",
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text="⚠️",
            font=("Segoe UI Emoji", 24),
            fg_color="#fff0f0",
            corner_radius=8,
            width=40,
            height=40
        ).pack(side="right")
        
        # Value
        ctk.CTkLabel(
            content,
            text="8",
            font=("Arial", 36, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w", pady=(10, 5))
        
        # Subtitle
        ctk.CTkLabel(
            content,
            text="Revisar inventario",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w")
    
    def create_chart(self, parent):
        """Crear gráfico de barras"""
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=12
        )
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header
        header = ctk.CTkFrame(chart_frame, fg_color="white", height=60)
        header.pack(fill="x", padx=25, pady=(20, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Inventario por Categoría",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Gráfico con matplotlib
        fig = Figure(figsize=(6, 3.5), facecolor='white')
        ax = fig.add_subplot(111)
        
        categories = ['Papelería', 'Ferretería', 'Abarrotes', 'Limpieza', 'Otros']
        values = [450, 320, 280, 150, 100]
        
        bars = ax.bar(categories, values, color='#00b4d8', width=0.6)
        
        ax.set_ylim(0, 600)
        ax.set_ylabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_alerts_list(self, parent):
        """Lista de últimas alertas"""
        alerts_frame = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=12
        )
        alerts_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Header
        header = ctk.CTkFrame(alerts_frame, fg_color="white", height=60)
        header.pack(fill="x", padx=25, pady=(20, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Últimas Alertas",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Alertas
        alerts = [
            ("⚠️", "#fff4e6", "Stock bajo: Tornillo 1/2\"", "Quedan 8 unidades"),
            ("🔴", "#ffe5e5", "Producto agotado: Arroz 1kg", "0 unidades disponibles"),
            ("⚠️", "#fff4e6", "Sin movimiento: Pintura azul", "30 días sin rotación")
        ]
        
        for icon, bg, title, subtitle in alerts:
            alert_item = ctk.CTkFrame(
                alerts_frame,
                fg_color=bg,
                corner_radius=8,
                height=70
            )
            alert_item.pack(fill="x", padx=25, pady=5)
            alert_item.pack_propagate(False)
            
            ctk.CTkLabel(
                alert_item,
                text=icon,
                font=("Segoe UI Emoji", 20)
            ).pack(side="left", padx=15)
            
            text_frame = ctk.CTkFrame(alert_item, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True)
            
            ctk.CTkLabel(
                text_frame,
                text=title,
                font=("Arial", 12, "bold"),
                text_color="#2b2d42",
                anchor="w"
            ).pack(anchor="w", pady=(12, 2))
            
            ctk.CTkLabel(
                text_frame,
                text=subtitle,
                font=("Arial", 10),
                text_color="#6c757d",
                anchor="w"
            ).pack(anchor="w")
        
        # Ver todas
        ctk.CTkButton(
            alerts_frame,
            text="Ver todas las alertas →",
            fg_color="transparent",
            text_color="#00b4d8",
            hover_color="#f8f9fa",
            font=("Arial", 12),
            height=40
        ).pack(pady=(10, 20))


if __name__ == "__main__":
    root = ctk.CTk()
    app = DashboardView(root)
    root.mainloop()