"""
NoteBox - Vista del Módulo de Usuarios (Corregida y Alineada con Figma)
Ubicación: view/users_view.py
"""
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os

from components.base_view import BaseView
from controller.users_controller import UsersController
from utils.alerts import alert_manager
from utils.logger import Logger
from utils.helpers import Helpers

class UsersView(BaseView):
    """Vista del Módulo de Usuarios."""

    def __init__(self, user_data):
        # Variables de estado
        self.users = []
        self.current_page = 1
        self.users_per_page = 5
        self.total_users = 0
        self.search_query = ""
        self.filter_role = None
        self.user_roles = {}
        self.images = {}

        # Instancia del controlador
        self.controller = UsersController()
        self.controller.set_current_user(user_data) # Pasar datos del usuario actual al controlador

        # Llamar al constructor de la clase base
        super().__init__(
            user_data=user_data,
            page_id="usuarios", # Este ID debe coincidir con el del sidebar
            page_title="Gestión de Usuarios",
            page_subtitle="Administrar cuentas y permisos de acceso"
        )

    def _load_icon(self, name, size=(20, 20)):
        """Intenta cargar un icono desde `assets/icons` probando varias extensiones y cacheándolo.

        Devuelve un `CTkImage` o `None` si no se encuentra/puede cargar.
        """
        # Usar cache si ya fue cargado (incluyendo tamaño)
        key = f"{name}:{size[0]}x{size[1]}"
        if key in self.images:
            return self.images[key]

        icons_dir = os.path.join(self.base_path, "..", "assets", "icons")
        candidates = [name, f"{name}.png", f"{name}.ico", f"{name}.jpg", f"{name}.gif"]

        for cand in candidates:
            path = os.path.join(icons_dir, cand)
            try:
                if os.path.exists(path):
                    img = Image.open(path)
                    img = img.resize(size, Image.LANCZOS)
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                    self.images[key] = ctk_img
                    return ctk_img
            except Exception:
                # Intentar siguiente candidato
                continue

        return None

    def create_content(self):
        """Crea el contenido específico del módulo de usuarios."""
        # Frame principal para el contenido (heredado de BaseView)
        content_frame = self.content_frame

        # Toolbar (buscador, botón "Crear Usuario")
        self.create_toolbar(content_frame)

        # Resumen de usuarios (Tarjetas Administradores/Empleados)
        self.create_summary_cards(content_frame)

        # Tabla de usuarios
        self.create_table(content_frame)

        # Descripción de roles
        self.create_roles_description(content_frame)

        # Cargar datos iniciales
        self.load_data()

    def create_toolbar(self, parent):
        """Crea la barra de herramientas (buscador, botón "Crear Usuario")."""
        toolbar = ctk.CTkFrame(parent, fg_color="transparent", height=60)
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
            search_frame, placeholder_text="Buscar usuarios...",
            fg_color="transparent", border_width=0, font=ctk.CTkFont(size=14), height=44
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        # Botón Crear Usuario
        add_icon = self._load_icon("mas", size=(18, 18))
        if add_icon:
            create_btn = ctk.CTkButton(
                toolbar, text=" Crear Usuario", width=160, height=44,
                font=ctk.CTkFont(size=13, weight="bold"), fg_color="#00B4D8",
                text_color="#FFFFFF", hover_color="#0096B4", corner_radius=10,
                image=add_icon, compound="left",
                command=self.open_create_user_dialog
            )
        else:
            create_btn = ctk.CTkButton(
                toolbar, text="➕ Crear Usuario", width=160, height=44,
                font=ctk.CTkFont(size=13, weight="bold"), fg_color="#00B4D8",
                text_color="#FFFFFF", hover_color="#0096B4", corner_radius=10,
                command=self.open_create_user_dialog
            )
        create_btn.pack(side="right")

    def on_search_change(self, event):
        """Evento que se dispara al cambiar el texto de búsqueda."""
        self.search_query = self.search_entry.get().strip()
        self.current_page = 1 # Reiniciar a la primera página al buscar
        self.load_users()

    def create_summary_cards(self, parent):
        """Crea las tarjetas de resumen (Administradores/Empleados)."""
        summary_frame = ctk.CTkFrame(parent, fg_color="transparent")
        summary_frame.pack(fill="x", pady=(0, 15))

        # Tarjeta Administradores
        admin_card = ctk.CTkFrame(summary_frame, fg_color="#38B6FF", corner_radius=15)
        admin_card.pack(side="left", fill="x", expand=True, padx=(0, 10))

        admin_inner = ctk.CTkFrame(admin_card, fg_color="transparent")
        admin_inner.pack(fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(
            admin_inner,
            text="Administradores",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")

        self.admin_count_label = ctk.CTkLabel(
            admin_inner,
            text="0 usuarios",
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF"
        )
        self.admin_count_label.pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            admin_inner,
            text="Acceso total al sistema",
            font=ctk.CTkFont(size=11),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(5, 0))

        # Icono de escudo
        shield_icon = self._load_icon("dashboard", size=(24, 24))
        if shield_icon:
            ctk.CTkLabel(admin_inner, image=shield_icon, text="").place(relx=0.95, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(admin_inner, text="🛡️", font=ctk.CTkFont(size=16), text_color="#FFFFFF").place(relx=0.95, rely=0.5, anchor="center")

        # Tarjeta Empleados
        employee_card = ctk.CTkFrame(summary_frame, fg_color="#F0F0F0", corner_radius=15)
        employee_card.pack(side="right", fill="x", expand=True, padx=(10, 0))

        employee_inner = ctk.CTkFrame(employee_card, fg_color="transparent")
        employee_inner.pack(fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(
            employee_inner,
            text="Empleados",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w")

        self.employee_count_label = ctk.CTkLabel(
            employee_inner,
            text="0 usuarios",
            font=ctk.CTkFont(size=12),
            text_color="#2b2d42"
        )
        self.employee_count_label.pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            employee_inner,
            text="Acceso limitado según permisos",
            font=ctk.CTkFont(size=11),
            text_color="#6c757d"
        ).pack(anchor="w", pady=(5, 0))

        # Icono de usuario
        user_icon = self._load_icon("user_avatar", size=(24, 24))
        if user_icon:
            ctk.CTkLabel(employee_inner, image=user_icon, text="").place(relx=0.95, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(employee_inner, text="👤", font=ctk.CTkFont(size=16), text_color="#2b2d42").place(relx=0.95, rely=0.5, anchor="center")

    def create_table(self, parent):
        """Crea la tabla de usuarios con encabezado sincronizado."""
        table_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        self.table_frame = table_frame

        self.columns = [
            ("Usuario", 140),
            ("Nombre", 180),
            ("Email", 200),
            ("Rol", 120),
            ("Estado", 100),
            ("Último Acceso", 150),
            ("Acciones", 160)
        ]

        # Calcular ancho mínimo de tabla
        total_columns_width = sum(w for _, w in self.columns)
        total_padding = len(self.columns) * 16 + 40
        self._table_min_width = total_columns_width + total_padding

        # Contenedor principal con canvas para scroll sincronizado
        main_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Canvas principal para el contenido
        self.main_canvas = tk.Canvas(main_container, bg="#FFFFFF", highlightthickness=0, height=400)
        v_scroll = tk.Scrollbar(main_container, orient="vertical", command=self.main_canvas.yview)
        h_scroll = tk.Scrollbar(main_container, orient="horizontal", command=self.main_canvas.xview)
        self.main_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.main_canvas.pack(side="left", fill="both", expand=True)

        # Frame principal que contiene encabezado + filas
        self.table_content_frame = ctk.CTkFrame(self.main_canvas, fg_color="transparent")
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.table_content_frame, anchor="nw")

        # Crear encabezado dentro del canvas
        self.header_frame = ctk.CTkFrame(self.table_content_frame, fg_color="#F8FAFC", height=50)
        self.header_frame.pack(fill="x", padx=5, pady=0)
        self.header_frame.pack_propagate(False)

        header_inner = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_inner.pack(fill="both", expand=True, padx=5, pady=8)

        for name, width in self.columns:
            col_frame = ctk.CTkFrame(header_inner, fg_color="transparent", width=width)
            col_frame.pack(side="left", padx=8)
            col_frame.pack_propagate(False)
            ctk.CTkLabel(
                col_frame, text=name,
                font=ctk.CTkFont(size=12, weight="bold"), text_color="#64748B", anchor="w"
            ).pack(side="left", fill="both", expand=True)

        # Separador
        separator = ctk.CTkFrame(self.table_content_frame, fg_color="#E2E8F0", height=1)
        separator.pack(fill="x", padx=5)

        # Frame para las filas
        self.rows_container = ctk.CTkFrame(self.table_content_frame, fg_color="transparent")
        self.rows_container.pack(fill="both", expand=True)

        # Actualizar scrollregion
        def _on_frame_config(event):
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        self.table_content_frame.bind("<Configure>", _on_frame_config)

        # Ajustar ancho del contenido
        def _on_canvas_config(event):
            try:
                new_w = max(event.width, self._table_min_width)
                self.main_canvas.itemconfig(self.canvas_window, width=new_w)
            except Exception:
                pass
        self.main_canvas.bind("<Configure>", _on_canvas_config)

        # Soporte de rueda del ratón
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Footer con paginación
        footer_frame = ctk.CTkFrame(table_frame, fg_color="transparent", height=40)
        footer_frame.pack(fill="x", padx=15, pady=(0, 15))
        footer_frame.pack_propagate(False)

        self.pagination_label = ctk.CTkLabel(
            footer_frame, text="No hay usuarios para mostrar",
            font=ctk.CTkFont(size=11), text_color="#64748B", anchor="w"
        )
        self.pagination_label.pack(side="left")

    def update_table(self):
        """Actualiza la tabla con los usuarios cargados."""
        # Limpiar filas anteriores
        for widget in self.rows_container.winfo_children():
            widget.destroy()

        if not self.users:
            # Mensaje si no hay usuarios
            no_users_label = ctk.CTkLabel(
                self.rows_container,
                text="No se encontraron usuarios con los filtros aplicados.",
                font=ctk.CTkFont(size=14), text_color="#6B7280"
            )
            no_users_label.pack(expand=True, pady=20)
            return

        # Crear filas para cada usuario
        for i, user in enumerate(self.users):
            is_even = i % 2 == 0
            self.create_user_row(self.rows_container, user, is_even)

    def create_user_row(self, parent, user, is_even):
        """Crea una fila para un usuario en la tabla."""
        bg_color = "#FFFFFF" if is_even else "#F8FAFC"
        row_frame = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=0, height=60)
        row_frame.pack(fill="x", pady=2, padx=0)
        row_frame.pack_propagate(False)

        inner_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=5, pady=8)

        # Usuario (140px)
        user_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=140)
        user_frame.pack(side="left", padx=8)
        user_frame.pack_propagate(False)
        ctk.CTkLabel(user_frame, text=user["username"], font=ctk.CTkFont(size=11), text_color="#1E293B", anchor="w").pack(side="left", fill="both", expand=True)

        # Nombre (180px)
        nombre_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=180)
        nombre_frame.pack(side="left", padx=8)
        nombre_frame.pack_propagate(False)
        ctk.CTkLabel(nombre_frame, text=user["nombre"], font=ctk.CTkFont(size=11), text_color="#1E293B", anchor="w").pack(side="left", fill="both", expand=True)

        # Email (200px)
        email_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=200)
        email_frame.pack(side="left", padx=8)
        email_frame.pack_propagate(False)
        ctk.CTkLabel(email_frame, text=user["email"], font=ctk.CTkFont(size=11), text_color="#1E293B", anchor="w").pack(side="left", fill="both", expand=True)

        # Rol (120px)
        role_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=120)
        role_frame.pack(side="left", padx=8)
        role_frame.pack_propagate(False)

        role_name = user["rol"].lower() if user["rol"] else "empleado"
        role_colors = {
            "admin": ("#00B4D8", "#FFFFFF"),
            "administrador": ("#00B4D8", "#FFFFFF"),
            "empleado": ("#E5E7EB", "#1E293B")
        }
        bg_color, text_color = role_colors.get(role_name, ("#E5E7EB", "#1E293B"))

        role_badge = ctk.CTkFrame(role_frame, fg_color=bg_color, corner_radius=8, height=26)
        role_badge.pack(side="left")
        ctk.CTkLabel(
            role_badge, text=role_name.upper(),
            font=ctk.CTkFont(size=10, weight="bold"), text_color=text_color
        ).pack(padx=8, pady=4)

        # Estado (100px)
        status_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=100)
        status_frame.pack(side="left", padx=8)
        status_frame.pack_propagate(False)

        status = user["estado"]
        badge_colors = {
            "Activo": ("#DCFCE7", "#16A34A"),
            "Inactivo": ("#FEE2E2", "#DC2626"),
            "Pendiente": ("#FEF3C7", "#D97706")
        }
        bg_color, text_color = badge_colors.get(status, badge_colors["Activo"])

        badge = ctk.CTkFrame(status_frame, fg_color=bg_color, corner_radius=12, height=26)
        badge.pack(side="left")
        ctk.CTkLabel(
            badge, text=status,
            font=ctk.CTkFont(size=10, weight="bold"), text_color=text_color
        ).pack(padx=12, pady=4)

        # Último Acceso (150px)
        ultimo_acceso_text = ""
        try:
            if user["ultimo_acceso"]:
                ultimo_acceso_text = user["ultimo_acceso"].strftime("%Y-%m-%d") 
            else:
                ultimo_acceso_text = "Nunca"
        except Exception:
            ultimo_acceso_text = "Nunca"
            
        ultimo_acceso_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=150)
        ultimo_acceso_frame.pack(side="left", padx=8)
        ultimo_acceso_frame.pack_propagate(False)
        ctk.CTkLabel(ultimo_acceso_frame, text=ultimo_acceso_text, font=ctk.CTkFont(size=11), text_color="#64748B", anchor="w").pack(side="left", fill="both", expand=True)

        # Acciones (160px) - Ancho suficiente para los 3 botones
        actions_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=160)
        actions_frame.pack(side="left", padx=8)
        actions_frame.pack_propagate(False)

        # Botón Editar
        edit_icon = self._load_icon("edit", size=(18, 18))
        if edit_icon:
            edit_btn = ctk.CTkButton(
                actions_frame, image=edit_icon, text="", width=32, height=32,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda u=user: self.edit_user(u)
            )
        else:
            edit_btn = ctk.CTkButton(
                actions_frame, text="✏️", width=32, height=32,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda u=user: self.edit_user(u)
            )
        edit_btn.pack(side="left", padx=3)

        # Botón Cambiar Estado
        status_icon = self._load_icon("low_stock", size=(18, 18))
        if status_icon:
            status_btn = ctk.CTkButton(
                actions_frame, image=status_icon, text="", width=32, height=32,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda u=user: self.toggle_user_status(u)
            )
        else:
            status_btn = ctk.CTkButton(
                actions_frame, text="🔄", width=32, height=32,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda u=user: self.toggle_user_status(u)
            )
        status_btn.pack(side="left", padx=3)

        # Botón Eliminar
        delete_icon = self._load_icon("delete", size=(18, 18))
        if delete_icon:
            delete_btn = ctk.CTkButton(
                actions_frame, image=delete_icon, text="", width=32, height=32,
                fg_color="transparent", hover_color="#FEE2E2",
                corner_radius=6,
                command=lambda u=user: self.delete_user(u)
            )
        else:
            delete_btn = ctk.CTkButton(
                actions_frame, text="🗑️", width=32, height=32,
                fg_color="transparent", hover_color="#FEE2E2",
                corner_radius=6,
                command=lambda u=user: self.delete_user(u)
            )
        delete_btn.pack(side="left", padx=3)

    def create_roles_description(self, parent):
        """Crea la descripción de los roles (Administrador y Empleado)."""
        roles_frame = ctk.CTkFrame(parent, fg_color="transparent")
        roles_frame.pack(fill="x", pady=(0, 20))

        # Título
        ctk.CTkLabel(
            roles_frame,
            text="Roles del Sistema",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2b2d42"
        ).pack(anchor="w", pady=(0, 15))

        # Rol Administrador
        admin_role_frame = ctk.CTkFrame(roles_frame, fg_color="#E0F7FA", corner_radius=12)
        admin_role_frame.pack(fill="x", pady=(0, 15))

        admin_inner = ctk.CTkFrame(admin_role_frame, fg_color="transparent")
        admin_inner.pack(fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(
            admin_inner,
            text="🔒 Rol: Administrador",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00B4D8"
        ).pack(anchor="w")

        ctk.CTkLabel(
            admin_inner,
            text="• Acceso completo al sistema\n• Gestión de usuarios y permisos\n• Configuración del sistema\n• Exportar e importar datos",
            font=ctk.CTkFont(size=12),
            text_color="#1E293B",
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))

        # Rol Empleado
        employee_role_frame = ctk.CTkFrame(roles_frame, fg_color="#F0F0F0", corner_radius=12)
        employee_role_frame.pack(fill="x", pady=(0, 15))

        employee_inner = ctk.CTkFrame(employee_role_frame, fg_color="transparent")
        employee_inner.pack(fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(
            employee_inner,
            text="👤 Rol: Empleado",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#6c757d"
        ).pack(anchor="w")

        ctk.CTkLabel(
            employee_inner,
            text="• Gestión de inventario\n• Registro de entradas/salidas\n• Ver reportes básicos\n• Sin acceso a configuración",
            font=ctk.CTkFont(size=12),
            text_color="#1E293B",
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))

    def load_data(self):
        """Carga los datos iniciales: usuarios, resumen y roles."""
        try:
            # Cargar usuarios
            self.load_users()

            # Cargar resumen de usuarios
            summary = self.controller.get_users_summary()
            self.update_summary_cards(summary)

            # Cargar roles
            self.user_roles = {role['id']: role for role in self.controller.get_user_roles()}

        except Exception as e:
            Logger.log_error_exception(e, "USERS_VIEW")
            alert_manager.show_error(
                "Error al cargar datos", 
                f"No se pudieron cargar los datos iniciales.\n\nError: {str(e)}",
                self
            )

    def load_users(self):
        """Carga usuarios desde el controlador."""
        try:
            # Usar el controlador para obtener usuarios
            users, total = self.controller.get_users(
                page=self.current_page,
                search=self.search_query,
                role_filter=self.filter_role
            )
            self.users = users
            self.total_users = total

            # Actualizar UI
            self.update_table()
            self.update_pagination_label()

        except Exception as e:
            Logger.log_error_exception(e, "USERS_VIEW")
            alert_manager.show_error(
                "Error al cargar usuarios", 
                "No se pudieron cargar los usuarios.\n\nPor favor, intente de nuevo.",
                self
            )

    def update_summary_cards(self, summary):
        """Actualiza las tarjetas de resumen con los datos del resumen."""
        self.admin_count_label.configure(text=f"{summary['admin']} usuarios")
        self.employee_count_label.configure(text=f"{summary['empleado']} usuarios")

    def update_pagination_label(self):
        """Actualiza el texto de la paginación."""
        if self.total_users == 0:
            self.pagination_label.configure(text="No hay usuarios para mostrar")
            return

        start_index = (self.current_page - 1) * self.users_per_page + 1
        end_index = min(start_index + len(self.users) - 1, self.total_users)
        self.pagination_label.configure(
            text=f"Mostrando {start_index}-{end_index} de {self.total_users} usuarios | Página {self.current_page}"
        )

    def open_create_user_dialog(self):
        """Abre un diálogo para crear un nuevo usuario."""
        self.open_add_user_dialog()

    def open_add_user_dialog(self):
        """Abre un diálogo para añadir un nuevo usuario."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Crear Nuevo Usuario")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()

        # Centrar el diálogo
        x = self.winfo_x() + (self.winfo_width() // 2) - (500 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")

        # Título con ícono
        title_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        title_frame.pack(fill="x", pady=(20, 10), padx=20)

        user_icon = self._load_icon("users", size=(32, 32))
        if user_icon:
            ctk.CTkLabel(title_frame, image=user_icon, text="").pack(side="left", padx=(0, 10))
        else:
            ctk.CTkLabel(title_frame, text="👥", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 10))
            
        ctk.CTkLabel(
            title_frame,
            text="Crear Nuevo Usuario",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2b2d42"
        ).pack(side="left")

        # Scrollable Frame para el formulario
        form_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Campos del formulario
        fields = [
            ("Nombre Completo:*", "name_entry", "Ingrese el nombre completo"),
            ("Nombre de Usuario:*", "username_entry", "Ingrese el nombre de usuario"),
            ("Email:*", "email_entry", "ejemplo@empresa.com"),
            ("Contraseña:*", "password_entry", "Ingrese la contraseña"),
            ("Confirmar Contraseña:*", "confirm_password_entry", "Confirme la contraseña")
        ]

        for label_text, var_name, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(
                field_frame, text=label_text, font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=(5, 0))

            if var_name in ["password_entry", "confirm_password_entry"]:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder, show="•")
            else:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder)
            widget.pack(fill="x", pady=(5, 10))

            setattr(self, var_name, widget)  # Guardar referencia

        # Rol
        ctk.CTkLabel(
            form_frame, text="Rol:*", font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(10, 0))

        self.role_combo = ctk.CTkComboBox(form_frame, values=["Seleccione un rol"])
        self.role_combo.pack(fill="x", pady=(5, 10))

        # Cargar roles en el combo box
        roles_list = [role['name'] for role in self.user_roles.values()]
        if roles_list:
            self.role_combo.configure(values=roles_list)
            self.role_combo.set(roles_list[0])
        else:
            self.role_combo.configure(values=["No hay roles disponibles"])
            self.role_combo.set("No hay roles disponibles")

        # Botones de acción
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(0, 20), padx=20)

        def save_user():
            # Validar campos
            name = self.name_entry.get().strip()
            username = self.username_entry.get().strip()
            email = self.email_entry.get().strip()
            password = self.password_entry.get().strip()
            confirm_password = self.confirm_password_entry.get().strip()
            role_name = self.role_combo.get().strip()

            # Validación básica
            required_fields = [
                ("nombre completo", name),
                ("nombre de usuario", username),
                ("email", email),
                ("contraseña", password),
                ("confirmar contraseña", confirm_password),
                ("rol", role_name)
            ]
            
            missing_fields = []
            for field_name, field_value in required_fields:
                if not field_value or field_value == "Seleccione un rol" or field_value == "No hay roles disponibles":
                    missing_fields.append(field_name)
            
            if missing_fields:
                alert_manager.validation_error(
                    "Por favor complete los siguientes campos obligatorios:\n\n" + 
                    "\n".join([f"• {field}" for field in missing_fields]),
                    self
                )
                return

            # Validar formato de email
            if "@" not in email or "." not in email:
                alert_manager.validation_error(
                    "Por favor ingrese una dirección de email válida.\n\nEjemplo: usuario@empresa.com",
                    self
                )
                return

            if password != confirm_password:
                alert_manager.validation_error(
                    "Las contraseñas no coinciden.\n\nPor favor, asegúrese de que ambas contraseñas sean iguales.",
                    self
                )
                return

            # Validar fortaleza de contraseña
            if len(password) < 6:
                alert_manager.validation_error(
                    "La contraseña debe tener al menos 6 caracteres.\n\nPor seguridad, use una contraseña más larga.",
                    self
                )
                return


            # Validar formato de nombre (solo letras y espacios)
            import re
            if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", name):
                alert_manager.validation_error(
                    "El nombre solo puede contener letras y espacios.",
                    self
                )
                return

            # Validar formato de usuario (letras y números)
            if not re.match(r"^[a-zA-Z0-9]+$", username):
                alert_manager.validation_error(
                    "El usuario solo puede contener letras y números (sin espacios ni símbolos).",
                    self
                )
                return

            # Obtener el ID del rol
            role_id = None
            for rid, role_data in self.user_roles.items():
                if role_data['name'] == role_name:
                    role_id = rid
                    break

            if role_id is None:
                alert_manager.show_error("Error de Rol", "Rol no válido.", self)
                return

            # Confirmar creación
            confirm_message = f"¿Está seguro de crear el usuario '{name}'?\n\n"
            confirm_message += f"• Nombre de usuario: {username}\n"
            confirm_message += f"• Email: {email}\n"
            confirm_message += f"• Rol: {role_name}\n\n"
            confirm_message += "El usuario recibirá acceso al sistema según los permisos del rol asignado."

            if not alert_manager.confirm("Confirmar Creación de Usuario", confirm_message, self):
                return

            # Preparar datos para enviar al controlador
            user_data = {
                "nombre": name,
                "username": username,
                "email": email,
                "password": password,
                "rol": role_id
            }

            # Usar el controlador para crear el usuario
            success, result = self.controller.create_user(user_data)
            if success:
                Logger.success(f"Usuario '{name}' creado con ID {result.get('id', 'N/A')}", "USERS_VIEW")
                # Cerrar el diálogo
                dialog.destroy()
                # Recargar la lista de usuarios
                self.load_users()
                # Actualizar resumen
                summary = self.controller.get_users_summary()
                self.update_summary_cards(summary)
                # Mostrar mensaje de éxito
                alert_manager.show_success(
                    "Usuario Creado", 
                    f"El usuario '{name}' ha sido creado exitosamente.\n\n"
                    f"• Nombre de usuario: {username}\n"
                    f"• Email: {email}\n"
                    f"• Rol: {role_name}\n"
                    f"• Estado: Activo\n\n"
                    f"El usuario ya puede iniciar sesión en el sistema.",
                    self
                )
            else:
                Logger.error(f"Error al crear usuario '{name}': {result}", "USERS_VIEW")
                alert_manager.show_error(
                    "Error al Crear Usuario", 
                    f"No se pudo crear el usuario.\n\nError: {result}",
                    self
                )

        # Botón Guardar
        save_btn = ctk.CTkButton(
            buttons_frame, text="💾 Guardar Usuario", width=150, height=40,
            fg_color="#00B4D8", text_color="#FFFFFF", hover_color="#0096B4",
            command=save_user
        )
        save_btn.pack(side="left", padx=10)

        # Botón Cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame, text="Cancelar", width=150, height=40,
            fg_color="#E5E7EB", text_color="#1E293B", hover_color="#D1D5DB",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=10)

    def edit_user(self, user):
        """Acción para editar un usuario (abre un diálogo)."""
        self.open_edit_user_dialog(user)

    def open_edit_user_dialog(self, user):
        """Abre un diálogo para editar un usuario existente."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Editar Usuario: {user['nombre']}")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()

        # Centrar el diálogo
        x = self.winfo_x() + (self.winfo_width() // 2) - (500 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")

        # Título con ícono
        title_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        title_frame.pack(fill="x", pady=(20, 10), padx=20)

        user_icon = self._load_icon("users", size=(32, 32))
        if user_icon:
            ctk.CTkLabel(title_frame, image=user_icon, text="").pack(side="left", padx=(0, 10))
        else:
            ctk.CTkLabel(title_frame, text="👤", font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 10))
            
        ctk.CTkLabel(
            title_frame,
            text=f"Editar Usuario: {user['nombre']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2b2d42"
        ).pack(side="left")

        # Scrollable Frame para el formulario
        form_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Campos del formulario
        fields = [
            ("Nombre Completo:*", "name_entry", "Ingrese el nombre completo"),
            ("Nombre de Usuario:*", "username_entry", "Ingrese el nombre de usuario"),
            ("Email:*", "email_entry", "ejemplo@empresa.com"),
            ("Nueva Contraseña (opcional):", "password_entry", "Deje vacío para mantener la actual"),
            ("Confirmar Nueva Contraseña:", "confirm_password_entry", "Confirme la nueva contraseña")
        ]

        for label_text, var_name, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(
                field_frame, text=label_text, font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=(5, 0))

            if var_name in ["password_entry", "confirm_password_entry"]:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder, show="•")
            else:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder)
            widget.pack(fill="x", pady=(5, 10))

            setattr(self, var_name, widget)  # Guardar referencia

        # Rol
        ctk.CTkLabel(
            form_frame, text="Rol:*", font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(10, 0))

        self.role_combo = ctk.CTkComboBox(form_frame, values=["Seleccione un rol"])
        self.role_combo.pack(fill="x", pady=(5, 10))

        # Cargar roles en el combo box
        roles_list = [role['name'] for role in self.user_roles.values()]
        if roles_list:
            self.role_combo.configure(values=roles_list)
        else:
            self.role_combo.configure(values=["No hay roles disponibles"])
            self.role_combo.set("No hay roles disponibles")

        # Rellenar campos con los datos actuales del usuario
        self.name_entry.insert(0, user['nombre'])
        self.username_entry.insert(0, user['username'])
        self.email_entry.insert(0, user['email'])

        # Seleccionar el rol actual
        current_role_id = user.get('rol')
        current_role_name = ""
        for rid, role_data in self.user_roles.items():
            if str(rid) == str(current_role_id):
                current_role_name = role_data['name']
                break
                
        if current_role_name:
            self.role_combo.set(current_role_name)
        elif roles_list:
            self.role_combo.set(roles_list[0])

        # Botones de acción
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(0, 20), padx=20)

        def save_edited_user():
            # Validar campos
            name = self.name_entry.get().strip()
            username = self.username_entry.get().strip()
            email = self.email_entry.get().strip()
            password = self.password_entry.get().strip()
            confirm_password = self.confirm_password_entry.get().strip()
            role_name = self.role_combo.get().strip()

            if not name or not username or not email or not role_name:
                alert_manager.empty_fields(self)
                return

            # Validar formato de email
            if "@" not in email or "." not in email:
                alert_manager.validation_error(
                    "Por favor ingrese una dirección de email válida.\n\nEjemplo: usuario@empresa.com",
                    self
                )
                return

            # Si se ingresó una contraseña, validar que coincidan
            if password:
                if password != confirm_password:
                    alert_manager.validation_error(
                        "Las contraseñas no coinciden.\n\nPor favor, asegúrese de que ambas contraseñas sean iguales.",
                        self
                    )
                    return
                
                # Validar fortaleza de contraseña
                if len(password) < 6:
                    alert_manager.validation_error(
                        "La contraseña debe tener al menos 6 caracteres.\n\nPor seguridad, use una contraseña más larga.",
                        self
                    )
                    return

            # Obtener el ID del rol
            role_id = None
            for rid, role_data in self.user_roles.items():
                if role_data['name'] == role_name:
                    role_id = rid
                    break

            if role_id is None:
                alert_manager.show_error("Error de Rol", "Rol no válido.", self)
                return

            # Preparar datos para enviar al controlador
            user_data = {
                "nombre": name,
                "username": username,
                "email": email,
                "rol": role_id
            }

            # Si se ingresó una contraseña, agregarla
            if password:
                user_data["password"] = password

            # Confirmar actualización
            confirm_message = f"¿Está seguro de actualizar los datos del usuario?\n\n"
            confirm_message += f"• Nombre: {user['nombre']} → {name}\n"
            confirm_message += f"• Nombre de usuario: {user['username']} → {username}\n"
            confirm_message += f"• Email: {user['email']} → {email}\n"
            confirm_message += f"• Rol: {current_role_name} → {role_name}\n"
            if password:
                confirm_message += "• Contraseña: Será actualizada\n"

            if not alert_manager.confirm("Confirmar Actualización de Usuario", confirm_message, self):
                return

            # Usar el controlador para actualizar el usuario
            success, result = self.controller.update_user(user['id'], user_data)
            if success:
                Logger.success(f"Usuario ID {user['id']} actualizado", "USERS_VIEW")
                # Cerrar el diálogo
                dialog.destroy()
                # Recargar la lista de usuarios
                self.load_users()
                # Mostrar mensaje de éxito
                alert_manager.success_update(self)
            else:
                Logger.error(f"Error al actualizar usuario ID {user['id']}: {result}", "USERS_VIEW")
                alert_manager.show_error(
                    "Error al Actualizar", 
                    f"No se pudo actualizar el usuario.\n\nError: {result}",
                    self
                )

        # Botón Guardar Cambios
        save_btn = ctk.CTkButton(
            buttons_frame, text="💾 Guardar Cambios", width=150, height=40,
            fg_color="#00B4D8", text_color="#FFFFFF", hover_color="#0096B4",
            command=save_edited_user
        )
        save_btn.pack(side="left", padx=10)

        # Botón Cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame, text="Cancelar", width=150, height=40,
            fg_color="#E5E7EB", text_color="#1E293B", hover_color="#D1D5DB",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=10)

    def toggle_user_status(self, user):
        """Cambia el estado de un usuario (Activo/Inactivo)."""
        try:
            new_status = "Inactivo" if user["estado"] == "Activo" else "Activo"
            status_change = "desactivar" if new_status == "Inactivo" else "activar"
            
            confirm_message = f"¿Está seguro de {status_change} al usuario '{user['nombre']}'?\n\n"
            
            if new_status == "Inactivo":
                confirm_message += "⚠️ ADVERTENCIA: El usuario perderá acceso al sistema.\n"
                confirm_message += "No podrá iniciar sesión hasta que sea reactivado.\n\n"
            else:
                confirm_message += "El usuario recuperará acceso completo al sistema.\n\n"
                
            confirm_message += f"Usuario: {user['nombre']}\n"
            confirm_message += f"Estado actual: {user['estado']}\n"
            confirm_message += f"Nuevo estado: {new_status}"

            if not alert_manager.confirm("Confirmar Cambio de Estado", confirm_message, self):
                return
                
            success, message = self.controller.change_user_status(user['id'], new_status == "Activo")
            if success:
                Logger.success(f"Estado del usuario {user['id']} cambiado a {new_status}", "USERS_VIEW")
                # Refrescar la lista de usuarios
                self.load_users()
                # Mostrar mensaje de éxito
                alert_manager.show_success(
                    f"Usuario {status_change.title()}do", 
                    f"El usuario '{user['nombre']}' ha sido {status_change}do exitosamente.\n\n"
                    f"Nuevo estado: {new_status}",
                    self
                )
            else:
                Logger.error(f"Error al cambiar estado del usuario {user['id']}: {message}", "USERS_VIEW")
                alert_manager.show_error(
                    "Error al Cambiar Estado", 
                    f"No se pudo cambiar el estado del usuario.\n\nError: {message}",
                    self
                )
        except Exception as e:
            Logger.log_error_exception(e, "USERS_VIEW")
            alert_manager.show_error(
                "Error Inesperado", 
                f"Error inesperado al cambiar estado: {str(e)}",
                self
            )

    def delete_user(self, user):
        """Acción para eliminar un usuario."""
        try:
            # Validar que user tiene los datos necesarios
            if not user or 'id' not in user or 'nombre' not in user:
                alert_manager.show_error("Error", "Datos del usuario inválidos.", self)
                return
            
            # Confirmar eliminación con detalles
            confirm_message = f"¿Está seguro de eliminar permanentemente al usuario '{user['nombre']}'?\n\n"
            confirm_message += "⚠️ ADVERTENCIA: Esta acción es IRREVERSIBLE.\n\n"
            confirm_message += f"• Nombre: {user['nombre']}\n"
            confirm_message += f"• Usuario: {user['username']}\n"
            confirm_message += f"• Email: {user['email']}\n"
            confirm_message += f"• Rol: {user['rol']}\n\n"
            confirm_message += "Se eliminarán todos los datos asociados a este usuario."

            if not alert_manager.confirm_delete(f"el usuario '{user['nombre']}'", self):
                return
            
            Logger.info(f"Eliminando usuario ID: {user['id']}, nombre: {user['nombre']}", "USERS_VIEW")
            success, message = self.controller.delete_user(user['id'])
            
            if success:
                Logger.success(f"Usuario {user['id']} eliminado", "USERS_VIEW")
                # Refrescar lista de usuarios
                self.load_users()
                # Refrescar resumen de usuarios
                summary = self.controller.get_users_summary()
                self.update_summary_cards(summary)
                # Mostrar mensaje de éxito
                alert_manager.success_delete(self)
            else:
                Logger.error(f"Error al eliminar usuario {user['id']}: {message}", "USERS_VIEW")
                alert_manager.error_delete(self)
                
        except Exception as e:
            Logger.log_error_exception(e, "USERS_VIEW")
            alert_manager.show_error(
                "Error al Eliminar", 
                f"Error inesperado al eliminar usuario.\n\n{str(e)}",
                self
            )

    def get_notification_count(self):
        """Obtiene el número de notificaciones no leídas."""
        return alert_manager.get_unread_count()