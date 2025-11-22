"""
NoteBox - Vista del Módulo de Inventario
Ubicación: view/inventory_view.py
"""

import customtkinter as ctk
from PIL import Image
import os

from components.base_view import BaseView
from controller.inventory_controller import InventoryController
from utils.logger import Logger
from utils.helpers import Helpers

class InventarioView(BaseView):
    """Vista del Módulo de Inventario."""

    def __init__(self, user_data):
        # Variables de estado
        self.products = []
        self.categories = {}
        self.current_page = 1
        self.products_per_page = 7
        self.total_products = 0
        self.search_query = ""
        self.filter_category_id = None
        self.images = {}

        # Instancia del controlador
        self.controller = InventoryController()
        self.controller.set_current_user(user_data) # Pasar datos del usuario actual al controlador

        # Llamar al constructor de la clase base
        super().__init__(
            user_data=user_data,
            page_id="inventario", # Este ID debe coincidir con el del sidebar
            page_title="Gestión de Inventario",
            page_subtitle="Administrar productos y categorías"
        )

    def create_content(self):
        """Crea el contenido específico del módulo de inventario."""
        # Frame principal para el contenido (heredado de BaseView)
        content_frame = self.content_frame

        # Toolbar (buscador, filtros, botones)
        self.create_toolbar(content_frame)

        # Filtros activos
        self.create_filters_bar(content_frame)

        # Tabla de productos
        self.create_table(content_frame)

        # Paginación
        self.create_pagination(content_frame)

        # Cargar datos iniciales
        self.load_products()

    def create_toolbar(self, parent):
        """Crea la barra de herramientas (buscador, filtros, botones)."""
        toolbar = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        toolbar.pack(fill="x", pady=(0, 15))

        # Búsqueda
        search_frame = ctk.CTkFrame(toolbar, fg_color="#FFFFFF", corner_radius=12, width=450, height=48)
        search_frame.pack(side="left")
        search_frame.pack_propagate(False)

        ctk.CTkLabel(search_frame, text="🔍", font=ctk.CTkFont(size=16), text_color="#94A3B8").pack(side="left", padx=(18, 10))
        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Buscar productos...",
            fg_color="transparent", border_width=0, font=ctk.CTkFont(size=14), height=44
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.on_search_change) # <-- Vincular evento de búsqueda

        # Botones
        btns_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btns_frame.pack(side="right")

        # Filtrar
        filter_btn = ctk.CTkButton(
            btns_frame, text="🔽  Filtrar", width=110, height=44,
            font=ctk.CTkFont(size=13), fg_color="#FFFFFF",
            text_color="#1E293B", hover_color="#F1F5F9",
            corner_radius=10, border_width=1, border_color="#E2E8F0",
            command=self.open_filter_dialog
        )
        filter_btn.pack(side="left", padx=(0, 12))

        # Exportar
        export_btn = ctk.CTkButton(
            btns_frame, text="⬇  Exportar", width=120, height=44,
            font=ctk.CTkFont(size=13), fg_color="#10B981",
            text_color="#FFFFFF", hover_color="#059669", corner_radius=10,
            command=self.export_inventory
        )
        export_btn.pack(side="left", padx=(0, 12))

        # Añadir Producto
        add_btn = ctk.CTkButton(
            btns_frame, text="+  Añadir Producto", width=160, height=44,
            font=ctk.CTkFont(size=13, weight="bold"), fg_color="#00B4D8",
            text_color="#FFFFFF", hover_color="#0096B4", corner_radius=10,
            command=self.add_product
        )
        add_btn.pack(side="left")

    def on_search_change(self, event):
        """Evento que se dispara al cambiar el texto de búsqueda."""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1 # Reiniciar a la primera página al buscar
        self.load_products() # <-- Llamar a load_products para refrescar

    def open_filter_dialog(self):
        """Abre un diálogo para seleccionar filtro por categoría."""
        # Usar el controlador para obtener categorías
        categories_dict = self.controller.get_categories()

        dialog = ctk.CTkToplevel(self)
        dialog.title("Filtrar por Categoría")
        dialog.geometry("300x350")
        dialog.transient(self)
        dialog.grab_set()

        # Centrar el diálogo
        x = self.winfo_x() + (self.winfo_width() - 300) // 2
        y = self.winfo_y() + (self.winfo_height() - 350) // 2
        dialog.geometry(f"300x350+{x}+{y}")

        # Título
        ctk.CTkLabel(dialog, text="Seleccionar Categoría", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        # Scrollable Frame para categorías
        categories_scrollable = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        categories_scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Variable para el radio button
        selected_category_id = ctk.StringVar(value="all") # Valor por defecto: "all"

        # Botón "Todos los productos"
        all_radio = ctk.CTkRadioButton(
            categories_scrollable,
            text="Todos los productos",
            variable=selected_category_id,
            value="all"
        )
        all_radio.pack(anchor="w", padx=10, pady=5)

        # Iterar sobre las categorías del controlador
        for cat_id, cat_data in categories_dict.items():
            cat_radio = ctk.CTkRadioButton(
                categories_scrollable,
                text=cat_data['nombre'],
                variable=selected_category_id,
                value=str(cat_id) # Convertir ID a string para el radiobutton
            )
            cat_radio.pack(anchor="w", padx=10, pady=5)

        # Botón Aplicar
        def apply_filter():
            value = selected_category_id.get()
            if value == "all":
                self.filter_category_id = None
            else:
                self.filter_category_id = int(value) # Convertir de string a int
            self.current_page = 1 # Reiniciar a la primera página al filtrar
            self.load_products() # <-- Refrescar productos con el nuevo filtro
            dialog.destroy()

        apply_btn = ctk.CTkButton(
            dialog,
            text="Aplicar Filtro",
            width=100,
            height=30,
            fg_color="#00B4D8",
            text_color="#FFFFFF",
            hover_color="#0096B4",
            corner_radius=8,
            command=apply_filter
        )
        apply_btn.pack(pady=10)

    def create_filters_bar(self, parent):
        """Crea la barra de filtros activos."""
        filters_frame = ctk.CTkFrame(parent, fg_color="transparent", height=35)
        filters_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            filters_frame, text="Filtros activos:",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(side="left", padx=(0, 12))

        # Mostrar filtro de categoría si está activo
        if self.filter_category_id is not None:
            # Buscar el nombre de la categoría en el diccionario self.categories
            category_name = "Categoría desconocida"
            for cat_id, cat_data in self.categories.items():
                if cat_id == self.filter_category_id:
                    category_name = cat_data.get('nombre', 'Categoría sin nombre')
                    break

            tag_frame = ctk.CTkFrame(filters_frame, fg_color="#E0F7FA", corner_radius=15, height=28)
            tag_frame.pack(side="left", padx=(0, 10))
            tag_frame.pack_propagate(False)

            ctk.CTkLabel(
                tag_frame, text=category_name,
                font=ctk.CTkFont(size=11), text_color="#00B4D8"
            ).pack(side="left", padx=(12, 5), pady=4)

            # Botón para quitar el filtro
            remove_tag_btn = ctk.CTkButton(
                tag_frame, text="×", width=20, height=20,
                fg_color="transparent", text_color="#00B4D8",
                hover_color="#B2EBF2", font=ctk.CTkFont(size=14),
                command=self.clear_category_filter
            )
            remove_tag_btn.pack(side="left", padx=(0, 8))
        else:
            # Mostrar mensaje si no hay filtros activos
            ctk.CTkLabel(
                filters_frame, text="Ningún filtro aplicado",
                font=ctk.CTkFont(size=12), text_color="#94A3B8"
            ).pack(side="left", padx=(0, 10))

        # Botón para agregar más filtros (opcional)
        ctk.CTkButton(
            filters_frame, text="+ Agregar filtro",
            font=ctk.CTkFont(size=12), fg_color="transparent",
            text_color="#94A3B8", hover_color="#F1F5F9", width=110, height=28,
            command=self.open_filter_dialog # <-- Reutilizar el diálogo existente
        ).pack(side="left")

    def clear_category_filter(self):
        """Limpia el filtro de categoría."""
        self.filter_category_id = None
        self.current_page = 1
        self.load_products()

    def create_table(self, parent):
        """Crea la tabla de productos."""
        table_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        self.table_frame = table_frame # <-- Guardar referencia para update_table

        # Encabezado de la tabla
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=(15, 0))
        header_frame.pack_propagate(False)

        columns = [
            ("ID", 60),
            ("Producto", 220),
            ("Categoría", 110),
            ("Stock", 70),
            ("Precio", 80),
            ("Estado", 100),
            ("Acciones", 90)
        ]

        for name, width in columns:
            ctk.CTkLabel(
                header_frame, text=name, width=width,
                font=ctk.CTkFont(size=12, weight="bold"), text_color="#64748B", anchor="w"
            ).pack(side="left", padx=8)

        # Separador
        separator = ctk.CTkFrame(table_frame, fg_color="#F1F5F9", height=1)
        separator.pack(fill="x", padx=15)

        # Contenedor para filas (scrollable frame)
        self.rows_container = ctk.CTkScrollableFrame(table_frame, fg_color="transparent", height=350)
        self.rows_container.pack(fill="both", expand=True, padx=15, pady=(10, 15))

    def update_table(self):
        """Actualiza la tabla con los productos cargados."""
        # Limpiar filas anteriores
        for widget in self.rows_container.winfo_children():
            widget.destroy()

        if not self.products:
            # Mensaje si no hay productos
            no_products_label = ctk.CTkLabel(
                self.rows_container,
                text="No se encontraron productos con los filtros aplicados.",
                font=ctk.CTkFont(size=14), text_color="#6B7280"
            )
            no_products_label.pack(expand=True)
            return

        # Crear filas para cada producto
        for i, product in enumerate(self.products):
            is_even = i % 2 == 0
            self.create_product_row(self.rows_container, product, is_even)

    def create_product_row(self, parent, product, is_even):
        """Crea una fila para un producto en la tabla."""
        bg_color = "#FFFFFF" if is_even else "#F8FAFC"
        row_frame = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=0, height=60)
        row_frame.pack(fill="x", pady=2, padx=0)
        row_frame.pack_propagate(False)

        inner_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=5, pady=8)

        # ID
        ctk.CTkLabel(
            inner_frame, text=str(product["id"]).zfill(3),
            width=60, font=ctk.CTkFont(size=12), text_color="#64748B", anchor="w"
        ).pack(side="left", padx=8)

        # Producto (con icono genérico)
        product_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=220)
        product_frame.pack(side="left", padx=8)
        product_frame.pack_propagate(False)

        icon_frame = ctk.CTkFrame(product_frame, fg_color="#E0F7FA", width=32, height=32, corner_radius=8)
        icon_frame.pack(side="left", padx=(0, 10))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="📦", font=ctk.CTkFont(size=12)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            product_frame, text=product["nombre"],
            font=ctk.CTkFont(size=12), text_color="#1E293B", anchor="w"
        ).pack(side="left", fill="y")

        # Categoría
        category_name = self.categories.get(product.get('categoria_id'), {}).get('nombre', 'Sin Categoría')
        ctk.CTkLabel(
            inner_frame, text=category_name,
            width=110, font=ctk.CTkFont(size=12), text_color="#64748B", anchor="w"
        ).pack(side="left", padx=8)

        # Stock
        ctk.CTkLabel(
            inner_frame, text=str(product["stock"]),
            width=70, font=ctk.CTkFont(size=12), text_color="#1E293B", anchor="w"
        ).pack(side="left", padx=8)

        # Precio
        ctk.CTkLabel(
            inner_frame, text=Helpers.format_currency(product["precio"]),
            width=80, font=ctk.CTkFont(size=12), text_color="#1E293B", anchor="w"
        ).pack(side="left", padx=8)

        # Estado (badge)
        status_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=100)
        status_frame.pack(side="left", padx=8)
        status_frame.pack_propagate(False)

        status = product["estado"]
        badge_colors = {
            "Disponible": ("#DCFCE7", "#16A34A"),
            "Stock Bajo": ("#FEF3C7", "#D97706"),
            "Agotado": ("#FEE2E2", "#DC2626")
        }
        bg_color, text_color = badge_colors.get(status, badge_colors["Disponible"])

        badge = ctk.CTkFrame(status_frame, fg_color=bg_color, corner_radius=12, height=26)
        badge.pack(side="left")
        ctk.CTkLabel(
            badge, text=status,
            font=ctk.CTkFont(size=10, weight="bold"), text_color=text_color
        ).pack(padx=12, pady=4)

        # Acciones (Editar, Eliminar)
        actions_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=90)
        actions_frame.pack(side="left", padx=8)
        actions_frame.pack_propagate(False)

        # Botón Editar
        edit_btn = ctk.CTkButton(
            actions_frame, text="✏️", width=32, height=32,
            fg_color="transparent", hover_color="#E0F7FA",
            corner_radius=6, font=ctk.CTkFont(size=14),
            command=lambda p=product: self.edit_product(p)
        )
        edit_btn.pack(side="left", padx=2)

        # Botón Eliminar
        delete_btn = ctk.CTkButton(
            actions_frame, text="🗑️", width=32, height=32,
            fg_color="transparent", hover_color="#FEE2E2",
            corner_radius=6, font=ctk.CTkFont(size=14),
            command=lambda p=product: self.delete_product(p)
        )
        delete_btn.pack(side="left", padx=2)

    def create_pagination(self, parent):
        """Crea la barra de paginación."""
        pagination_frame = ctk.CTkFrame(parent, fg_color="transparent", height=45)
        pagination_frame.pack(fill="x")

        # Texto de paginación
        self.pagination_label = ctk.CTkLabel(
            pagination_frame, text="Mostrando 0 de 0 productos",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        )
        self.pagination_label.pack(side="left")

        # Botones de paginación
        buttons_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        buttons_frame.pack(side="right")

        # Botón Anterior
        prev_btn = ctk.CTkButton(
            buttons_frame, text="Anterior", width=80, height=34,
            font=ctk.CTkFont(size=12), fg_color="#FFFFFF", text_color="#1E293B",
            hover_color="#F1F5F9", border_width=1, border_color="#E2E8F0", corner_radius=8,
            command=self.previous_page
        )
        prev_btn.pack(side="left", padx=4)

        # Botones de páginas (solo mostrará la actual y +/- 1)
        self.page_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        self.page_buttons_frame.pack(side="left", padx=4)
        self.update_page_buttons() # <-- Actualizar los botones numéricos

        # Botón Siguiente
        next_btn = ctk.CTkButton(
            buttons_frame, text="Siguiente", width=80, height=34,
            font=ctk.CTkFont(size=12), fg_color="#FFFFFF", text_color="#1E293B",
            hover_color="#F1F5F9", border_width=1, border_color="#E2E8F0", corner_radius=8,
            command=self.next_page
        )
        next_btn.pack(side="left", padx=4)

    def update_pagination_label(self):
        """Actualiza el texto de la paginación."""
        if self.total_products == 0:
            self.pagination_label.configure(text="No hay productos para mostrar")
            return

        start_index = (self.current_page - 1) * self.products_per_page + 1
        end_index = min(start_index + len(self.products) - 1, self.total_products)
        self.pagination_label.configure(text=f"Mostrando {start_index}-{end_index} de {self.total_products} productos")

    def update_page_buttons(self):
        """Actualiza los botones numéricos de la paginación."""
        # Limpiar botones anteriores
        for widget in self.page_buttons_frame.winfo_children():
            widget.destroy()

        if self.total_products == 0:
            return

        total_pages = (self.total_products + self.products_per_page - 1) // self.products_per_page

        # Calcular rango de páginas a mostrar
        start_page = max(1, self.current_page - 1)
        end_page = min(total_pages, self.current_page + 1)

        # Botón para la primera página si es necesario
        if start_page > 1:
            first_btn = ctk.CTkButton(
                self.page_buttons_frame, text="1", width=34, height=34,
                font=ctk.CTkFont(size=12),
                fg_color="#FFFFFF", text_color="#1E293B", hover_color="#F1F5F9",
                border_width=1, border_color="#E2E8F0", corner_radius=8,
                command=lambda: self.go_to_page(1)
            )
            first_btn.pack(side="left", padx=2)
            if start_page > 2:
                dots_label = ctk.CTkLabel(self.page_buttons_frame, text="...", font=ctk.CTkFont(size=12))
                dots_label.pack(side="left", padx=2)

        # Botones para las páginas en el rango
        for page_num in range(start_page, end_page + 1):
            is_current = page_num == self.current_page
            btn = ctk.CTkButton(
                self.page_buttons_frame, text=str(page_num), width=34, height=34,
                font=ctk.CTkFont(size=12, weight="bold" if is_current else "normal"),
                fg_color="#00B4D8" if is_current else "#FFFFFF",
                text_color="#FFFFFF" if is_current else "#1E293B",
                hover_color="#0096B4" if is_current else "#F1F5F9",
                border_width=0 if is_current else 1,
                border_color="#E2E8F0", corner_radius=8,
                command=lambda p=page_num: self.go_to_page(p)
            )
            btn.pack(side="left", padx=2)

        # Botón para la última página si es necesario
        if end_page < total_pages:
            if end_page < total_pages - 1:
                dots_label = ctk.CTkLabel(self.page_buttons_frame, text="...", font=ctk.CTkFont(size=12))
                dots_label.pack(side="left", padx=2)
            last_btn = ctk.CTkButton(
                self.page_buttons_frame, text=str(total_pages), width=34, height=34,
                font=ctk.CTkFont(size=12),
                fg_color="#FFFFFF", text_color="#1E293B", hover_color="#F1F5F9",
                border_width=1, border_color="#E2E8F0", corner_radius=8,
                command=lambda: self.go_to_page(total_pages)
            )
            last_btn.pack(side="left", padx=2)

    def previous_page(self):
        """Va a la página anterior."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_products()

    def next_page(self):
        """Va a la página siguiente."""
        total_pages = (self.total_products + self.products_per_page - 1) // self.products_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_products()

    def go_to_page(self, page_num):
        """Va a una página específica."""
        if 1 <= page_num <= (self.total_products + self.products_per_page - 1) // self.products_per_page:
            self.current_page = page_num
            self.load_products()

    def load_products(self):
        """Carga productos desde el controlador."""
        try:
            # Usar el controlador para obtener productos
            products, total = self.controller.get_products(
                page=self.current_page,
                search=self.search_query,
                category_id=self.filter_category_id
            )
            self.products = products
            self.total_products = total

            # Cargar categorías si aún no están cargadas
            if not self.categories:
                self.categories = self.controller.get_categories()

            # Actualizar UI
            self.update_table()
            self.update_pagination_label()
            self.update_page_buttons()

            Logger.info(f"Productos cargados: {len(products)} en página {self.current_page} de {total}", "INVENTORY_VIEW")

        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_VIEW")
            # Opcional: Mostrar un mensaje de error al usuario
            # self.show_message("Error al cargar productos", "error")

    def add_product(self):
        """Acción para añadir un producto (abre un diálogo o cambia a otra vista)."""
        # Opcional: Abrir un diálogo para añadir producto
        from tkinter import messagebox
        messagebox.showinfo("Añadir Producto", "Funcionalidad en desarrollo.")

    def edit_product(self, product):
        """Acción para editar un producto."""
        # Opcional: Abrir un diálogo para editar producto
        from tkinter import messagebox
        messagebox.showinfo("Editar Producto", f"Editando producto: {product['nombre']}")

    def delete_product(self, product):
        """Acción para eliminar un producto."""
        from tkinter import messagebox
        confirmed = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el producto '{product['nombre']}'?\n\nEsta acción no se puede deshacer."
        )
        if confirmed:
            success, message = self.controller.delete_product(product['id'])
            if success:
                Logger.success(f"Producto {product['id']} eliminado", "INVENTORY_VIEW")
                # Refrescar la lista de productos
                self.load_products()
                # Mostrar mensaje de éxito
                self.show_message("Producto eliminado correctamente", "success")
            else:
                Logger.error(f"Error al eliminar producto {product['id']}: {message}", "INVENTORY_VIEW")
                self.show_message(f"Error al eliminar: {message}", "error")

    def export_inventory(self):
        """Exporta el inventario."""
        success, message = self.controller.export_inventory(format="csv", category_id=self.filter_category_id, search_query=self.search_query)
        if success:
            Logger.success(f"Inventario exportado a: {message}", "INVENTORY_VIEW")
            self.show_message(f"Exportado a: {message}", "success")
        else:
            Logger.error(f"Error al exportar inventario: {message}", "INVENTORY_VIEW")
            self.show_message(f"Error al exportar: {message}", "error")

    def show_message(self, message, msg_type="info"):
        """Muestra un mensaje temporal al usuario."""
        # Este es un ejemplo simple, puedes implementar un popup más elegante
        colors = {"info": "#3B82F6", "success": "#10B981", "warning": "#F59E0B", "error": "#EF4444"}
        color = colors.get(msg_type, "#3B82F6")

        popup = ctk.CTkToplevel(self)
        popup.title("")
        popup.geometry("300x100")
        popup.resizable(False, False)
        popup.configure(fg_color="#FFFFFF")
        popup.transient(self)
        popup.grab_set()

        # Centrar popup
        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (100 // 2)
        popup.geometry(f"300x100+{x}+{y}")

        label = ctk.CTkLabel(
            popup, text=message,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color
        )
        label.pack(expand=True)

        popup.after(3000, popup.destroy)

