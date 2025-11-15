# view/inventory_view.py

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class InventoryView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox - Inventario")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Datos de ejemplo
        self.products = [
            ("001", "📦", "Cuaderno A4", "Papelería", 150, "$2.50", "Disponible", "#d4edda"),
            ("002", "📦", "Lápices AA", "Lápices", 8, "$0.25", "Stock Bajo", "#fff3cd"),
            ("003", "📦", "Plumón negro", "Plumones", 0, "$1.50", "Agotado", "#f8d7da"),
            ("004", "📦", "Goma chica", "Papelería", 45, "$3.20", "Disponible", "#d4edda"),
            ("005", "📦", "Lapicero Azul", "Lápices", 230, "$0.50", "Disponible", "#d4edda"),
            ("006", "📦", "Peluche oso feliz", "Peluche", 12, "$8.50", "Stock Bajo", "#fff3cd"),
            ("007", "📦", "Resistol 1L", "Pegamento", 68, "$4.75", "Disponible", "#d4edda"),
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
        
        # Buscador sidebar
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
            ("📊", "Dashboard", False),
            ("📦", "Inventario", True),
            ("🔄", "Movimientos", False),
            ("📈", "Reportes", False),
            ("👥", "Usuarios", False),
            ("⚙️", "Configuración", False),
            ("❓", "Ayuda", False)
        ]
        
        for icon, text, active in menu_items:
            self.create_menu_item(sidebar, icon, text, active)
        
        # Usuario footer
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
        content = ctk.CTkFrame(main_container, fg_color="#f8f9fa")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Barra de herramientas
        toolbar = ctk.CTkFrame(content, fg_color="white", corner_radius=12, height=100)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)
        
        toolbar_content = ctk.CTkFrame(toolbar, fg_color="white")
        toolbar_content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Buscador de productos
        search_product = ctk.CTkEntry(
            toolbar_content,
            placeholder_text="🔍 Buscar productos...",
            width=350,
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        search_product.pack(side="left", padx=(0, 20))
        
        # Botón Filtrar
        filter_btn = ctk.CTkButton(
            toolbar_content,
            text="🔽 Filtrar",
            width=120,
            height=45,
            font=("Arial", 13),
            fg_color="white",
            text_color="#2b2d42",
            border_width=1,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
            corner_radius=8
        )
        filter_btn.pack(side="left", padx=(0, 10))
        
        # Botón Exportar
        export_btn = ctk.CTkButton(
            toolbar_content,
            text="⬇ Exportar",
            width=130,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="#10b981",
            hover_color="#059669",
            corner_radius=8
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        # Botón Añadir Producto
        add_btn = ctk.CTkButton(
            toolbar_content,
            text="+ Añadir Producto",
            width=160,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=8
        )
        add_btn.pack(side="left")
        
        # Filtros activos
        filters_frame = ctk.CTkFrame(toolbar, fg_color="white", height=40)
        filters_frame.pack(fill="x", padx=25, pady=(0, 10))
        
        ctk.CTkLabel(
            filters_frame,
            text="Filtros activos:",
            font=("Arial", 12),
            text_color="#6c757d"
        ).pack(side="left", padx=(0, 10))
        
        # Tag de filtro
        filter_tag = ctk.CTkFrame(filters_frame, fg_color="#e8f4f8", corner_radius=6, height=28)
        filter_tag.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            filter_tag,
            text="Papelería",
            font=("Arial", 11),
            text_color="#00b4d8"
        ).pack(side="left", padx=(10, 5))
        
        ctk.CTkButton(
            filter_tag,
            text="×",
            width=20,
            height=20,
            font=("Arial", 14),
            fg_color="transparent",
            text_color="#00b4d8",
            hover_color="#d0ebf5"
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkLabel(
            filters_frame,
            text="+ Agregar filtro",
            font=("Arial", 11),
            text_color="#00b4d8",
            cursor="hand2"
        ).pack(side="left")
        
        # === TABLA ===
        table_container = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        table_container.pack(fill="both", expand=True)
        
        # Frame para tabla con scrollbar
        table_frame = ctk.CTkFrame(table_container, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Headers de tabla
        headers = ["ID", "Producto", "Categoría", "Stock", "Precio", "Estado", "Acciones"]
        widths = [80, 250, 150, 100, 100, 150, 120]
        
        header_row = ctk.CTkFrame(table_frame, fg_color="#f8f9fa", height=50, corner_radius=8)
        header_row.pack(fill="x", pady=(0, 10))
        header_row.pack_propagate(False)
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                header_row,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#2b2d42",
                width=width,
                anchor="w" if i > 0 else "center"
            ).pack(side="left", padx=(15 if i == 0 else 10, 0))
        
        # Scroll frame para filas
        scroll_frame = ctk.CTkScrollableFrame(
            table_frame,
            fg_color="white",
            corner_radius=0
        )
        scroll_frame.pack(fill="both", expand=True)
        
        # Crear filas de productos
        for product in self.products:
            self.create_product_row(scroll_frame, product, widths)
        
        # === FOOTER CON PAGINACIÓN ===
        footer = ctk.CTkFrame(table_container, fg_color="white", height=70)
        footer.pack(fill="x", padx=25, pady=(0, 20))
        footer.pack_propagate(False)
        
        # Texto de resultados
        ctk.CTkLabel(
            footer,
            text="Mostrando 1-7 de 1,245 productos",
            font=("Arial", 12),
            text_color="#6c757d"
        ).pack(side="left")
        
        # Botones de paginación
        pagination = ctk.CTkFrame(footer, fg_color="white")
        pagination.pack(side="right")
        
        # Anterior
        ctk.CTkButton(
            pagination,
            text="Anterior",
            width=90,
            height=38,
            font=("Arial", 12),
            fg_color="white",
            text_color="#6c757d",
            border_width=1,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
            corner_radius=6
        ).pack(side="left", padx=5)
        
        # Página 1 (activa)
        ctk.CTkButton(
            pagination,
            text="1",
            width=38,
            height=38,
            font=("Arial", 12, "bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=6
        ).pack(side="left", padx=2)
        
        # Página 2
        ctk.CTkButton(
            pagination,
            text="2",
            width=38,
            height=38,
            font=("Arial", 12),
            fg_color="white",
            text_color="#6c757d",
            border_width=1,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
            corner_radius=6
        ).pack(side="left", padx=2)
        
        # Página 3
        ctk.CTkButton(
            pagination,
            text="3",
            width=38,
            height=38,
            font=("Arial", 12),
            fg_color="white",
            text_color="#6c757d",
            border_width=1,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
            corner_radius=6
        ).pack(side="left", padx=2)
        
        # Siguiente
        ctk.CTkButton(
            pagination,
            text="Siguiente",
            width=90,
            height=38,
            font=("Arial", 12),
            fg_color="white",
            text_color="#6c757d",
            border_width=1,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
            corner_radius=6
        ).pack(side="left", padx=5)
        
        # Footer final
        final_footer = ctk.CTkLabel(
            main_container,
            text="NoteBox v1.0 - 2025",
            font=("Arial", 10),
            text_color="#adb5bd",
            fg_color="#f8f9fa",
            height=40
        )
        final_footer.pack(side="bottom", fill="x")
    
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
    
    def create_product_row(self, parent, product, widths):
        """Crear fila de producto"""
        id_val, icon, name, category, stock, price, status, status_color = product
        
        row = ctk.CTkFrame(parent, fg_color="white", height=65)
        row.pack(fill="x", pady=3)
        row.pack_propagate(False)
        
        # ID
        ctk.CTkLabel(
            row,
            text=id_val,
            font=("Arial", 12),
            text_color="#6c757d",
            width=widths[0]
        ).pack(side="left", padx=(15, 0))
        
        # Producto con icono
        product_frame = ctk.CTkFrame(row, fg_color="white", width=widths[1])
        product_frame.pack(side="left", padx=10)
        product_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            product_frame,
            text=icon,
            font=("Segoe UI Emoji", 16)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            product_frame,
            text=name,
            font=("Arial", 12),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        # Categoría
        ctk.CTkLabel(
            row,
            text=category,
            font=("Arial", 12),
            text_color="#6c757d",
            width=widths[2],
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Stock
        ctk.CTkLabel(
            row,
            text=str(stock),
            font=("Arial", 12, "bold"),
            text_color="#2b2d42",
            width=widths[3],
            anchor="center"
        ).pack(side="left", padx=10)
        
        # Precio
        ctk.CTkLabel(
            row,
            text=price,
            font=("Arial", 12),
            text_color="#2b2d42",
            width=widths[4],
            anchor="center"
        ).pack(side="left", padx=10)
        
        # Estado (badge)
        status_badge = ctk.CTkLabel(
            row,
            text=status,
            font=("Arial", 11, "bold"),
            text_color="#2b2d42",
            fg_color=status_color,
            corner_radius=6,
            width=120,
            height=28
        )
        status_badge.pack(side="left", padx=10)
        
        # Acciones
        actions_frame = ctk.CTkFrame(row, fg_color="white", width=widths[6])
        actions_frame.pack(side="left", padx=10)
        
        # Editar
        ctk.CTkButton(
            actions_frame,
            text="✏️",
            width=35,
            height=35,
            font=("Segoe UI Emoji", 14),
            fg_color="#e8f4f8",
            hover_color="#d0ebf5",
            corner_radius=6
        ).pack(side="left", padx=2)
        
        # Eliminar
        ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=35,
            height=35,
            font=("Segoe UI Emoji", 14),
            fg_color="#fee",
            hover_color="#fcc",
            corner_radius=6
        ).pack(side="left", padx=2)


if __name__ == "__main__":
    root = ctk.CTk()
    app = InventoryView(root)
    root.mainloop()