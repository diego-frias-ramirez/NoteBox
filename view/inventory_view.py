"""
NoteBox - Vista del Módulo de Inventario (Versión Corregida)
Ubicación: view/inventory_view.py
"""

import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime

from components.base_view import BaseView
from controller.inventory_controller import InventoryController
from utils.alerts import alert_manager
from utils.logger import Logger
from utils.helpers import Helpers

class InventoryView(BaseView):
    """Vista del Módulo de Inventario."""

    def __init__(self, user_data):
        # Variables de estado
        self.products = []
        self.categories = {}
        self.current_page = 1
        self.products_per_page = 7
        self.total_products = 0
        self.search_query = ""
        self.filter_category_ids = []  # CAMBIADO: Lista de categorías (máximo 3)
        self.sort_order = None  # Independiente: None, "newest", "oldest"
        self.images = {}

        # Instancia del controlador
        self.controller = InventoryController()
        self.controller.set_current_user(user_data)

        # Llamar al constructor de la clase base
        super().__init__(
            user_data=user_data,
            page_id="inventario",
            page_title="Gestión de Inventario",
            page_subtitle="Administrar productos y categorías"
        )

    def create_content(self):
        """Crea el contenido específico del módulo de inventario."""
        content_frame = self.content_frame

        # Toolbar (buscador, filtros, botones)
        self.create_toolbar(content_frame)

        # Frame contenedor para la barra de filtros (se actualizará dinámicamente)
        self.filters_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.filters_container.pack(fill="x", pady=(0, 15))

        # Crear barra de filtros inicial
        self.create_filters_bar()

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

        # Icono de búsqueda
        search_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "search.png")
        try:
            img = Image.open(search_icon_path)
            img = img.resize((16, 16), Image.LANCZOS)
            search_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(16, 16))
            ctk.CTkLabel(search_frame, image=search_icon, text="").pack(side="left", padx=(18, 10))
        except:
            ctk.CTkLabel(search_frame, text="🔍", font=ctk.CTkFont(size=16), text_color="#94A3B8").pack(side="left", padx=(18, 10))

        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Buscar productos...",
            fg_color="transparent", border_width=0, font=ctk.CTkFont(size=14), height=44
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        # Botones
        btns_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btns_frame.pack(side="right")

        # Exportar
        export_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "dowload.png")
        try:
            img = Image.open(export_icon_path)
            img = img.resize((16, 16), Image.LANCZOS)
            export_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(16, 16))
            export_btn = ctk.CTkButton(
                btns_frame, text="Exportar", width=120, height=44,
                font=ctk.CTkFont(size=13), fg_color="#10B981",
                text_color="#FFFFFF", hover_color="#059669", corner_radius=10,
                image=export_icon, compound="left",
                command=self.export_inventory
            )
        except:
            export_btn = ctk.CTkButton(
                btns_frame, text="⬇  Exportar", width=120, height=44,
                font=ctk.CTkFont(size=13), fg_color="#10B981",
                text_color="#FFFFFF", hover_color="#059669", corner_radius=10,
                command=self.export_inventory
            )
        export_btn.pack(side="left", padx=(0, 12))

        # Añadir Producto
        add_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "mas.png")
        try:
            img = Image.open(add_icon_path)
            img = img.resize((16, 16), Image.LANCZOS)
            add_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(16, 16))
            add_btn = ctk.CTkButton(
                btns_frame, text="Añadir Producto", width=160, height=44,
                font=ctk.CTkFont(size=13, weight="bold"), fg_color="#00B4D8",
                text_color="#FFFFFF", hover_color="#0096B4", corner_radius=10,
                image=add_icon, compound="left",
                command=self.add_product
            )
        except:
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
        self.current_page = 1
        self.load_products()

    def open_sort_dialog(self):
        """NUEVO: Abre un diálogo para seleccionar el orden de los productos."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ordenar Productos")
        dialog.geometry("300x250")
        dialog.transient(self)
        dialog.grab_set()

        # Centrar el diálogo
        x = self.winfo_x() + (self.winfo_width() - 300) // 2
        y = self.winfo_y() + (self.winfo_height() - 250) // 2
        dialog.geometry(f"300x250+{x}+{y}")

        # Título
        title_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        title_frame.pack(fill="x", pady=(15, 5), padx=20)

        ctk.CTkLabel(
            title_frame, 
            text="📊 Ordenar Por", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        # Frame para opciones
        options_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        options_frame.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # Variable para el radio button
        selected_sort = ctk.StringVar(value=self.sort_order or "none")

        # Opciones de ordenamiento
        sort_options = [
            ("none", "Sin ordenar (por defecto)"),
            ("newest", "Más reciente primero"),
            ("oldest", "Más antiguo primero")
        ]

        for value, text in sort_options:
            radio = ctk.CTkRadioButton(
                options_frame,
                text=text,
                variable=selected_sort,
                value=value
            )
            radio.pack(anchor="w", padx=10, pady=8)

        # Botón Aplicar
        def apply_sort():
            value = selected_sort.get()
            self.sort_order = None if value == "none" else value
            self.current_page = 1
            self.load_products()
            dialog.destroy()

        apply_btn = ctk.CTkButton(
            dialog,
            text="Aplicar Orden",
            width=100,
            height=30,
            fg_color="#00B4D8",
            text_color="#FFFFFF",
            hover_color="#0096B4",
            corner_radius=8,
            command=apply_sort
        )
        apply_btn.pack(pady=10)

    def open_filter_dialog(self):
        """Abre un diálogo para seleccionar filtro por categoría (puede agregar hasta 3)."""
        # Verificar si ya hay 3 categorías seleccionadas
        if len(self.filter_category_ids) >= 3:
            alert_manager.show_warning(
                "Límite de Filtros",
                "Ya has agregado el máximo de 3 categorías.\n\nElimina alguna para agregar otra.",
                self
            )
            return
        
        categories_dict = self.controller.get_categories()

        dialog = ctk.CTkToplevel(self)
        dialog.title("Filtrar por Categoría")
        dialog.geometry("350x400")
        dialog.transient(self)
        dialog.grab_set()

        # Centrar el diálogo
        x = self.winfo_x() + (self.winfo_width() - 350) // 2
        y = self.winfo_y() + (self.winfo_height() - 400) // 2
        dialog.geometry(f"350x400+{x}+{y}")

        # Título
        title_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        title_frame.pack(fill="x", pady=(15, 5), padx=20)

        filter_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "filtro.png")
        try:
            img = Image.open(filter_icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            filter_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            ctk.CTkLabel(title_frame, image=filter_icon, text="").pack(side="left", padx=(0, 10))
        except:
            ctk.CTkLabel(title_frame, text="⚙️", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(title_frame, text="Seleccionar Categoría", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        # Subtítulo informativo
        info_label = ctk.CTkLabel(
            dialog,
            text=f"Categorías seleccionadas: {len(self.filter_category_ids)}/3",
            font=ctk.CTkFont(size=12),
            text_color="#64748B"
        )
        info_label.pack(pady=(0, 10))

        # Scrollable Frame para categorías
        categories_scrollable = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        categories_scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Variable para el checkbox seleccionado
        selected_category_id = ctk.StringVar(value="")

        # Iterar sobre las categorías del controlador
        for cat_id, cat_data in categories_dict.items():
            # Saltar categorías ya seleccionadas
            if cat_id in self.filter_category_ids:
                continue
                
            cat_radio = ctk.CTkRadioButton(
                categories_scrollable,
                text=cat_data['nombre'],
                variable=selected_category_id,
                value=str(cat_id)
            )
            cat_radio.pack(anchor="w", padx=10, pady=5)

        # Botón Aplicar
        def apply_filter():
            value = selected_category_id.get()
            if value and value != "":
                category_id = int(value)
                if category_id not in self.filter_category_ids:
                    self.filter_category_ids.append(category_id)
                    self.current_page = 1
                    self.load_products()
            dialog.destroy()

        apply_btn = ctk.CTkButton(
            dialog,
            text="Agregar Categoría",
            width=100,
            height=30,
            fg_color="#00B4D8",
            text_color="#FFFFFF",
            hover_color="#0096B4",
            corner_radius=8,
            command=apply_filter
        )
        apply_btn.pack(pady=10)

    def create_filters_bar(self):
        """Crea/Actualiza la barra de filtros activos mostrando todos los filtros aplicados."""
        # Limpiar widgets existentes en el contenedor
        for widget in self.filters_container.winfo_children():
            widget.destroy()
        
        # Crear nuevo frame para los filtros
        filters_frame = ctk.CTkFrame(self.filters_container, fg_color="transparent", height=35)
        filters_frame.pack(fill="x")

        ctk.CTkLabel(
            filters_frame, text="Filtros activos:",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(side="left", padx=(0, 12))

        # Contador de filtros de categoría
        category_filters_count = len(self.filter_category_ids)
        has_any_filter = False

        # Mostrar filtro de búsqueda si está activo (NO CUENTA PARA EL LÍMITE)
        if self.search_query.strip():
            has_any_filter = True
            tag_frame = ctk.CTkFrame(filters_frame, fg_color="#FEF3C7", corner_radius=15, height=28)
            tag_frame.pack(side="left", padx=(0, 10))
            tag_frame.pack_propagate(False)

            search_text = self.search_query if len(self.search_query) <= 20 else self.search_query[:17] + "..."
            ctk.CTkLabel(
                tag_frame, text=f"🔍 {search_text}",
                font=ctk.CTkFont(size=11), text_color="#D97706"
            ).pack(side="left", padx=(12, 5), pady=4)

            remove_tag_btn = ctk.CTkButton(
                tag_frame, text="×", width=20, height=20,
                fg_color="transparent", text_color="#D97706",
                hover_color="#FDE68A", font=ctk.CTkFont(size=14),
                command=self.clear_search_filter
            )
            remove_tag_btn.pack(side="left", padx=(0, 8))

        # Mostrar filtros de categorías (MÁXIMO 3)
        for cat_id in self.filter_category_ids:
            has_any_filter = True
            category_name = "Categoría desconocida"
            for c_id, cat_data in self.categories.items():
                if c_id == cat_id:
                    category_name = cat_data.get('nombre', 'Categoría sin nombre')
                    break

            tag_frame = ctk.CTkFrame(filters_frame, fg_color="#E0F7FA", corner_radius=15, height=28)
            tag_frame.pack(side="left", padx=(0, 10))
            tag_frame.pack_propagate(False)

            ctk.CTkLabel(
                tag_frame, text=f"📁 {category_name}",
                font=ctk.CTkFont(size=11), text_color="#00B4D8"
            ).pack(side="left", padx=(12, 5), pady=4)

            # Crear comando con closure para capturar el cat_id correcto
            def make_remove_command(category_id):
                return lambda: self.remove_category_filter(category_id)

            remove_tag_btn = ctk.CTkButton(
                tag_frame, text="×", width=20, height=20,
                fg_color="transparent", text_color="#00B4D8",
                hover_color="#B2EBF2", font=ctk.CTkFont(size=14),
                command=make_remove_command(cat_id)
            )
            remove_tag_btn.pack(side="left", padx=(0, 8))

        # Mostrar filtro de ordenamiento si está activo (NO CUENTA PARA EL LÍMITE)
        if self.sort_order:
            has_any_filter = True
            sort_text = "Más reciente" if self.sort_order == "newest" else "Más antiguo"
            tag_frame = ctk.CTkFrame(filters_frame, fg_color="#DCFCE7", corner_radius=15, height=28)
            tag_frame.pack(side="left", padx=(0, 10))
            tag_frame.pack_propagate(False)

            ctk.CTkLabel(
                tag_frame, text=f"📊 {sort_text}",
                font=ctk.CTkFont(size=11), text_color="#16A34A"
            ).pack(side="left", padx=(12, 5), pady=4)

            remove_tag_btn = ctk.CTkButton(
                tag_frame, text="×", width=20, height=20,
                fg_color="transparent", text_color="#16A34A",
                hover_color="#BBF7D0", font=ctk.CTkFont(size=14),
                command=self.clear_sort_filter
            )
            remove_tag_btn.pack(side="left", padx=(0, 8))

        # Mostrar "Ningún filtro aplicado" solo si NO hay ningún filtro
        if not has_any_filter:
            ctk.CTkLabel(
                filters_frame, text="Ningún filtro aplicado",
                font=ctk.CTkFont(size=12), text_color="#94A3B8"
            ).pack(side="left", padx=(0, 10))

        # Mostrar botón "Agregar categoría" solo si hay menos de 3 categorías
        if category_filters_count < 3:
            add_filter_btn = ctk.CTkButton(
                filters_frame, text=f"+ Agregar categoría ({category_filters_count}/3)",
                font=ctk.CTkFont(size=12), fg_color="transparent",
                text_color="#00B4D8", hover_color="#F1F5F9", width=180, height=28,
                command=self.open_filter_dialog
            )
            add_filter_btn.pack(side="left", padx=(0, 8))
        
        # Botón de ordenar (solo si NO hay ordenamiento activo)
        if not self.sort_order:
            sort_btn = ctk.CTkButton(
                filters_frame, text="📋 Ordenar",
                font=ctk.CTkFont(size=12), fg_color="transparent",
                text_color="#16A34A", hover_color="#F1F5F9", width=100, height=28,
                command=self.open_sort_dialog
            )
            sort_btn.pack(side="left")

    def remove_category_filter(self, category_id):
        """Elimina una categoría específica de los filtros."""
        if category_id in self.filter_category_ids:
            self.filter_category_ids.remove(category_id)
            self.current_page = 1
            self.load_products()

    def clear_search_filter(self):
        """Limpia el filtro de búsqueda."""
        self.search_query = ""
        self.search_entry.delete(0, 'end')
        self.current_page = 1
        self.load_products()

    def clear_sort_filter(self):
        """Limpia el filtro de ordenamiento."""
        self.sort_order = None
        self.current_page = 1
        self.load_products()

    def create_table(self, parent):
        """Crea la tabla de productos."""
        table_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        self.table_frame = table_frame

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
            ("Acciones", 120)
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

        # Acciones (Editar, Eliminar, Ver Detalles)
        actions_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=120)
        actions_frame.pack(side="left", padx=8)
        actions_frame.pack_propagate(False)

        # Botón Editar
        edit_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "edit.png")
        try:
            img = Image.open(edit_icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            edit_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            edit_btn = ctk.CTkButton(
                actions_frame, image=edit_icon, text="", width=32, height=32,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda p=product: self.edit_product(p)
            )
        except:
            edit_btn = ctk.CTkButton(
                actions_frame, text="✏️", width=32, height=32,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6, font=ctk.CTkFont(size=14),
                command=lambda p=product: self.edit_product(p)
            )
        edit_btn.pack(side="left", padx=2)

        # Botón Eliminar
        delete_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "delete.png")
        try:
            img = Image.open(delete_icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            delete_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            delete_btn = ctk.CTkButton(
                actions_frame, image=delete_icon, text="", width=32, height=32,
                fg_color="transparent", hover_color="#FEE2E2",
                corner_radius=6,
                command=lambda p=product: self.delete_product(p)
            )
        except:
            delete_btn = ctk.CTkButton(
                actions_frame, text="🗑️", width=32, height=32,
                fg_color="transparent", hover_color="#FEE2E2",
                corner_radius=6, font=ctk.CTkFont(size=14),
                command=lambda p=product: self.delete_product(p)
            )
        delete_btn.pack(side="left", padx=2)

        # Botón Ver Detalles
        details_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "products_2.png")
        try:
            img = Image.open(details_icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            details_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            details_btn = ctk.CTkButton(
                actions_frame, image=details_icon, text="", width=32, height=32,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda p=product: self.view_product_details(p)
            )
        except:
            details_btn = ctk.CTkButton(
                actions_frame, text="👁️", width=32, height=32,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6, font=ctk.CTkFont(size=14),
                command=lambda p=product: self.view_product_details(p)
            )
        details_btn.pack(side="left", padx=2)

    def create_pagination(self, parent):
        """Crea la barra de paginación."""
        pagination_frame = ctk.CTkFrame(parent, fg_color="transparent", height=45)
        pagination_frame.pack(fill="x")

        self.pagination_label = ctk.CTkLabel(
            pagination_frame, text="Mostrando 0 de 0 productos",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        )
        self.pagination_label.pack(side="left")

        buttons_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        buttons_frame.pack(side="right")

        prev_btn = ctk.CTkButton(
            buttons_frame, text="Anterior", width=80, height=34,
            font=ctk.CTkFont(size=12), fg_color="#FFFFFF", text_color="#1E293B",
            hover_color="#F1F5F9", border_width=1, border_color="#E2E8F0", corner_radius=8,
            command=self.previous_page
        )
        prev_btn.pack(side="left", padx=4)

        self.page_buttons_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        self.page_buttons_frame.pack(side="left", padx=4)
        self.update_page_buttons()

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
        for widget in self.page_buttons_frame.winfo_children():
            widget.destroy()

        if self.total_products == 0:
            return

        total_pages = (self.total_products + self.products_per_page - 1) // self.products_per_page
        start_page = max(1, self.current_page - 1)
        end_page = min(total_pages, self.current_page + 1)

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
            # Obtener productos del controlador
            # Si hay múltiples categorías, obtener productos de todas
            if self.filter_category_ids:
                # Obtener productos de cada categoría y combinarlos
                all_products = []
                total = 0
                for cat_id in self.filter_category_ids:
                    products, cat_total = self.controller.get_products(
                        page=self.current_page,
                        search=self.search_query,
                        category_id=cat_id
                    )
                    all_products.extend(products)
                    total += cat_total
                
                # Eliminar duplicados basados en ID
                seen_ids = set()
                products = []
                for product in all_products:
                    if product['id'] not in seen_ids:
                        seen_ids.add(product['id'])
                        products.append(product)
                
                total = len(products)
            else:
                # Sin filtro de categoría, obtener todos
                products, total = self.controller.get_products(
                    page=self.current_page,
                    search=self.search_query,
                    category_id=None
                )
            
            # Aplicar ordenamiento localmente si está configurado
            if self.sort_order and products:
                if self.sort_order == "newest":
                    products = sorted(products, key=lambda x: x.get('id', 0), reverse=True)
                elif self.sort_order == "oldest":
                    products = sorted(products, key=lambda x: x.get('id', 0))
            
            self.products = products
            self.total_products = total

            if not self.categories:
                self.categories = self.controller.get_categories()

            # Actualizar la barra de filtros para reflejar los cambios
            self.create_filters_bar()
            
            self.update_table()
            self.update_pagination_label()
            self.update_page_buttons()

            Logger.info(f"Productos cargados: {len(products)} en página {self.current_page} de {total}", "INVENTORY_VIEW")
            self.generate_stock_alerts(products)

        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_VIEW")
            alert_manager.show_error(
                "Error al cargar productos", 
                f"No se pudieron cargar los productos.\nError: {str(e)}",
                parent=self
            )

    def generate_stock_alerts(self, products):
        """Genera alertas automáticas para productos con stock bajo o agotado."""
        try:
            low_stock_count = 0
            no_stock_count = 0
            
            for product in products:
                alert_id = alert_manager.generate_stock_alert(product)
                if alert_id:
                    if product.get('stock', 0) <= 0:
                        no_stock_count += 1
                    else:
                        low_stock_count += 1
            
            if low_stock_count > 0 or no_stock_count > 0:
                total = len(products)
                low_rotation = alert_manager.get_low_rotation_alerts_count(products)
                alert_manager.show_stock_summary(total, low_stock_count, no_stock_count, low_rotation, self)
                
        except Exception as e:
            Logger.error(f"Error generando alertas de stock: {str(e)}", "INVENTORY_VIEW")

    def add_product(self):
        """Acción para añadir un producto."""
        self.open_add_product_dialog()

    def edit_product(self, product):
        """Acción para editar un producto."""
        self.open_edit_product_dialog(product)

    def delete_product(self, product):
        """Acción para eliminar un producto."""
        confirmed = alert_manager.confirm_delete(f"el producto '{product['nombre']}'", self)
        
        if confirmed:
            success, message = self.controller.delete_product(product['id'])
            if success:
                Logger.success(f"Producto {product['id']} eliminado", "INVENTORY_VIEW")
                self.load_products()
                alert_manager.success_delete(self)
            else:
                Logger.error(f"Error al eliminar producto {product['id']}: {message}", "INVENTORY_VIEW")
                alert_manager.error_delete(self)

    def view_product_details(self, product):
        """Acción para ver detalles de un producto."""
        message = f"=== DETALLES DEL PRODUCTO ===\n\n"
        message += f"📋 ID: {product['id']}\n"
        message += f"📦 Nombre: {product['nombre']}\n"
        message += f"🏷️  Categoría: {self.categories.get(product.get('categoria_id'), {}).get('nombre', 'Sin Categoría')}\n"
        message += f"📊 Stock: {product['stock']} unidades\n"
        message += f"💰 Precio: {Helpers.format_currency(product['precio'])}\n"
        message += f"📈 Estado: {product['estado']}\n"
        
        if product.get('descripcion'):
            message += f"\n📝 Descripción:\n{product['descripcion']}"
        
        if product.get('codigo'):
            message += f"\n🔖 Código: {product['codigo']}"
        
        alert_manager.show_info("Detalles del Producto", message, self)

    def export_inventory(self):
        """Exporta el inventario con nombre de archivo que incluye fecha."""
        confirmed = alert_manager.confirm(
            "Confirmar Exportación",
            "¿Desea exportar el inventario actual?\n\nSe generará un archivo CSV con los productos filtrados.",
            self
        )
        
        if not confirmed:
            return
        
        # Verificar si el controlador acepta el parámetro filename
        # Verificar si el controlador acepta el parámetro filename
        try:
            # Generar nombre de archivo base
            current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            default_filename = f"inventario_{current_date}.csv"
            
            # Obtener directorio por defecto
            from utils.helpers import Helpers
            default_dir = Helpers.get_exports_dir("reports")
            
            # Pedir al usuario dónde guardar (con valor por defecto)
            filepath = ctk.filedialog.asksaveasfilename(
                title="Guardar Inventario",
                initialdir=default_dir,
                initialfile=default_filename,
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
            )
            
            if not filepath:
                return # Usuario canceló selección
            
            # Si hay múltiples categorías, exportar con category_id None pero filtrado
            category_id_export = self.filter_category_ids[0] if len(self.filter_category_ids) == 1 else None
            
            # Intentar con el parámetro filepath
            success, message = self.controller.export_inventory(
                format="csv", 
                category_id=category_id_export, 
                search_query=self.search_query,
                filepath=filepath
            )
        except TypeError:
            # Si el controlador no acepta filepath, usar el método original
            Logger.info("Controlador no acepta filepath, usando método estándar", "INVENTORY_VIEW")
            category_id_export = self.filter_category_ids[0] if len(self.filter_category_ids) == 1 else None
            success, message = self.controller.export_inventory(
                format="csv", 
                category_id=category_id_export, 
                search_query=self.search_query
            )
        
        if success:
            Logger.success(f"Inventario exportado a: {message}", "INVENTORY_VIEW")
            alert_manager.show_success(
                "Exportación Exitosa", 
                f"El inventario se exportó correctamente.\n\nUbicación: {message}",
                self
            )
        else:
            Logger.error(f"Error al exportar inventario: {message}", "INVENTORY_VIEW")
            alert_manager.show_error(
                "Error al Exportar", 
                f"No se pudo exportar el inventario.\nError: {message}",
                self
            )

    def show_message(self, message, msg_type="info"):
        """Muestra un mensaje temporal al usuario."""
        if msg_type == "success":
            alert_manager.show_success("Éxito", message, self)
        elif msg_type == "error":
            alert_manager.show_error("Error", message, self)
        elif msg_type == "warning":
            alert_manager.show_warning("Advertencia", message, self)
        else:
            alert_manager.show_info("Información", message, self)

    def open_add_product_dialog(self):
        """Abre un diálogo para añadir un nuevo producto."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Añadir Nuevo Producto")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()

        x = self.winfo_x() + (self.winfo_width() // 2) - (500 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")

        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))

        icon_path = os.path.join(self.base_path, "..", "assets", "icons", "products.png")
        try:
            img = Image.open(icon_path)
            img = img.resize((32, 32), Image.LANCZOS)
            self.images["add_product_icon"] = ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))
            ctk.CTkLabel(title_frame, image=self.images["add_product_icon"], text="").pack(side="left", padx=(0, 10))
        except:
            ctk.CTkLabel(title_frame, text="📦", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(title_frame, text="Añadir Nuevo Producto", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(10, 0))

        fields = [
            ("Nombre del Producto:*", "name_entry", "Ingrese el nombre"),
            ("Código del Producto:*", "code_entry", "Ingrese el código"),
            ("Descripción:", "description_entry", ""),
            ("Categoría:*", "category_combo", ""),
            ("Stock Actual:*", "stock_entry", "Ingrese el stock"),
            ("Stock Mínimo:*", "min_stock_entry", "Ingrese el stock mínimo"),
            ("Precio Unitario:*", "price_entry", "Ingrese el precio")
        ]

        for label_text, var_name, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(field_frame, text=label_text, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(5, 0))

            if var_name == "description_entry":
                widget = ctk.CTkTextbox(field_frame, height=60)
                widget.pack(fill="x", pady=(5, 10))
            elif var_name == "category_combo":
                widget = ctk.CTkComboBox(field_frame, values=["Seleccione una categoría"])
                widget.pack(fill="x", pady=(5, 10))
            else:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder)
                widget.pack(fill="x", pady=(5, 10))

            setattr(self, var_name, widget)

        categories_list = list(self.categories.values())
        category_names = [cat['nombre'] for cat in categories_list]
        if category_names:
            self.category_combo.configure(values=category_names)
        else:
            self.category_combo.configure(values=["No hay categorías disponibles"])
            self.category_combo.set("No hay categorías disponibles")

        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))

        def save_product():
            name = self.name_entry.get().strip()
            code = self.code_entry.get().strip()
            description = self.description_entry.get("1.0", "end-1c").strip()
            category_name = self.category_combo.get().strip()
            stock_str = self.stock_entry.get().strip()
            min_stock_str = self.min_stock_entry.get().strip()
            price_str = self.price_entry.get().strip()

            required_fields = [
                ("nombre", name),
                ("código", code),
                ("categoría", category_name),
                ("stock", stock_str),
                ("stock mínimo", min_stock_str),
                ("precio", price_str)
            ]
            
            missing_fields = []
            for field_name, field_value in required_fields:
                if not field_value or field_value == "Seleccione una categoría" or field_value == "No hay categorías disponibles":
                    missing_fields.append(field_name)
            
            if missing_fields:
                alert_manager.validation_error(
                    "Por favor complete los siguientes campos obligatorios:\n\n" + 
                    "\n".join([f"• {field}" for field in missing_fields]),
                    self
                )
                return

            import re
            if not re.search(r'[a-zA-Z]', name):
                alert_manager.validation_error(
                    "El nombre del producto debe contener al menos una letra.",
                    self
                )
                return

            try:
                stock = int(stock_str)
                min_stock = int(min_stock_str)
                price = float(price_str)
                
                if stock < 0 or min_stock < 0 or price < 0:
                    raise ValueError("Los valores no pueden ser negativos")
                    
            except ValueError as e:
                if "negativos" in str(e):
                    alert_manager.validation_error(
                        "Los valores de stock y precio deben ser números positivos.",
                        self
                    )
                else:
                    alert_manager.validation_error(
                        "Stock, stock mínimo y precio deben ser números válidos.",
                        self
                    )
                return

            category_id = None
            for cat in categories_list:
                if cat['nombre'] == category_name:
                    category_id = cat['id']
                    break

            if category_id is None:
                alert_manager.show_error("Error de Categoría", "Categoría no válida.", self)
                return

            product_data = {
                "codigo": code,
                "nombre": name,
                "descripcion": description,
                "categoria_id": category_id,
                "stock": stock,
                "stock_minimo": min_stock,
                "precio": price,
                "estado": "Disponible",
                "activo": True
            }

            success, result = self.controller.create_product(product_data)
            if success:
                Logger.success(f"Producto '{name}' creado con ID {result['id']}", "INVENTORY_VIEW")
                dialog.destroy()
                self.load_products()
                alert_manager.success_save(self)
                alert_manager.generate_movement_alert(result, "Entrada", stock, "Creación de nuevo producto")
            else:
                Logger.error(f"Error al crear producto '{name}': {result}", "INVENTORY_VIEW")
                alert_manager.show_error("Error al Crear", f"No se pudo crear el producto.\nError: {result}", self)

        save_btn = ctk.CTkButton(
            buttons_frame, text="Guardar Producto", width=150, height=30,
            fg_color="#00B4D8", text_color="#FFFFFF", hover_color="#0096B4",
            command=save_product
        )
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(
            buttons_frame, text="Cancelar", width=150, height=30,
            fg_color="#E5E7EB", text_color="#1E293B", hover_color="#D1D5DB",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=10)

    def open_edit_product_dialog(self, product):
        """Abre un diálogo para editar un producto existente."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Editar Producto: {product['nombre']}")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()

        x = self.winfo_x() + (self.winfo_width() // 2) - (500 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")

        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))

        icon_path = os.path.join(self.base_path, "..", "assets", "icons", "products.png")
        try:
            img = Image.open(icon_path)
            img = img.resize((32, 32), Image.LANCZOS)
            self.images["edit_product_icon"] = ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))
            ctk.CTkLabel(title_frame, image=self.images["edit_product_icon"], text="").pack(side="left", padx=(0, 10))
        except:
            ctk.CTkLabel(title_frame, text="📦", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(title_frame, text=f"Editar Producto: {product['nombre']}", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, pady=(10, 0))

        fields = [
            ("Nombre del Producto:*", "name_entry", "Ingrese el nombre"),
            ("Código del Producto:*", "code_entry", "Ingrese el código"),
            ("Descripción:", "description_entry", ""),
            ("Categoría:*", "category_combo", ""),
            ("Stock Actual:*", "stock_entry", "Ingrese el stock"),
            ("Stock Mínimo:*", "min_stock_entry", "Ingrese el stock mínimo"),
            ("Precio Unitario:*", "price_entry", "Ingrese el precio")
        ]

        for label_text, var_name, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(field_frame, text=label_text, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(5, 0))

            if var_name == "description_entry":
                widget = ctk.CTkTextbox(field_frame, height=60)
                widget.pack(fill="x", pady=(5, 10))
            elif var_name == "category_combo":
                widget = ctk.CTkComboBox(field_frame, values=["Seleccione una categoría"])
                widget.pack(fill="x", pady=(5, 10))
            else:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder)
                widget.pack(fill="x", pady=(5, 10))

            setattr(self, var_name, widget)

        categories_list = list(self.categories.values())
        category_names = [cat['nombre'] for cat in categories_list]
        if category_names:
            self.category_combo.configure(values=category_names)
        else:
            self.category_combo.configure(values=["No hay categorías disponibles"])
            self.category_combo.set("No hay categorías disponibles")

        current_category_name = self.categories.get(product.get('categoria_id'), {}).get('nombre', 'Sin Categoría')
        self.category_combo.set(current_category_name)

        self.name_entry.insert(0, product['nombre'])
        self.code_entry.insert(0, product['codigo'])
        self.description_entry.insert("1.0", product['descripcion'] if product.get('descripcion') else "")
        self.stock_entry.insert(0, str(product['stock']))
        self.min_stock_entry.insert(0, str(product['stock_minimo']))
        self.price_entry.insert(0, str(product['precio']))

        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))

        def save_edited_product():
            name = self.name_entry.get().strip()
            code = self.code_entry.get().strip()
            description = self.description_entry.get("1.0", "end-1c").strip()
            category_name = self.category_combo.get().strip()
            stock_str = self.stock_entry.get().strip()
            min_stock_str = self.min_stock_entry.get().strip()
            price_str = self.price_entry.get().strip()

            required_fields = [
                ("nombre", name),
                ("código", code),
                ("categoría", category_name),
                ("stock", stock_str),
                ("stock mínimo", min_stock_str),
                ("precio", price_str)
            ]
            
            missing_fields = []
            for field_name, field_value in required_fields:
                if not field_value or field_value == "Seleccione una categoría" or field_value == "No hay categorías disponibles":
                    missing_fields.append(field_name)
            
            if missing_fields:
                alert_manager.validation_error(
                    "Por favor complete los siguientes campos obligatorios:\n\n" + 
                    "\n".join([f"• {field}" for field in missing_fields]),
                    self
                )
                return

            import re
            if not re.search(r'[a-zA-Z]', name):
                alert_manager.validation_error(
                    "El nombre del producto debe contener al menos una letra.",
                    self
                )
                return

            try:
                stock = int(stock_str)
                min_stock = int(min_stock_str)
                price = float(price_str)
                
                if stock < 0 or min_stock < 0 or price < 0:
                    raise ValueError("Los valores no pueden ser negativos")
                    
            except ValueError as e:
                if "negativos" in str(e):
                    alert_manager.validation_error(
                        "Los valores de stock y precio deben ser números positivos.",
                        self
                    )
                else:
                    alert_manager.validation_error(
                        "Stock, stock mínimo y precio deben ser números válidos.",
                        self
                    )
                return

            category_id = None
            for cat in categories_list:
                if cat['nombre'] == category_name:
                    category_id = cat['id']
                    break

            if category_id is None:
                alert_manager.show_error("Error de Categoría", "Categoría no válida.", self)
                return

            old_stock = product['stock']
            stock_difference = stock - old_stock
            movement_type = "Entrada" if stock_difference > 0 else "Salida" if stock_difference < 0 else None

            product_data = {
                "nombre": name,
                "codigo": code,
                "descripcion": description,
                "categoria_id": category_id,
                "stock": stock,
                "stock_minimo": min_stock,
                "precio": price,
                "estado": product['estado'],
                "activo": product['activo']
            }

            success, result = self.controller.update_product(product['id'], product_data)
            if success:
                Logger.success(f"Producto ID {product['id']} actualizado", "INVENTORY_VIEW")
                dialog.destroy()
                self.load_products()
                alert_manager.success_update(self)
                
                if movement_type and stock_difference != 0:
                    alert_manager.generate_movement_alert(
                        result,
                        movement_type,
                        abs(stock_difference),
                        f"Actualización de producto: {name}"
                    )
            else:
                Logger.error(f"Error al actualizar producto ID {product['id']}: {result}", "INVENTORY_VIEW")
                alert_manager.show_error("Error al Actualizar", f"No se pudo actualizar el producto.\nError: {result}", self)

        save_btn = ctk.CTkButton(
            buttons_frame, text="Guardar Cambios", width=150, height=30,
            fg_color="#00B4D8", text_color="#FFFFFF", hover_color="#0096B4",
            command=save_edited_product
        )
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(
            buttons_frame, text="Cancelar", width=150, height=30,
            fg_color="#E5E7EB", text_color="#1E293B", hover_color="#D1D5DB",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=10)

    def get_notification_count(self):
        """Obtiene el número de notificaciones no leídas."""
        return alert_manager.get_unread_count()