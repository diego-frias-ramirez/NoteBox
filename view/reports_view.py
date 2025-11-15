# view/reports_view.py

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ReportsView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox - Reportes")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Datos de ejemplo
        self.low_rotation_products = [
            ("📦", "Pintura Azul", "45 días", 12, "Atención Requerida"),
            ("📦", "Cable Ethernet 10m", "38 días", 8, "Atención Requerida"),
            ("📦", "Jabón Líquido 2L", "32 días", 5, "Atención Requerida"),
            ("📦", "Cinta Adhesiva", "28 días", 15, "Atención Requerida"),
            ("📦", "Pegamento Blanco", "25 días", 10, "Atención Requerida"),
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
            ("📈", "Reportes", True),
            ("👥", "Usuarios", False),
            ("⚙️", "Configuración", False),
            ("❓", "Ayuda", False)
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
        
        # === GENERADOR DE REPORTES ===
        report_generator = ctk.CTkFrame(content, fg_color="white", corner_radius=12, height=100)
        report_generator.pack(fill="x", pady=(0, 20))
        report_generator.pack_propagate(False)
        
        gen_content = ctk.CTkFrame(report_generator, fg_color="white")
        gen_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Título y descripción
        title_frame = ctk.CTkFrame(gen_content, fg_color="white")
        title_frame.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            title_frame,
            text="Generar Reportes",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Exporte datos en diferentes formatos",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        # Filtros de fecha
        filters_frame = ctk.CTkFrame(gen_content, fg_color="white")
        filters_frame.pack(side="left", padx=(40, 20))
        
        date_from = ctk.CTkEntry(
            filters_frame,
            placeholder_text="📅 Desde",
            width=140,
            height=40,
            font=("Arial", 12),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        date_from.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(filters_frame, text="-", font=("Arial", 16), text_color="#6c757d").pack(side="left", padx=5)
        
        date_to = ctk.CTkEntry(
            filters_frame,
            placeholder_text="📅 Hasta",
            width=140,
            height=40,
            font=("Arial", 12),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        date_to.pack(side="left", padx=(10, 0))
        
        # Botones de exportación
        export_frame = ctk.CTkFrame(gen_content, fg_color="white")
        export_frame.pack(side="right")
        
        ctk.CTkButton(
            export_frame,
            text="📄 PDF",
            width=100,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#ef233c",
            hover_color="#dc2626",
            corner_radius=8
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            export_frame,
            text="📊 Excel",
            width=100,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#10b981",
            hover_color="#059669",
            corner_radius=8
        ).pack(side="left")
        
        # === GRÁFICOS (2 columnas) ===
        charts_row = ctk.CTkFrame(content, fg_color="transparent")
        charts_row.pack(fill="x", pady=(0, 20))
        
        # Gráfico de línea - Evolución del Inventario
        self.create_line_chart(charts_row)
        
        # Gráfico de pie - Distribución por Categoría
        self.create_pie_chart(charts_row)
        
        # === TARJETAS DE MÉTRICAS (4 columnas) ===
        metrics_row = ctk.CTkFrame(content, fg_color="transparent")
        metrics_row.pack(fill="x", pady=(0, 20))
        
        # Métrica 1: Valor Total
        self.create_metric_card(
            metrics_row,
            "Valor Total",
            "$45,230",
            "↗ 8.5%",
            "📦",
            "#e8f4f8",
            "#10b981",
            0
        )
        
        # Métrica 2: Rotación
        self.create_metric_card(
            metrics_row,
            "Rotación",
            "4.2x",
            "Mensual",
            "📈",
            "#e8f4f8",
            "#6c757d",
            1
        )
        
        # Métrica 3: Cobertura
        self.create_metric_card(
            metrics_row,
            "Cobertura",
            "45 días",
            "Promedio",
            "📅",
            "#fff4e6",
            "#6c757d",
            2
        )
        
        # Métrica 4: Sin Rotación
        self.create_metric_card(
            metrics_row,
            "Sin Rotación",
            "12",
            "+30 días",
            "📉",
            "#fee",
            "#ef233c",
            3
        )
        
        # === SECCIÓN INFERIOR (Tabla + Imagen) ===
        bottom_row = ctk.CTkFrame(content, fg_color="transparent")
        bottom_row.pack(fill="both", expand=True)
        
        # Tabla de productos de baja rotación
        table_frame = ctk.CTkFrame(bottom_row, fg_color="white", corner_radius=12)
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        table_content = ctk.CTkFrame(table_frame, fg_color="white")
        table_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Título tabla
        ctk.CTkLabel(
            table_content,
            text="Productos de Baja Rotación",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(
            table_content,
            text="Productos sin movimiento en los últimos 30 días",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(fill="x", pady=(0, 20))
        
        # Headers
        headers_frame = ctk.CTkFrame(table_content, fg_color="#f8f9fa", height=45, corner_radius=8)
        headers_frame.pack(fill="x", pady=(0, 10))
        headers_frame.pack_propagate(False)
        
        headers = ["Producto", "Días sin Movimiento", "Stock Actual", "Estado"]
        widths = [250, 150, 120, 150]
        
        for header, width in zip(headers, widths):
            ctk.CTkLabel(
                headers_frame,
                text=header,
                font=("Arial", 11, "bold"),
                text_color="#2b2d42",
                width=width,
                anchor="w"
            ).pack(side="left", padx=10)
        
        # Productos
        products_list = ctk.CTkScrollableFrame(table_content, fg_color="white", height=250)
        products_list.pack(fill="both", expand=True, pady=(0, 15))
        
        for product in self.low_rotation_products:
            self.create_product_row(products_list, product, widths)
        
        # Link ver más
        ctk.CTkLabel(
            table_content,
            text="Ver informe completo →",
            font=("Arial", 12),
            text_color="#00b4d8",
            cursor="hand2",
            anchor="w"
        ).pack(fill="x")
        
        # Imagen "Más Vendido"
        image_frame = ctk.CTkFrame(bottom_row, fg_color="#ffeaa7", corner_radius=12)
        image_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        image_content = ctk.CTkFrame(image_frame, fg_color="transparent")
        image_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Badge "Más Vendido"
        badge_frame = ctk.CTkFrame(image_content, fg_color="white", corner_radius=20, height=50)
        badge_frame.pack(pady=(10, 0))
        
        ctk.CTkLabel(
            badge_frame,
            text="Más Vendido",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42"
        ).pack(padx=30, pady=12)
        
        # Emoji de celebración
        ctk.CTkLabel(
            image_content,
            text="🎉📦",
            font=("Segoe UI Emoji", 40)
        ).pack(side="top", anchor="ne", padx=20)
        
        # Placeholder para imagen de producto
        product_display = ctk.CTkLabel(
            image_content,
            text="🖊️✏️📝\n\nPAPELERÍA\nMÁS VENDIDA",
            font=("Arial", 24, "bold"),
            text_color="#2b2d42",
            justify="center"
        )
        product_display.pack(expand=True)
        
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
    
    def create_line_chart(self, parent):
        """Gráfico de línea"""
        chart_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        header = ctk.CTkFrame(chart_frame, fg_color="white", height=60)
        header.pack(fill="x", padx=25, pady=(20, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Evolución del Inventario",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Gráfico
        fig = Figure(figsize=(6, 3.5), facecolor='white')
        ax = fig.add_subplot(111)
        
        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        values = [42, 47, 50, 48, 53, 56]
        
        ax.plot(months, values, color='#00b4d8', marker='o', linewidth=2.5, markersize=8)
        ax.set_ylim(0, 60)
        ax.set_ylabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_pie_chart(self, parent):
        """Gráfico de pie"""
        chart_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        chart_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        header = ctk.CTkFrame(chart_frame, fg_color="white", height=60)
        header.pack(fill="x", padx=25, pady=(20, 10))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Distribución por Categoría",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Gráfico
        fig = Figure(figsize=(6, 3.5), facecolor='white')
        ax = fig.add_subplot(111)
        
        sizes = [45, 25, 12, 18]
        labels = ['Papelería: 45%', 'Ferretería: 25%', 'Limpieza: 12%', 'Abarrotes: 18%']
        colors = ['#00b4d8', '#74c0fc', '#8b5a2b', '#e0e0e0']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90)
        ax.axis('equal')
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_metric_card(self, parent, title, value, subtitle, icon, bg_color, subtitle_color, position):
        """Crear tarjeta de métrica"""
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
            font=("Arial", 28, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w", pady=(10, 5))
        
        # Subtitle
        ctk.CTkLabel(
            content,
            text=subtitle,
            font=("Arial", 11),
            text_color=subtitle_color,
            anchor="w"
        ).pack(anchor="w")
    
    def create_product_row(self, parent, product, widths):
        """Crear fila de producto"""
        icon, name, days, stock, status = product
        
        row = ctk.CTkFrame(parent, fg_color="white", height=60)
        row.pack(fill="x", pady=3)
        row.pack_propagate(False)
        
        # Producto con icono de alerta
        product_frame = ctk.CTkFrame(row, fg_color="white", width=widths[0])
        product_frame.pack(side="left", padx=10)
        product_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            product_frame,
            text="⚠️",
            font=("Segoe UI Emoji", 16),
            fg_color="#fee",
            corner_radius=6,
            width=32,
            height=32
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            product_frame,
            text=name,
            font=("Arial", 12),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Días
        ctk.CTkLabel(
            row,
            text=days,
            font=("Arial", 12),
            text_color="#6c757d",
            width=widths[1],
            anchor="center"
        ).pack(side="left", padx=10)
        
        # Stock
        ctk.CTkLabel(
            row,
            text=f"{stock} unidades",
            font=("Arial", 12),
            text_color="#6c757d",
            width=widths[2],
            anchor="center"
        ).pack(side="left", padx=10)
        
        # Estado
        status_badge = ctk.CTkLabel(
            row,
            text=status,
            font=("Arial", 10, "bold"),
            text_color="#721c24",
            fg_color="#f8d7da",
            corner_radius=6,
            width=widths[3],
            height=28
        )
        status_badge.pack(side="left", padx=10)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ReportsView(root)
    root.mainloop()