# view/movements_view.py

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime

class MovementsView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox - Movimientos")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.movement_type = tk.StringVar(value="entrada")
        
        # Datos de ejemplo
        self.movements = [
            ("entrada", "📦", "Cuaderno A4", 50, "Compra proveedor", "2025-11-05", "Admin"),
            ("salida", "📦", "Tornillo 1/2\"", 15, "Venta", "2025-11-05", "Vendedor1"),
            ("entrada", "📦", "Detergente 500ml", 30, "Compra proveedor", "2025-11-04", "Admin"),
            ("salida", "📦", "Lapicero Azul", 25, "Venta", "2025-11-04", "Vendedor2"),
            ("entrada", "📦", "Aceite 1L", 40, "Ajuste de inventario", "2025-11-03", "Admin"),
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
            ("🔄", "Movimientos", True),
            ("📈", "Reportes", False),
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
        
        # Grid layout (2 columnas)
        grid_container = ctk.CTkFrame(content, fg_color="transparent")
        grid_container.pack(fill="both", expand=True)
        
        # === COLUMNA IZQUIERDA: FORMULARIO ===
        left_column = ctk.CTkFrame(grid_container, fg_color="white", corner_radius=12)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        form_content = ctk.CTkFrame(left_column, fg_color="white")
        form_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título
        ctk.CTkLabel(
            form_content,
            text="Registrar Movimiento",
            font=("Arial", 20, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 25))
        
        # Tipo de Movimiento
        ctk.CTkLabel(
            form_content,
            text="Tipo de Movimiento",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        type_frame = ctk.CTkFrame(form_content, fg_color="white")
        type_frame.pack(fill="x", pady=(0, 20))
        
        # Botón Entrada
        self.entrada_btn = ctk.CTkButton(
            type_frame,
            text="⊕ Entrada",
            width=150,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="#10b981",
            hover_color="#059669",
            corner_radius=8,
            command=lambda: self.set_movement_type("entrada")
        )
        self.entrada_btn.pack(side="left", padx=(0, 10))
        
        # Botón Salida
        self.salida_btn = ctk.CTkButton(
            type_frame,
            text="⊖ Salida",
            width=150,
            height=45,
            font=("Arial", 13),
            fg_color="white",
            text_color="#6c757d",
            border_width=2,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
            corner_radius=8,
            command=lambda: self.set_movement_type("salida")
        )
        self.salida_btn.pack(side="left")
        
        # Producto
        ctk.CTkLabel(
            form_content,
            text="Producto",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        product_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Seleccionar producto...",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        product_entry.pack(fill="x", pady=(0, 20))
        
        # Cantidad
        ctk.CTkLabel(
            form_content,
            text="Cantidad",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        quantity_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="0",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        quantity_entry.pack(fill="x", pady=(0, 20))
        
        # Motivo
        ctk.CTkLabel(
            form_content,
            text="Motivo",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        motive_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Ej: Compra, Venta, Ajuste...",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        motive_entry.pack(fill="x", pady=(0, 20))
        
        # Fecha
        ctk.CTkLabel(
            form_content,
            text="Fecha",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        date_frame = ctk.CTkFrame(form_content, fg_color="#f8f9fa", corner_radius=8, height=45)
        date_frame.pack(fill="x", pady=(0, 20))
        date_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            date_frame,
            text="📅 " + datetime.now().strftime("%Y-%m-%d"),
            font=("Arial", 13),
            text_color="#6c757d"
        ).pack(side="left", padx=15)
        
        # Notas
        ctk.CTkLabel(
            form_content,
            text="Notas (Opcional)",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        notes_textbox = ctk.CTkTextbox(
            form_content,
            height=100,
            font=("Arial", 12),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        notes_textbox.pack(fill="x", pady=(0, 30))
        notes_textbox.insert("1.0", "Observaciones adicionales...")
        
        # Botones
        buttons_frame = ctk.CTkFrame(form_content, fg_color="white")
        buttons_frame.pack(fill="x")
        
        ctk.CTkButton(
            buttons_frame,
            text="💾 GUARDAR",
            width=200,
            height=50,
            font=("Arial", 14, "bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=8
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="Limpiar",
            width=100,
            height=50,
            font=("Arial", 13),
            fg_color="white",
            text_color="#6c757d",
            border_width=1,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
            corner_radius=8
        ).pack(side="left")
        
        # === COLUMNA DERECHA: HISTORIAL ===
        right_column = ctk.CTkFrame(grid_container, fg_color="white", corner_radius=12)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        history_content = ctk.CTkFrame(right_column, fg_color="white")
        history_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título historial
        ctk.CTkLabel(
            history_content,
            text="Historial de Movimientos Recientes",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 20))
        
        # Headers de tabla
        headers_frame = ctk.CTkFrame(history_content, fg_color="#f8f9fa", height=45, corner_radius=8)
        headers_frame.pack(fill="x", pady=(0, 10))
        headers_frame.pack_propagate(False)
        
        headers = ["Tipo", "Producto", "Cantidad", "Motivo", "Fecha", "Usuario"]
        for header in headers:
            ctk.CTkLabel(
                headers_frame,
                text=header,
                font=("Arial", 11, "bold"),
                text_color="#2b2d42",
                anchor="w"
            ).pack(side="left", expand=True, padx=10)
        
        # Lista de movimientos
        movements_list = ctk.CTkScrollableFrame(
            history_content,
            fg_color="white",
            height=300
        )
        movements_list.pack(fill="both", expand=True, pady=(0, 15))
        
        for movement in self.movements:
            self.create_movement_row(movements_list, movement)
        
        # Footer historial
        ctk.CTkLabel(
            history_content,
            text="Mostrando últimos 5 movimientos",
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            history_content,
            text="Ver historial completo →",
            font=("Arial", 12),
            text_color="#00b4d8",
            cursor="hand2",
            anchor="w"
        ).pack(fill="x")
        
        # === TARJETAS DE RESUMEN ===
        summary_frame = ctk.CTkFrame(content, fg_color="transparent")
        summary_frame.pack(fill="x", pady=(20, 0))
        
        # Entradas del Día
        entrada_card = ctk.CTkFrame(summary_frame, fg_color="#10b981", corner_radius=12)
        entrada_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        entrada_content = ctk.CTkFrame(entrada_card, fg_color="transparent")
        entrada_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        header_entrada = ctk.CTkFrame(entrada_content, fg_color="transparent")
        header_entrada.pack(fill="x")
        
        ctk.CTkLabel(
            header_entrada,
            text="Entradas del Día",
            font=("Arial", 14, "bold"),
            text_color="white",
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_entrada,
            text="⬆",
            font=("Arial", 24),
            text_color="white"
        ).pack(side="right")
        
        ctk.CTkLabel(
            entrada_content,
            text="120 unidades",
            font=("Arial", 28, "bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(10, 5))
        
        ctk.CTkLabel(
            entrada_content,
            text="8 movimientos registrados",
            font=("Arial", 12),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")
        
        # Salidas del Día
        salida_card = ctk.CTkFrame(summary_frame, fg_color="#ef233c", corner_radius=12)
        salida_card.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        salida_content = ctk.CTkFrame(salida_card, fg_color="transparent")
        salida_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        header_salida = ctk.CTkFrame(salida_content, fg_color="transparent")
        header_salida.pack(fill="x")
        
        ctk.CTkLabel(
            header_salida,
            text="Salidas del Día",
            font=("Arial", 14, "bold"),
            text_color="white",
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_salida,
            text="⬇",
            font=("Arial", 24),
            text_color="white"
        ).pack(side="right")
        
        ctk.CTkLabel(
            salida_content,
            text="85 unidades",
            font=("Arial", 28, "bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(10, 5))
        
        ctk.CTkLabel(
            salida_content,
            text="12 movimientos registrados",
            font=("Arial", 12),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")
        
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
    
    def create_movement_row(self, parent, movement):
        """Crear fila de movimiento"""
        mov_type, icon, product, quantity, motive, date, user = movement
        
        row = ctk.CTkFrame(parent, fg_color="white", height=55)
        row.pack(fill="x", pady=3)
        row.pack_propagate(False)
        
        # Tipo (badge)
        type_color = "#d4edda" if mov_type == "entrada" else "#f8d7da"
        type_text_color = "#155724" if mov_type == "entrada" else "#721c24"
        type_icon = "⊕" if mov_type == "entrada" else "⊖"
        
        type_badge = ctk.CTkLabel(
            row,
            text=f"{type_icon} {mov_type.capitalize()}",
            font=("Arial", 10, "bold"),
            text_color=type_text_color,
            fg_color=type_color,
            corner_radius=6,
            width=85
        )
        type_badge.pack(side="left", expand=True, padx=5)
        
        # Producto
        product_frame = ctk.CTkFrame(row, fg_color="white")
        product_frame.pack(side="left", expand=True, padx=5)
        
        ctk.CTkLabel(
            product_frame,
            text=icon,
            font=("Segoe UI Emoji", 14)
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkLabel(
            product_frame,
            text=product,
            font=("Arial", 11),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Cantidad
        ctk.CTkLabel(
            row,
            text=str(quantity),
            font=("Arial", 11, "bold"),
            text_color="#2b2d42",
            anchor="center"
        ).pack(side="left", expand=True, padx=5)
        
        # Motivo
        ctk.CTkLabel(
            row,
            text=motive,
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="w"
        ).pack(side="left", expand=True, padx=5)
        
        # Fecha
        ctk.CTkLabel(
            row,
            text=date,
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="center"
        ).pack(side="left", expand=True, padx=5)
        
        # Usuario
        ctk.CTkLabel(
            row,
            text=user,
            font=("Arial", 11),
            text_color="#6c757d",
            anchor="center"
        ).pack(side="left", expand=True, padx=5)
    
    def set_movement_type(self, tipo):
        """Cambiar tipo de movimiento"""
        self.movement_type.set(tipo)
        
        if tipo == "entrada":
            self.entrada_btn.configure(
                fg_color="#10b981",
                text_color="white",
                font=("Arial", 13, "bold"),
                border_width=0
            )
            self.salida_btn.configure(
                fg_color="white",
                text_color="#6c757d",
                font=("Arial", 13),
                border_width=2,
                border_color="#e0e0e0"
            )
        else:
            self.salida_btn.configure(
                fg_color="#ef233c",
                text_color="white",
                font=("Arial", 13, "bold"),
                border_width=0
            )
            self.entrada_btn.configure(
                fg_color="white",
                text_color="#6c757d",
                font=("Arial", 13),
                border_width=2,
                border_color="#e0e0e0"
            )


if __name__ == "__main__":
    root = ctk.CTk()
    app = MovementsView(root)
    root.mainloop()