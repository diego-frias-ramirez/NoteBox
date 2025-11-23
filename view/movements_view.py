"""
NoteBox - Vista del Módulo de Movimientos (Corregido y Funcional)
Ubicación: view/movements_view.py
"""

import customtkinter as ctk
from PIL import Image
import os
import datetime

from components.base_view import BaseView
from controller.movements_controller import MovementsController
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
            text_color="#6c757d",
            border_width=2,
            border_color="#e0e0e0",
            hover_color="#f8f9fa",
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

        self.product_combo = ctk.CTkComboBox(product_frame, values=["Cargando..."])
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
                fg_color="#10b981",
                text_color="white",
                font=ctk.CTkFont(size=13, weight="bold"),
                border_width=0
            )
            self.exit_btn.configure(
                fg_color="white",
                text_color="#6c757d",
                font=ctk.CTkFont(size=13),
                border_width=2,
                border_color="#e0e0e0"
            )
        else:
            self.exit_btn.configure(
                fg_color="#ef233c",
                text_color="white",
                font=ctk.CTkFont(size=13, weight="bold"),
                border_width=0
            )
            self.entry_btn.configure(
                fg_color="white",
                text_color="#6c757d",
                font=ctk.CTkFont(size=13),
                border_width=2,
                border_color="#e0e0e0"
            )

    def load_data(self):
        """Carga los datos iniciales: productos, usuarios, resumen diario y movimientos."""
        try:
            # Cargar productos (usando get_products sin paginación)
            products = self.controller.get_products(limit=1000) # Asumiendo que get_products devuelve (productos, total)
            self.products = {p['id']: p for p in products}
            product_names = [p['nombre'] for p in products]
            self.product_combo.configure(values=product_names if product_names else ["No hay productos"])

            # Cargar resumen diario
            self.daily_summary = self.controller.get_daily_summary()
            self.update_daily_summary()

            # Cargar movimientos
            self.load_movements()

        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_VIEW")
            self.show_message("Error al cargar datos iniciales.", "error")

    def load_movements(self):
        """Carga los movimientos desde el controlador."""
        try:
            # Usar el controlador para obtener movimientos
            movements, total = self.controller.get_movements(page=self.current_page, limit=self.movements_per_page)
            self.movements = movements
            self.total_movements = total

            # Actualizar UI
            self.update_movements_list()
            self.update_pagination_label() # <-- Método corregido

        except Exception as e:
            Logger.log_error_exception(e, "MOVEMENTS_VIEW")
            self.show_message("Error al cargar movimientos.", "error")

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
            no_movements_label.pack(expand=True)
            return

        for movement in self.movements:
            self.create_movement_row(self.movements_list, movement)

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
        ctk.CTkLabel(
            row,
            text=movement["fecha"].strftime("%Y-%m-%d %H:%M"),
            font=ctk.CTkFont(size=11),
            text_color="#6c757d",
            anchor="center"
        ).pack(side="left", expand=True, padx=5)

        # Usuario
        ctk.CTkLabel(
            row,
            text=movement["usuario_nombre"],
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
            self.pagination_label.configure(text=f"Mostrando {len(self.movements)} movimientos")

    def save_movement(self):
        """Guarda el movimiento registrado."""
        # Validar campos
        product_name = self.product_combo.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        motive = self.motive_entry.get().strip()

        if product_name == "Cargando..." or product_name == "No hay productos" or not product_name:
            self.show_message("Seleccione un producto válido.", "error")
            return

        if not quantity_str or not motive:
            self.show_message("Por favor, complete todos los campos.", "error")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                self.show_message("La cantidad debe ser un número positivo.", "error")
                return
        except ValueError:
            self.show_message("La cantidad debe ser un número válido.", "error")
            return

        # Obtener el ID del producto
        product_id = None
        for pid, prod in self.products.items():
            if prod['nombre'] == product_name:
                product_id = pid
                break

        if product_id is None:
            self.show_message("Producto no válido.", "error")
            return

        notes = self.notes_textbox.get("1.0", "end-1c").strip()

        # Usar el controlador para registrar el movimiento
        success, message = self.controller.register_movement(
            product_id=product_id,
            quantity=quantity,
            movement_type=self.movement_type,
            reason=motive,
            notes=notes
        )

        if success:
            Logger.success(f"Movimiento registrado: {message}", "MOVEMENTS_VIEW")
            self.load_movements()
            self.daily_summary = self.controller.get_daily_summary()
            self.update_daily_summary()
            self.show_message(message, "success")
            self.clear_form()
        else:
            Logger.error(f"Error al registrar movimiento: {message}", "MOVEMENTS_VIEW")
            self.show_message(f"Error al registrar: {message}", "error")

    def clear_form(self):
        """Limpia el formulario de registro."""
        if self.products:
            self.product_combo.set(list(self.products.values())[0]['nombre'])
        else:
            self.product_combo.set("No hay productos")
        self.quantity_entry.delete(0, "end")
        self.motive_entry.delete(0, "end")
        self.notes_textbox.delete("1.0", "end")
        self.notes_textbox.insert("1.0", "Observaciones adicionales...")
        self.set_movement_type("Entrada")

    def show_message(self, message, msg_type="info"):
        """Muestra un mensaje temporal al usuario."""
        colors = {"info": "#3B82F6", "success": "#10B981", "warning": "#F59E0B", "error": "#EF4444"}
        color = colors.get(msg_type, "#3B82F6")

        popup = ctk.CTkToplevel(self)
        popup.title("")
        popup.geometry("300x100")
        popup.resizable(False, False)
        popup.configure(fg_color="#FFFFFF")
        popup.transient(self)
        popup.grab_set()

        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (100 // 2)
        popup.geometry(f"300x100+{x}+{y}")

        content_frame = ctk.CTkFrame(popup, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        icon_path = ""
        if msg_type == "success":
            icon_path = os.path.join(self.base_path, "..", "assets", "icons", "alert_info.png")
        elif msg_type == "error":
            icon_path = os.path.join(self.base_path, "..", "assets", "icons", "alert.png")
        elif msg_type == "warning":
            icon_path = os.path.join(self.base_path, "..", "assets", "icons", "alert_yellow.png")
        else:  # info
            icon_path = os.path.join(self.base_path, "..", "assets", "icons", "notifications.png")

        try:
            img = Image.open(icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            icon_img = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            icon_label = ctk.CTkLabel(content_frame, image=icon_img, text="")
            icon_label.pack(side="left", padx=(0, 10))
        except:
            fallback_emoji = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
            ctk.CTkLabel(content_frame, text=fallback_emoji.get(msg_type, "ℹ️"), font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))

        label = ctk.CTkLabel(
            content_frame, text=message,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color
        )
        label.pack(side="left", expand=True)

        popup.after(3000, popup.destroy)

