"""
NoteBox - Vista del Módulo de Movimientos (Corregido y Funcional)
Ubicación: view/movements_view.py
"""

import customtkinter as ctk
from PIL import Image
import os
import datetime
import tkinter as tk
from tkinter import ttk

from components.base_view import BaseView
from controller.movements_controller import MovementsController
from utils.alerts import alert_manager
from utils.logger import Logger
from utils.helpers import Helpers

class MovementsView(BaseView):
    """Vista del Módulo de Movimientos."""

    def __init__(self, user_data):
        # Variables de estado
        self.movements = []
        self.current_page = 1
        self.movements_per_page = 5
        self.total_movements = 0
        self.daily_summary = {"entradas": 0, "salidas": 0, "count_entradas": 0, "count_salidas": 0}
        self.products = {}
        self.users = {}
        self.movement_type = "Entrada"

        # Instancia del controlador
        self.controller = MovementsController()
        self.controller.set_current_user(user_data)

        # Llamar al constructor de la clase base
        super().__init__(
            user_data=user_data,
            page_id="movimientos",
            page_title="Movimientos de Inventario",
            page_subtitle="Registrar y visualizar entradas y salidas de productos"
        )

    def create_content(self):
        """Crea el contenido específico del módulo de movimientos."""
        # Frame principal para el contenido (heredado de BaseView)
        content_frame = self.content_frame

        # Contenido principal (2 columnas)
        main_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # Columna Izquierda: Formulario de Registro
        left_column = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=12)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Título del formulario
        form_header = ctk.CTkFrame(left_column, fg_color="transparent")
        form_header.pack(fill="x", padx=30, pady=(30, 20))

        ctk.CTkLabel(
            form_header,
            text="Registrar Movimiento",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w")

        # Tipo de Movimiento
        type_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        type_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            type_frame,
            text="Tipo de Movimiento:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 10))

        # Botones Entrada/Salida
        self.entry_btn = ctk.CTkButton(
            type_frame,
            text="⊕ Entrada",
            width=150,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#10b981",
            text_color="white",
            hover_color="#059669",
            corner_radius=8,
            command=lambda: self.set_movement_type("Entrada")
        )
        self.entry_btn.pack(side="left", padx=(0, 10))

        self.exit_btn = ctk.CTkButton(
            type_frame,
            text="⊖ Salida",
            width=150,
            height=45,
            font=ctk.CTkFont(size=13),
            fg_color="white",
            text_color="#64748B", # Slate-500 para texto inactivo legible
            border_width=2,
            border_color="#e2e8f0",
            hover_color="#f1f5f9", # Slate-100 para hover sutil
            corner_radius=8,
            command=lambda: self.set_movement_type("Salida")
        )
        self.exit_btn.pack(side="left")

        # Producto
        product_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        product_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            product_frame,
            text="Producto:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 10))

        self.product_combo = ctk.CTkComboBox(product_frame, values=["Cargando productos..."])
        self.product_combo.pack(fill="x", pady=(0, 10))

        # Cantidad
        quantity_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        quantity_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            quantity_frame,
            text="Cantidad:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 10))

        self.quantity_entry = ctk.CTkEntry(quantity_frame, placeholder_text="Ingrese la cantidad", height=45)
        self.quantity_entry.pack(fill="x", pady=(0, 10))

        # Motivo
        motive_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        motive_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            motive_frame,
            text="Motivo:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 10))

        self.motive_entry = ctk.CTkEntry(motive_frame, placeholder_text="Ej: Compra, Venta, Ajuste...", height=45)
        self.motive_entry.pack(fill="x", pady=(0, 10))

        # Notas (Opcional)
        notes_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        notes_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            notes_frame,
            text="Notas (Opcional):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 10))

        self.notes_textbox = ctk.CTkTextbox(notes_frame, height=100)
        self.notes_textbox.pack(fill="x", pady=(0, 10))
        self.notes_textbox.insert("1.0", "Observaciones adicionales...")
        self.notes_textbox.bind("<FocusIn>", self.on_notes_focus_in)
        self.notes_textbox.bind("<FocusOut>", self.on_notes_focus_out)

        # Botón Guardar
        save_btn = ctk.CTkButton(
            left_column,
            text="💾 GUARDAR",
            width=200,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=8,
            command=self.save_movement
        )
        save_btn.pack(pady=30)

        # Columna Derecha: Historial y Resumen
        right_column = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=12)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Título del historial
        history_header = ctk.CTkFrame(right_column, fg_color="transparent")
        history_header.pack(fill="x", padx=30, pady=(30, 20))

        ctk.CTkLabel(
            history_header,
            text="Historial de Movimientos Recientes",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w")

        # Botón Ver Todos
        view_all_btn = ctk.CTkButton(
            history_header,
            text="📋 Ver todos",
            width=120,
            height=35,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=8,
            command=self.open_all_movements_window
        )
        view_all_btn.pack(side="right")

        # Tarjetas de Resumen Diario
        summary_frame = ctk.CTkFrame(right_column, fg_color="transparent")
        summary_frame.pack(fill="x", padx=30, pady=(0, 20))

        # Tarjeta Entradas
        entry_card = ctk.CTkFrame(summary_frame, fg_color="#10b981", corner_radius=12)
        entry_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        entry_content = ctk.CTkFrame(entry_card, fg_color="transparent")
        entry_content.pack(fill="both", expand=True, padx=30, pady=25)

        header_entry = ctk.CTkFrame(entry_content, fg_color="transparent")
        header_entry.pack(fill="x")

        ctk.CTkLabel(
            header_entry,
            text="Entradas del Día",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            anchor="w"
        ).pack(side="left")

        ctk.CTkLabel(
            header_entry,
            text="⬆",
            font=ctk.CTkFont(size=24),
            text_color="white"
        ).pack(side="right")

        self.entry_count_label = ctk.CTkLabel(
            entry_content,
            text="0 unidades",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white",
            anchor="w"
        )
        self.entry_count_label.pack(anchor="w", pady=(10, 5))

        self.entry_motions_label = ctk.CTkLabel(
            entry_content,
            text="0 movimientos registrados",
            font=ctk.CTkFont(size=12),
            text_color="white",
            anchor="w"
        )
        self.entry_motions_label.pack(anchor="w")

        # Tarjeta Salidas
        exit_card = ctk.CTkFrame(summary_frame, fg_color="#ef233c", corner_radius=12)
        exit_card.pack(side="right", fill="both", expand=True, padx=(10, 0))

        exit_content = ctk.CTkFrame(exit_card, fg_color="transparent")
        exit_content.pack(fill="both", expand=True, padx=30, pady=25)

        header_exit = ctk.CTkFrame(exit_content, fg_color="transparent")
        header_exit.pack(fill="x")

        ctk.CTkLabel(
            header_exit,
            text="Salidas del Día",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            anchor="w"
        ).pack(side="left")

        ctk.CTkLabel(
            header_exit,
            text="⬇",
            font=ctk.CTkFont(size=24),
            text_color="white"
        ).pack(side="right")

        self.exit_count_label = ctk.CTkLabel(
            exit_content,
            text="0 unidades",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white",
            anchor="w"
        )
        self.exit_count_label.pack(anchor="w", pady=(10, 5))

        self.exit_motions_label = ctk.CTkLabel(
            exit_content,
            text="0 movimientos registrados",
            font=ctk.CTkFont(size=12),
            text_color="white",
            anchor="w"
        )
        self.exit_motions_label.pack(anchor="w")

        # Historial de Movimientos
        history_frame = ctk.CTkFrame(right_column, fg_color="transparent")
        history_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Headers de tabla
        headers_frame = ctk.CTkFrame(history_frame, fg_color="#f8f9fa", height=45, corner_radius=8)
        headers_frame.pack(fill="x", pady=(0, 10))
        headers_frame.pack_propagate(False)

        headers = ["Tipo", "Producto", "Cantidad", "Motivo", "Fecha", "Usuario"]
        for header in headers:
            ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#2b2d42",
                anchor="w"
            ).pack(side="left", expand=True, padx=10)

        # Scrollable Frame para movimientos
        self.movements_list = ctk.CTkScrollableFrame(history_frame, fg_color="white", height=300)
        self.movements_list.pack(fill="both", expand=True, pady=(0, 15))

        # Footer del historial
        footer_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(0, 10))

        self.pagination_label = ctk.CTkLabel(
            footer_frame,
            text="Mostrando 0 movimientos",
            font=ctk.CTkFont(size=11),
            text_color="#6c757d",
            anchor="w"
        )
        self.pagination_label.pack(side="left")

        # Cargar datos iniciales
        self.load_data()

    def set_movement_type(self, movement_type):
        """Cambiar tipo de movimiento y actualizar UI."""
        self.movement_type = movement_type

        if movement_type == "Entrada":
            self.entry_btn.configure(
                fg_color="#10b981", # Verde Base
                text_color="white",
                font=ctk.CTkFont(size=13, weight="bold"),
                border_width=0,
                hover_color="#059669" # Verde Oscuro
            )
            self.exit_btn.configure(
                fg_color="white",
                text_color="#64748B", # Slate-500
                font=ctk.CTkFont(size=13),
                border_width=2,
                border_color="#e2e8f0",
                hover_color="#f1f5f9" # Slate-100
            )
        else:
            self.exit_btn.configure(
                fg_color="#ef233c", # Rojo Base
                text_color="white",
                font=ctk.CTkFont(size=13, weight="bold"),
                border_width=0,
                hover_color="#d90429" # Rojo Oscuro
            )
            self.entry_btn.configure(
                fg_color="white",
                text_color="#64748B", # Slate-500
                font=ctk.CTkFont(size=13),
                border_width=2,
                border_color="#e2e8f0",
                hover_color="#f1f5f9" # Slate-100
            )

    def load_data(self):
        """Carga los datos iniciales: productos, usuarios, resumen diario y movimientos."""
        try:
            # Cargar productos
            products_result = self.controller.get_products(limit=1000)
            if isinstance(products_result, tuple):
                products, total = products_result
            else:
                products = products_result
                
            self.products = {p['id']: p for p in products}
            product_names = [p['nombre'] for p in products]
            
            if product_names:
                self.product_combo.configure(values=product_names)
                self.product_combo.set(product_names[0])
            else:
                self.product_combo.configure(values=["No hay productos"])
                self.product_combo.set("No hay productos")

            # Cargar resumen diario
            self.daily_summary = self.controller.get_daily_summary()
            self.update_daily_summary()

            # Cargar movimientos
            self.load_movements()

        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_VIEW")
            # Usar alert_manager para mostrar error
            alert_manager.show_error(
                "Error al cargar datos", 
                f"No se pudieron cargar los datos iniciales.\n\nError: {str(e)}",
                self
            )

    def load_movements(self):
        """Carga los movimientos desde el controlador."""
        try:
            # Usar el controlador para obtener movimientos
            movements, total = self.controller.get_movements(
                page=self.current_page, 
                limit=self.movements_per_page
            )
            self.movements = movements
            self.total_movements = total

            # Actualizar UI
            self.update_movements_list()
            self.update_pagination_label()

        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_VIEW")
            # Usar alert_manager para mostrar error
            alert_manager.show_error(
                "Error al cargar movimientos", 
                "No se pudieron cargar los movimientos.\n\nPor favor, intente de nuevo.",
                self
            )

    def update_movements_list(self):
        """Actualiza la lista de movimientos en la interfaz."""
        # Limpiar filas anteriores
        for widget in self.movements_list.winfo_children():
            widget.destroy()

        if not self.movements:
            no_movements_label = ctk.CTkLabel(
                self.movements_list,
                text="No hay movimientos registrados.",
                font=ctk.CTkFont(size=14),
                text_color="#6B7280"
            )
            no_movements_label.pack(expand=True, pady=20)
            return

        for movement in self.movements:
            self.create_movement_row(self.movements_list, movement)

    def open_all_movements_window(self):
        """
        Abre una ventana nueva con un Treeview que muestra todos los movimientos completos.
        """
        try:
            all_movements = self.controller.get_all_movements()

            # Crear ventana
            win = ctk.CTkToplevel(self)
            win.title("📊 Todos los Movimientos")
            win.geometry("1000x500")
            win.transient(self)
            win.grab_set()
            
            # Centrar ventana
            win.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() // 2) - (1000 // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (500 // 2)
            win.geometry(f"1000x500+{x}+{y}")

            # Encabezado con botones
            top_frame = ctk.CTkFrame(win, fg_color="transparent")
            top_frame.pack(fill="x", padx=20, pady=(15, 10))

            # Título
            ctk.CTkLabel(
                top_frame,
                text="Todos los Movimientos Registrados",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#2b2d42"
            ).pack(side="left")

            # Botones a la derecha
            btn_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
            btn_frame.pack(side="right")

            refresh_btn = ctk.CTkButton(
                btn_frame, 
                text="🔄 Actualizar", 
                command=lambda: self._refresh_all_movements_tree(tree), 
                width=110, 
                height=34
            )
            refresh_btn.pack(side="left", padx=5)

            export_btn = ctk.CTkButton(
                btn_frame, 
                text="📥 Exportar", 
                command=lambda: self.export_all_movements(all_movements), 
                width=110, 
                height=34,
                fg_color="#10B981"
            )
            export_btn.pack(side="left", padx=5)

            close_btn = ctk.CTkButton(
                btn_frame, 
                text="Cerrar", 
                command=win.destroy, 
                width=100, 
                height=34, 
                fg_color="#EF4444"
            )
            close_btn.pack(side="left", padx=5)

            # Contenedor para Treeview
            tree_frame = ctk.CTkFrame(win, fg_color="#FFFFFF")
            tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

            # Treeview y Scrollbars usando grid para mejor control
            tree_frame.grid_columnconfigure(0, weight=1)
            tree_frame.grid_rowconfigure(0, weight=1)

            cols = ("id", "tipo", "producto", "cantidad", "motivo", "notas", "fecha", "usuario")
            tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=20)
            
            # Scrollbars
            vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
            
            # Configurar comandos de scroll del tree
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            # Grid layout
            tree.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb.grid(row=1, column=0, sticky="ew")

            # Configurar columnas
            tree.heading("id", text="ID")
            tree.heading("tipo", text="Tipo")
            tree.heading("producto", text="Producto")
            tree.heading("cantidad", text="Cantidad")
            tree.heading("motivo", text="Motivo")
            tree.heading("notas", text="Notas")
            tree.heading("fecha", text="Fecha")
            tree.heading("usuario", text="Usuario")

            tree.column("id", width=60, anchor="center")
            tree.column("tipo", width=90, anchor="center")
            tree.column("producto", width=260, anchor="w")
            tree.column("cantidad", width=80, anchor="center")
            tree.column("motivo", width=180, anchor="w")
            tree.column("notas", width=200, anchor="w")
            tree.column("fecha", width=150, anchor="center")
            tree.column("usuario", width=140, anchor="w")

            # Insertar datos
            for m in all_movements:
                fecha_val = m.get("fecha")
                if fecha_val is None:
                    fecha_str = ""
                elif isinstance(fecha_val, str):
                    fecha_str = fecha_val
                else:
                    try:
                        fecha_str = fecha_val.strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        fecha_str = str(fecha_val)

                tree.insert("", "end", values=(
                    m.get("id"), 
                    m.get("tipo"), 
                    m.get("producto_nombre", "Desconocido"), 
                    m.get("cantidad"),
                    m.get("motivo", ""), 
                    m.get("notas") or "", 
                    fecha_str, 
                    m.get("usuario_nombre", "Desconocido")
                ))

            # Configurar estilos alternados
            tree.tag_configure('evenrow', background='#f8f9fa')
            tree.tag_configure('oddrow', background='#ffffff')
            
            for i, item in enumerate(tree.get_children()):
                tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow',))

        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_VIEW")
            # Usar alert_manager para mostrar error
            alert_manager.show_error(
                "Error al abrir movimientos", 
                f"No se pudieron cargar todos los movimientos.\n\nError: {str(e)}",
                self
            )

    def _refresh_all_movements_tree(self, tree):
        """
        Refresca el contenido del Treeview con todos los movimientos.
        """
        try:
            # Limpiar treeview
            for row in tree.get_children():
                tree.delete(row)
                
            # Obtener datos actualizados
            all_movements = self.controller.get_all_movements()
            
            # Insertar nuevos datos
            for m in all_movements:
                fecha_val = m.get("fecha")
                if fecha_val is None:
                    fecha_str = ""
                elif isinstance(fecha_val, str):
                    fecha_str = fecha_val
                else:
                    try:
                        fecha_str = fecha_val.strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        fecha_str = str(fecha_val)
                        
                tree.insert("", "end", values=(
                    m.get("id"), 
                    m.get("tipo"), 
                    m.get("producto_nombre", "Desconocido"), 
                    m.get("cantidad"),
                    m.get("motivo", ""), 
                    m.get("notas") or "", 
                    fecha_str, 
                    m.get("usuario_nombre", "Desconocido")
                ))
            
            # Aplicar estilos alternados
            for i, item in enumerate(tree.get_children()):
                tree.item(item, tags=('evenrow' if i % 2 == 0 else 'oddrow',))
                
            # Mostrar mensaje de éxito
            alert_manager.show_success(
                "Datos Actualizados", 
                f"Se han cargado {len(all_movements)} movimientos.",
                self
            )
            
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_VIEW")
            alert_manager.show_error(
                "Error al actualizar", 
                "No se pudieron actualizar los movimientos.",
                self
            )

    def export_all_movements(self, movements_data):
        """Exporta los movimientos mostrados."""
        try:
            # Configurar nombre por defecto
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"movimientos_{timestamp}.csv"
            
            # Initial dir
            initial_dir = Helpers.get_exports_dir('reports')
            
            # Ask where to save
            filepath = ctk.filedialog.asksaveasfilename(
                title="Exportar Movimientos",
                initialdir=initial_dir,
                initialfile=default_filename,
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if not filepath:
                return  # Cancelado
            
            success, result = self.controller.export_movements(movements_data, filepath)
            
            if success:
                alert_manager.show_success(
                    "Exportación Exitosa", 
                    f"Movimientos exportados a:\n{os.path.basename(result)}",
                    self
                )
            else:
                alert_manager.show_error(
                    "Error al Exportar", 
                    f"No se pudo exportar:\n{result}",
                    self
                )
        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_VIEW")
            alert_manager.show_error("Error", f"Error inesperado: {str(e)}", self)

    def create_movement_row(self, parent, movement):
        """Crea una fila para un movimiento en la tabla."""
        row = ctk.CTkFrame(parent, fg_color="white", height=55)
        row.pack(fill="x", pady=3)
        row.pack_propagate(False)

        # Tipo (badge)
        type_color = "#d4edda" if movement["tipo"] == "Entrada" else "#f8d7da"
        type_text_color = "#155724" if movement["tipo"] == "Entrada" else "#721c24"
        type_icon = "⊕" if movement["tipo"] == "Entrada" else "⊖"

        type_badge = ctk.CTkLabel(
            row,
            text=f"{type_icon} {movement['tipo']}",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=type_text_color,
            fg_color=type_color,
            corner_radius=6,
            width=85
        )
        type_badge.pack(side="left", expand=True, padx=5)

        # Producto
        product_frame = ctk.CTkFrame(row, fg_color="white")
        product_frame.pack(side="left", expand=True, padx=5)

        icon_frame = ctk.CTkFrame(product_frame, fg_color="#E0F7FA", width=32, height=32, corner_radius=8)
        icon_frame.pack(side="left", padx=(0, 5))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="📦", font=ctk.CTkFont(size=12)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            product_frame,
            text=movement["producto_nombre"],
            font=ctk.CTkFont(size=11),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")

        # Cantidad
        ctk.CTkLabel(
            row,
            text=str(movement["cantidad"]),
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#2b2d42",
            anchor="center"
        ).pack(side="left", expand=True, padx=5)

        # Motivo
        ctk.CTkLabel(
            row,
            text=movement["motivo"],
            font=ctk.CTkFont(size=11),
            text_color="#6c757d",
            anchor="w"
        ).pack(side="left", expand=True, padx=5)

        # Fecha
        fecha_str = ""
        try:
            if isinstance(movement["fecha"], str):
                fecha_str = movement["fecha"]
            else:
                fecha_str = movement["fecha"].strftime("%Y-%m-%d %H:%M")
        except Exception:
            fecha_str = "Fecha no válida"
            
        ctk.CTkLabel(
            row,
            text=fecha_str,
            font=ctk.CTkFont(size=11),
            text_color="#6c757d",
            anchor="center"
        ).pack(side="left", expand=True, padx=5)

        # Usuario
        ctk.CTkLabel(
            row,
            text=movement.get("usuario_nombre", "Desconocido"),
            font=ctk.CTkFont(size=11),
            text_color="#6c757d",
            anchor="center"
        ).pack(side="left", expand=True, padx=5)

    def update_daily_summary(self):
        """Actualiza las tarjetas de resumen diario."""
        self.entry_count_label.configure(text=f"{self.daily_summary['entradas']} unidades")
        self.entry_motions_label.configure(text=f"{self.daily_summary['count_entradas']} movimientos registrados")

        self.exit_count_label.configure(text=f"{self.daily_summary['salidas']} unidades")
        self.exit_motions_label.configure(text=f"{self.daily_summary['count_salidas']} movimientos registrados")

    def update_pagination_label(self):
        """Actualiza el texto de la paginación."""
        if self.total_movements == 0:
            self.pagination_label.configure(text="No hay movimientos para mostrar")
        else:
            total_pages = (self.total_movements + self.movements_per_page - 1) // self.movements_per_page
            start_index = (self.current_page - 1) * self.movements_per_page + 1
            end_index = min(start_index + len(self.movements) - 1, self.total_movements)
            
            self.pagination_label.configure(
                text=f"Página {self.current_page} de {total_pages} | Mostrando {len(self.movements)} de {self.total_movements} movimientos"
            )

    def save_movement(self):
        """Guarda el movimiento registrado."""
        # Validar campos
        product_name = self.product_combo.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        motive = self.motive_entry.get().strip()

        if product_name == "Cargando productos..." or product_name == "No hay productos" or not product_name:
            alert_manager.validation_error(
                "Por favor seleccione un producto válido de la lista.",
                self
            )
            return

        if not quantity_str or not motive:
            alert_manager.empty_fields(self)
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                alert_manager.validation_error(
                    "La cantidad debe ser un número positivo mayor que cero.",
                    self
                )
                return
        except ValueError:
            alert_manager.validation_error(
                "La cantidad debe ser un número válido (entero).",
                self
            )
            return

        # Obtener el ID del producto
        product_id = None
        product_data = None
        for pid, prod in self.products.items():
            if prod['nombre'] == product_name:
                product_id = pid
                product_data = prod
                break

        if product_id is None:
            alert_manager.show_error(
                "Producto no encontrado", 
                "El producto seleccionado no existe en la base de datos.",
                self
            )
            return

        # Validar stock disponible para salidas
        if self.movement_type == "Salida":
            stock_disponible = product_data.get('stock', 0)
            if stock_disponible < quantity:
                alert_manager.show_warning(
                    "Stock Insuficiente",
                    f"No hay suficiente stock disponible.\n\n"
                    f"Stock actual: {stock_disponible} unidades\n"
                    f"Intenta retirar: {quantity} unidades\n\n"
                    f"Faltante: {quantity - stock_disponible} unidades",
                    self
                )
                return

        notes = self.notes_textbox.get("1.0", "end-1c").strip()

        # Confirmar el movimiento
        movimiento_texto = f"{self.movement_type} de {quantity} unidades"
        confirm_message = f"¿Está seguro de registrar {movimiento_texto.lower()} del producto '{product_name}'?\n\n"
        confirm_message += f"Motivo: {motive}\n"
        confirm_message += f"Notas: {notes if notes else 'Ninguna'}"

        if not alert_manager.confirm("Confirmar Movimiento", confirm_message, self):
            return

        # Usar el controlador para registrar el movimiento
        success, message, new_product_data = self.controller.register_movement(
            product_id=product_id,
            quantity=quantity,
            movement_type=self.movement_type,
            reason=motive,
            notes=notes
        )

        if success:
            Logger.success(f"Movimiento registrado: {message}", "MOVEMENTS_VIEW")
            
            # Generar alerta de movimiento usando alert_manager
            alert_manager.generate_movement_alert(
                product_data,
                self.movement_type,
                quantity,
                motive
            )
            
            # Actualizar UI
            self.current_page = 1  # Resetear a la primera página para ver el nuevo movimiento
            self.load_movements()
            self.daily_summary = self.controller.get_daily_summary()
            self.update_daily_summary()
            
            # Mostrar mensaje de éxito detallado
            alert_manager.show_success(
                "Movimiento Registrado",
                f"Se registró correctamente la {movimiento_texto.lower()}.\n\n"
                f"• Producto: {product_name}\n"
                f"• Cantidad: {quantity} unidades\n"
                f"• Motivo: {motive}\n"
                f"• Stock actualizado: {new_product_data.get('stock', 'N/A')} unidades",
                self
            )
            
            self.clear_form()
        else:
            Logger.error(f"Error al registrar movimiento: {message}", "MOVEMENTS_VIEW")
            alert_manager.show_error(
                "Error al Registrar",
                f"No se pudo registrar el movimiento.\n\nError: {message}",
                self
            )

    def clear_form(self):
        """Limpia el formulario de registro."""
        # Restablecer tipo de movimiento a Entrada
        self.set_movement_type("Entrada")
        
        # Limpiar campos
        self.quantity_entry.delete(0, "end")
        self.motive_entry.delete(0, "end")
        
        # Restablecer notas
        self.notes_textbox.delete("1.0", "end")
        self.notes_textbox.insert("1.0", "Observaciones adicionales...")
        self.notes_textbox.configure(text_color="#6c757d")
        
        # Seleccionar primer producto si existe
        if self.products:
            product_names = [p['nombre'] for p in self.products.values()]
            if product_names:
                self.product_combo.set(product_names[0])

    def on_notes_focus_in(self, event):
        """Maneja el evento de foco en el campo de notas (borra placeholder)."""
        current_text = self.notes_textbox.get("1.0", "end-1c").strip()
        if current_text == "Observaciones adicionales...":
            self.notes_textbox.delete("1.0", "end")
            self.notes_textbox.configure(text_color="#2b2d42")

    def on_notes_focus_out(self, event):
        """Maneja el evento de pérdida de foco en el campo de notas (restaura placeholder)."""
        current_text = self.notes_textbox.get("1.0", "end-1c").strip()
        if not current_text:
            self.notes_textbox.insert("1.0", "Observaciones adicionales...")
            self.notes_textbox.configure(text_color="#6c757d")

    def get_notification_count(self):
        """Obtiene el número de notificaciones no leídas."""
        return alert_manager.get_unread_count()

    # Métodos de paginación adicionales
    def previous_page(self):
        """Va a la página anterior."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_movements()

    def next_page(self):
        """Va a la página siguiente."""
        total_pages = (self.total_movements + self.movements_per_page - 1) // self.movements_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_movements()

    def go_to_page(self, page_num):
        """Va a una página específica."""
        total_pages = (self.total_movements + self.movements_per_page - 1) // self.movements_per_page
        if 1 <= page_num <= total_pages:
            self.current_page = page_num
            self.load_movements()