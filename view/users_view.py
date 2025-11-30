"""
NoteBox - Vista del Módulo de Usuarios (Corregida y Alineada con Figma)
Ubicación: view/users_view.py
"""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import os

from components.base_view import BaseView
from controller.users_controller import UsersController
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

        ctk.CTkLabel(search_frame, text="🔍", font=ctk.CTkFont(size=16), text_color="#94A3B8").pack(side="left", padx=(18, 10))
        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Buscar usuarios...",
            fg_color="transparent", border_width=0, font=ctk.CTkFont(size=14), height=44
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.on_search_change) # <-- Vincular evento de búsqueda

        # Botón Crear Usuario
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
        self.load_users() # <-- Llamar a load_users para refrescar

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
        shield_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "filtro.png") # Reemplaza por el ícono correcto si tienes uno
        try:
            img = Image.open(shield_icon_path)
            img = img.resize((24, 24), Image.LANCZOS)
            shield_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
            ctk.CTkLabel(admin_inner, image=shield_icon, text="").place(relx=0.95, rely=0.5, anchor="center")
        except:
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
        user_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "user_avatar.png")
        try:
            img = Image.open(user_icon_path)
            img = img.resize((24, 24), Image.LANCZOS)
            user_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
            ctk.CTkLabel(employee_inner, image=user_icon, text="").place(relx=0.95, rely=0.5, anchor="center")
        except:
            ctk.CTkLabel(employee_inner, text="👤", font=ctk.CTkFont(size=16), text_color="#2b2d42").place(relx=0.95, rely=0.5, anchor="center")

    def create_table(self, parent):
        """Crea la tabla de usuarios."""
        table_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        self.table_frame = table_frame # <-- Guardar referencia para update_table

        # Encabezado de la tabla
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=(15, 0))
        header_frame.pack_propagate(False)

        columns = [
            ("Usuario", 120),
            ("Nombre", 180),
            ("Email", 200),
            ("Rol", 120),
            ("Estado", 100),
            ("Último Acceso", 150),
            ("Acciones", 100)
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

        # Footer con paginación (inicializar etiqueta de paginación)
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
            no_users_label.pack(expand=True)
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

        # Usuario (120px)
        user_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=100)
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

        # Rol
        role_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=120)
        role_frame.pack(side="left", padx=8)
        role_frame.pack_propagate(False)

        role_name = user["rol"].lower() if user["rol"] else "empleado"
        role_colors = {
            "admin": ("#00B4D8", "#FFFFFF"),
            "empleado": ("#E5E7EB", "#1E293B")
        }
        bg_color, text_color = role_colors.get(role_name, ("#E5E7EB", "#1E293B"))

        role_badge = ctk.CTkFrame(role_frame, fg_color=bg_color, corner_radius=8, height=26)
        role_badge.pack(side="left")
        ctk.CTkLabel(
            role_badge, text=role_name.upper(),
            font=ctk.CTkFont(size=10, weight="bold"), text_color=text_color
        ).pack(padx=8, pady=4)

        # Rol (120px)
        role_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=110)
        role_frame.pack(side="left", padx=8)
        role_frame.pack_propagate(False)
        
        role_name = user["rol"].lower() if user["rol"] else "empleado"
        role_colors = {
            "admin": ("#00B4D8", "#FFFFFF"),
            "empleado": ("#64748B", "#FFFFFF")
        }
        bg_color, text_color = role_colors.get(role_name, ("#64748B", "#FFFFFF"))
        
        role_badge = ctk.CTkFrame(role_frame, fg_color=bg_color, corner_radius=6, height=24)
        role_badge.pack(side="left", expand=False)
        ctk.CTkLabel(role_badge, text=role_name.upper(), font=ctk.CTkFont(size=9, weight="bold"), text_color=text_color).pack(padx=10, pady=3)

        # Estado
        status_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=100)
        status_frame.pack(side="left", padx=8)
        status_frame.pack_propagate(False)

        status = user["estado"]
        badge_colors = {
            "Activo": ("#DCFCE7", "#16A34A"),
            "Inactivo": ("#FEE2E2", "#DC2626")
        }
        bg_color, text_color = badge_colors.get(status, badge_colors["Activo"])

        badge = ctk.CTkFrame(status_frame, fg_color=bg_color, corner_radius=12, height=26)
        badge.pack(side="left")
        ctk.CTkLabel(
            badge, text=status,
            font=ctk.CTkFont(size=10, weight="bold"), text_color=text_color
        ).pack(padx=12, pady=4)

        # Estado (100px)
        status_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=100)
        status_frame.pack(side="left", padx=8)
        status_frame.pack_propagate(False)
        
        status = user["estado"]
        badge_colors = {
            "Activo": ("#DCFCE7", "#16A34A"),
            "Inactivo": ("#FEE2E2", "#DC2626")
        }
        bg_color, text_color = badge_colors.get(status, badge_colors["Activo"])
        
        badge = ctk.CTkFrame(status_frame, fg_color=bg_color, corner_radius=6, height=24)
        badge.pack(side="left")
        ctk.CTkLabel(badge, text=status, font=ctk.CTkFont(size=9, weight="bold"), text_color=text_color).pack(padx=10, pady=3)

        # Último Acceso (150px)
        ultimo_acceso_text = user["ultimo_acceso"].strftime("%Y-%m-%d") if user["ultimo_acceso"] else "Nunca"
        ultimo_acceso_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=150)
        ultimo_acceso_frame.pack(side="left", padx=8)
        ultimo_acceso_frame.pack_propagate(False)
        ctk.CTkLabel(ultimo_acceso_frame, text=ultimo_acceso_text, font=ctk.CTkFont(size=11), text_color="#64748B", anchor="w").pack(side="left", fill="both", expand=True)

        # Acciones (Editar, Cambiar Estado, Eliminar)
        actions_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", width=100) # <-- Ancho aumentado a 100
        actions_frame.pack(side="left", padx=8)
        actions_frame.pack_propagate(False)

        # Botón Editar
        edit_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "edit.png")
        try:
            img = Image.open(edit_icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            edit_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            edit_btn = ctk.CTkButton(
                actions_frame, image=edit_icon, text="", width=28, height=28,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda u=user: self.edit_user(u)
            )
        except:
            edit_btn = ctk.CTkButton(
                actions_frame, text="✏️", width=28, height=28,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda u=user: self.edit_user(u)
            )
        edit_btn.pack(side="left", padx=2)

        # Botón Cambiar Estado
        status_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "low_stock.png") # Reemplaza por un ícono de "toggle" o "status"
        try:
            img = Image.open(status_icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            status_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            status_btn = ctk.CTkButton(
                actions_frame, image=status_icon, text="", width=28, height=28,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda u=user: self.toggle_user_status(u)
            )
        except:
            status_btn = ctk.CTkButton(
                actions_frame, text="🔄", width=28, height=28,
                fg_color="transparent", hover_color="#E0F7FA",
                corner_radius=6,
                command=lambda u=user: self.toggle_user_status(u)
            )
        status_btn.pack(side="left", padx=2)

        # Botón Eliminar
        delete_icon_path = os.path.join(self.base_path, "..", "assets", "icons", "delete.png")
        try:
            img = Image.open(delete_icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            delete_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            delete_btn = ctk.CTkButton(
                actions_frame, image=delete_icon, text="", width=28, height=28,
                fg_color="transparent", hover_color="#FEE2E2",
                corner_radius=6,
                command=lambda u=user: self.delete_user(u)
            )
        except:
            delete_btn = ctk.CTkButton(
                actions_frame, text="🗑️", width=28, height=28,
                fg_color="transparent", hover_color="#FEE2E2",
                corner_radius=6,
                command=lambda u=user: self.delete_user(u)
            )
        delete_btn.pack(side="left", padx=2)

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
            # Opcional: Mostrar un mensaje de error al usuario
            # self.show_message("Error al cargar datos iniciales", "error")

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
            # Opcional: Mostrar un mensaje de error al usuario
            # self.show_message("Error al cargar usuarios", "error")

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
        self.pagination_label.configure(text=f"Mostrando {start_index}-{end_index} de {self.total_users} usuarios")

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

        # Centrar popup
        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (100 // 2)
        popup.geometry(f"300x100+{x}+{y}")

        # Frame para contenido
        content_frame = ctk.CTkFrame(popup, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Icono según tipo de mensaje
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
            # Fallback a emoji si no se puede cargar el ícono
            fallback_emoji = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
            ctk.CTkLabel(content_frame, text=fallback_emoji.get(msg_type, "ℹ️"), font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))

        # Texto del mensaje
        label = ctk.CTkLabel(
            content_frame, text=message,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color
        )
        label.pack(side="left", expand=True)

        popup.after(3000, popup.destroy)

    def open_create_user_dialog(self):
        """Abre un diálogo para crear un nuevo usuario."""
        from tkinter import messagebox
        # En lugar de un mensaje simple, abrir un diálogo para añadir producto
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

        # Scrollable Frame para el formulario
        form_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Campos del formulario
        fields = [
            ("Nombre Completo:", "name_entry", "Ingrese el nombre completo"),
            ("Nombre de Usuario:", "username_entry", "Ingrese el nombre de usuario"),
            ("Email:", "email_entry", "Ingrese el correo electrónico"),
            ("Contraseña:", "password_entry", "Ingrese la contraseña"),
            ("Confirmar Contraseña:", "confirm_password_entry", "Confirme la contraseña")
        ]

        for label_text, var_name, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(
                field_frame, text=label_text, font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=(5, 0))

            if var_name in ["password_entry", "confirm_password_entry"]:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder, show="*")
            else:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder)
            widget.pack(fill="x", pady=(5, 10))

            setattr(self, var_name, widget)  # Guardar referencia

        # Rol
        ctk.CTkLabel(
            form_frame, text="Rol:", font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(10, 0))

        self.role_combo = ctk.CTkComboBox(form_frame, values=["Seleccione un rol"])
        self.role_combo.pack(fill="x", pady=(5, 10))

        # Cargar roles en el combo box
        roles_list = [role['name'] for role in self.user_roles.values()]
        self.role_combo.configure(values=roles_list)

        # Botones de acción
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))

        def save_user():
            # Validar campos
            name = self.name_entry.get().strip()
            username = self.username_entry.get().strip()
            email = self.email_entry.get().strip()
            password = self.password_entry.get().strip()
            confirm_password = self.confirm_password_entry.get().strip()
            role_name = self.role_combo.get().strip()

            # Validación básica
            if not name or not username or not email or not password or not role_name:
                self.show_message("Por favor, complete todos los campos.", "error")
                return

            if password != confirm_password:
                self.show_message("Las contraseñas no coinciden.", "error")
                return

            # Obtener el ID del rol
            role_id = None
            for rid, role_data in self.user_roles.items():
                if role_data['name'] == role_name:
                    role_id = rid
                    break

            if role_id is None:
                self.show_message("Rol no válido.", "error")
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
                Logger.success(f"Usuario '{name}' creado con ID {result['id']}", "USERS_VIEW")
                # Cerrar el diálogo
                dialog.destroy()
                # Recargar la lista de usuarios
                self.load_users()
                # Mostrar mensaje de éxito
                self.show_message(f"Usuario '{name}' creado correctamente.", "success")
            else:
                Logger.error(f"Error al crear usuario '{name}': {result}", "USERS_VIEW")
                self.show_message(f"Error al crear: {result}", "error")

        save_btn = ctk.CTkButton(
            buttons_frame, text="Guardar Usuario", width=150, height=30,
            fg_color="#00B4D8", text_color="#FFFFFF", hover_color="#0096B4",
            command=save_user
        )
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(
            buttons_frame, text="Cancelar", width=150, height=30,
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

        # Scrollable Frame para el formulario
        form_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Campos del formulario
        fields = [
            ("Nombre Completo:", "name_entry", "Ingrese el nombre completo"),
            ("Nombre de Usuario:", "username_entry", "Ingrese el nombre de usuario"),
            ("Email:", "email_entry", "Ingrese el correo electrónico"),
            ("Contraseña (opcional):", "password_entry", "Ingrese una nueva contraseña (deje vacío para mantener la actual)"),
            ("Confirmar Contraseña:", "confirm_password_entry", "Confirme la nueva contraseña")
        ]

        for label_text, var_name, placeholder in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(
                field_frame, text=label_text, font=ctk.CTkFont(size=12)
            ).pack(anchor="w", pady=(5, 0))

            if var_name in ["password_entry", "confirm_password_entry"]:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder, show="*")
            else:
                widget = ctk.CTkEntry(field_frame, placeholder_text=placeholder)
            widget.pack(fill="x", pady=(5, 10))

            setattr(self, var_name, widget)  # Guardar referencia

        # Rol
        ctk.CTkLabel(
            form_frame, text="Rol:", font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(10, 0))

        self.role_combo = ctk.CTkComboBox(form_frame, values=["Seleccione un rol"])
        self.role_combo.pack(fill="x", pady=(5, 10))

        # Cargar roles en el combo box
        roles_list = [role['name'] for role in self.user_roles.values()]
        self.role_combo.configure(values=roles_list)

        # Rellenar campos con los datos actuales del usuario
        self.name_entry.insert(0, user['nombre'])
        self.username_entry.insert(0, user['username'])
        self.email_entry.insert(0, user['email'])
        # No rellenar la contraseña por seguridad
        # self.password_entry.insert(0, "") # Dejar vacío
        # self.confirm_password_entry.insert(0, "") # Dejar vacío

        # Seleccionar el rol actual
        current_role_name = self.user_roles.get(user.get('rol'), {}).get('name', 'Sin Rol')
        self.role_combo.set(current_role_name)

        # Botones de acción
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))

        def save_edited_user():
            # Validar campos
            name = self.name_entry.get().strip()
            username = self.username_entry.get().strip()
            email = self.email_entry.get().strip()
            password = self.password_entry.get().strip()
            confirm_password = self.confirm_password_entry.get().strip()
            role_name = self.role_combo.get().strip()

            if not name or not username or not email or not role_name:
                self.show_message("Por favor, complete todos los campos.", "error")
                return

            # Si se ingresó una contraseña, validar que coincidan
            if password and password != confirm_password:
                self.show_message("Las contraseñas no coinciden.", "error")
                return

            # Obtener el ID del rol
            role_id = None
            for rid, role_data in self.user_roles.items():
                if role_data['name'] == role_name:
                    role_id = rid
                    break

            if role_id is None:
                self.show_message("Rol no válido.", "error")
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

            # Usar el controlador para actualizar el usuario
            success, result = self.controller.update_user(user['id'], user_data)
            if success:
                Logger.success(f"Usuario ID {user['id']} actualizado", "USERS_VIEW")
                # Cerrar el diálogo
                dialog.destroy()
                # Recargar la lista de usuarios
                self.load_users()
                # Mostrar mensaje de éxito
                self.show_message(f"Usuario '{name}' actualizado correctamente.", "success")
            else:
                Logger.error(f"Error al actualizar usuario ID {user['id']}: {result}", "USERS_VIEW")
                self.show_message(f"Error al actualizar: {result}", "error")

        # Botón Guardar Cambios
        save_btn = ctk.CTkButton(
            buttons_frame, text="Guardar Cambios", width=150, height=30,
            fg_color="#00B4D8", text_color="#FFFFFF", hover_color="#0096B4",
            command=save_edited_user
        )
        save_btn.pack(side="left", padx=10)

        # Botón Cancelar
        cancel_btn = ctk.CTkButton(
            buttons_frame, text="Cancelar", width=150, height=30,
            fg_color="#E5E7EB", text_color="#1E293B", hover_color="#D1D5DB",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=10)

    def toggle_user_status(self, user):
        """Cambia el estado de un usuario (Activo/Inactivo)."""
        new_status = "Inactivo" if user["estado"] == "Activo" else "Activo"
        confirmed = messagebox.askyesno(
            "Confirmar Cambio de Estado",
            f"¿Está seguro de cambiar el estado del usuario '{user['nombre']}' a {new_status}?\n\nEsta acción puede afectar su acceso al sistema."
        )
        if confirmed:
            success, message = self.controller.change_user_status(user['id'], new_status == "Activo")
            if success:
                Logger.success(f"Estado del usuario {user['id']} cambiado a {new_status}", "USERS_VIEW")
                # Refrescar la lista de usuarios
                self.load_users()
                # Mostrar mensaje de éxito
                self.show_message(f"Estado del usuario '{user['nombre']}' actualizado a {new_status}.", "success")
            else:
                Logger.error(f"Error al cambiar estado del usuario {user['id']}: {message}", "USERS_VIEW")
                self.show_message(f"Error al cambiar estado: {message}", "error")

    def delete_user(self, user):
        """Acción para eliminar un usuario."""
        from tkinter import messagebox
        confirmed = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el usuario '{user['nombre']}'?\n\nEsta acción no se puede deshacer."
        )
        if confirmed:
            success, message = self.controller.delete_user(user['id'])
            if success:
                Logger.success(f"Usuario {user['id']} eliminado", "USERS_VIEW")
                # Refrescar la lista de usuarios
                self.load_users()
                # Mostrar mensaje de éxito
                self.show_message("Usuario eliminado correctamente", "success")
            else:
                Logger.error(f"Error al eliminar usuario {user['id']}: {message}", "USERS_VIEW")
                self.show_message(f"Error al eliminar: {message}", "error")

