# view/users_view.py

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class UsersView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox - Usuarios")
        self.root.geometry("1400x900")
        self.root.state('zoomed')
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Datos de ejemplo
        self.users = [
            ("👤", "admin", "Juan Pérez", "juan@notebox.com", "Admin", "Activo", "2025-11-05"),
            ("👤", "vendedor1", "María González", "maria@notebox.com", "Empleado", "Activo", "2025-11-05"),
            ("👤", "vendedor2", "Carlos Rodríguez", "carlos@notebox.com", "Empleado", "Activo", "2025-11-04"),
            ("👤", "almacen", "Ana Martínez", "ana@notebox.com", "Empleado", "Activo", "2025-11-03"),
            ("👤", "lhernandez", "Luis Hernández", "luis@notebox.com", "Empleado", "Inactivo", "2025-10-20"),
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
            ("📈", "Reportes", False),
            ("👥", "Usuarios", True),
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
        
        # === BARRA DE HERRAMIENTAS ===
        toolbar = ctk.CTkFrame(content, fg_color="white", corner_radius=12, height=90)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)
        
        toolbar_content = ctk.CTkFrame(toolbar, fg_color="white")
        toolbar_content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Buscador
        search_users = ctk.CTkEntry(
            toolbar_content,
            placeholder_text="🔍 Buscar usuarios...",
            width=400,
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=1,
            border_color="#e0e0e0"
        )
        search_users.pack(side="left", padx=(0, 20))
        
        # Botón Crear Usuario
        create_btn = ctk.CTkButton(
            toolbar_content,
            text="👤+ Crear Usuario",
            width=160,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=8
        )
        create_btn.pack(side="right")
        
        # === TARJETAS DE ESTADÍSTICAS (2 columnas) ===
        stats_row = ctk.CTkFrame(content, fg_color="transparent")
        stats_row.pack(fill="x", pady=(0, 20))
        
        # Administradores
        admin_card = ctk.CTkFrame(stats_row, fg_color="#00b4d8", corner_radius=12)
        admin_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        admin_content = ctk.CTkFrame(admin_card, fg_color="transparent")
        admin_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        admin_header = ctk.CTkFrame(admin_content, fg_color="transparent")
        admin_header.pack(fill="x")
        
        admin_text = ctk.CTkFrame(admin_header, fg_color="transparent")
        admin_text.pack(side="left")
        
        ctk.CTkLabel(
            admin_text,
            text="Administradores",
            font=("Arial", 14, "bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            admin_text,
            text="1 usuario",
            font=("Arial", 24, "bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        ctk.CTkLabel(
            admin_header,
            text="🛡️",
            font=("Segoe UI Emoji", 40),
            text_color="white"
        ).pack(side="right")
        
        ctk.CTkLabel(
            admin_content,
            text="Acceso total al sistema",
            font=("Arial", 12),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(10, 0))
        
        # Empleados
        emp_card = ctk.CTkFrame(stats_row, fg_color="white", corner_radius=12)
        emp_card.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        emp_content = ctk.CTkFrame(emp_card, fg_color="white")
        emp_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        emp_header = ctk.CTkFrame(emp_content, fg_color="white")
        emp_header.pack(fill="x")
        
        emp_text = ctk.CTkFrame(emp_header, fg_color="white")
        emp_text.pack(side="left")
        
        ctk.CTkLabel(
            emp_text,
            text="Empleados",
            font=("Arial", 14, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            emp_text,
            text="4 usuarios",
            font=("Arial", 24, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        ctk.CTkLabel(
            emp_header,
            text="👥",
            font=("Segoe UI Emoji", 40),
            text_color="#6c757d"
        ).pack(side="right")
        
        ctk.CTkLabel(
            emp_content,
            text="Acceso limitado según permisos",
            font=("Arial", 12),
            text_color="#6c757d",
            anchor="w"
        ).pack(anchor="w", pady=(10, 0))
        
        # === TABLA DE USUARIOS ===
        table_container = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        table_container.pack(fill="both", expand=True)
        
        table_content = ctk.CTkFrame(table_container, fg_color="white")
        table_content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Título
        ctk.CTkLabel(
            table_content,
            text="Lista de Usuarios",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(fill="x", pady=(0, 20))
        
        # Headers
        headers = ["Usuario", "Nombre", "Email", "Rol", "Estado", "Último Acceso", "Acciones"]
        widths = [120, 150, 200, 120, 100, 120, 120]
        
        header_row = ctk.CTkFrame(table_content, fg_color="#f8f9fa", height=50, corner_radius=8)
        header_row.pack(fill="x", pady=(0, 10))
        header_row.pack_propagate(False)
        
        for header, width in zip(headers, widths):
            ctk.CTkLabel(
                header_row,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#2b2d42",
                width=width,
                anchor="w"
            ).pack(side="left", padx=10)
        
        # Usuarios
        users_list = ctk.CTkScrollableFrame(table_content, fg_color="white", height=300)
        users_list.pack(fill="both", expand=True, pady=(0, 20))
        
        for user in self.users:
            self.create_user_row(users_list, user, widths)
        
        # === ROLES INFO ===
        roles_title = ctk.CTkLabel(
            content,
            text="Roles y Permisos",
            font=("Arial", 18, "bold"),
            text_color="#2b2d42",
            anchor="w"
        )
        roles_title.pack(fill="x", pady=(20, 15))
        
        # Rol Administrador
        admin_role_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        admin_role_card.pack(fill="x", pady=(0, 10))
        
        admin_role_content = ctk.CTkFrame(admin_role_card, fg_color="white")
        admin_role_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Header
        admin_role_header = ctk.CTkFrame(admin_role_content, fg_color="white")
        admin_role_header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            admin_role_header,
            text="🛡️",
            font=("Segoe UI Emoji", 24),
            fg_color="#e8f4f8",
            corner_radius=8,
            width=45,
            height=45
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            admin_role_header,
            text="Rol: Administrador",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Permisos
        permisos = [
            "• Acceso completo al sistema",
            "• Gestión de usuarios y permisos",
            "• Configuración del sistema",
            "• Exportar e importar datos"
        ]
        
        for permiso in permisos:
            ctk.CTkLabel(
                admin_role_content,
                text=permiso,
                font=("Arial", 12),
                text_color="#6c757d",
                anchor="w"
            ).pack(fill="x", pady=2)
        
        # Rol Empleado
        emp_role_card = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        emp_role_card.pack(fill="x", pady=(0, 20))
        
        emp_role_content = ctk.CTkFrame(emp_role_card, fg_color="white")
        emp_role_content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Header
        emp_role_header = ctk.CTkFrame(emp_role_content, fg_color="white")
        emp_role_header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            emp_role_header,
            text="👤",
            font=("Segoe UI Emoji", 24),
            fg_color="#f8f9fa",
            corner_radius=8,
            width=45,
            height=45
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            emp_role_header,
            text="Rol: Empleado",
            font=("Arial", 16, "bold"),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Permisos
        permisos_emp = [
            "• Gestión de inventario",
            "• Registro de entradas/salidas",
            "• Ver reportes básicos",
            "• Sin acceso a configuración"
        ]
        
        for permiso in permisos_emp:
            ctk.CTkLabel(
                emp_role_content,
                text=permiso,
                font=("Arial", 12),
                text_color="#6c757d",
                anchor="w"
            ).pack(fill="x", pady=2)
        
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
    
    def create_user_row(self, parent, user, widths):
        """Crear fila de usuario"""
        icon, username, name, email, role, status, last_access = user
        
        row = ctk.CTkFrame(parent, fg_color="white", height=65)
        row.pack(fill="x", pady=3)
        row.pack_propagate(False)
        
        # Usuario con icono
        user_frame = ctk.CTkFrame(row, fg_color="white", width=widths[0])
        user_frame.pack(side="left", padx=10)
        user_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            user_frame,
            text=icon,
            font=("Segoe UI Emoji", 18),
            fg_color="#e8f4f8",
            corner_radius=8,
            width=35,
            height=35
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            user_frame,
            text=username,
            font=("Arial", 12),
            text_color="#2b2d42",
            anchor="w"
        ).pack(side="left")
        
        # Nombre
        ctk.CTkLabel(
            row,
            text=name,
            font=("Arial", 12),
            text_color="#2b2d42",
            width=widths[1],
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Email
        ctk.CTkLabel(
            row,
            text=email,
            font=("Arial", 12),
            text_color="#6c757d",
            width=widths[2],
            anchor="w"
        ).pack(side="left", padx=10)
        
        # Rol (badge)
        rol_color = "#e8f4f8" if role == "Admin" else "#f8f9fa"
        rol_text_color = "#00b4d8" if role == "Admin" else "#6c757d"
        rol_icon = "🛡️" if role == "Admin" else "👤"
        
        rol_badge = ctk.CTkLabel(
            row,
            text=f"{rol_icon} {role}",
            font=("Arial", 11, "bold"),
            text_color=rol_text_color,
            fg_color=rol_color,
            corner_radius=6,
            width=widths[3],
            height=28
        )
        rol_badge.pack(side="left", padx=10)
        
        # Estado
        estado_color = "#d4edda" if status == "Activo" else "#f8d7da"
        estado_text_color = "#155724" if status == "Activo" else "#721c24"
        
        estado_badge = ctk.CTkLabel(
            row,
            text=status,
            font=("Arial", 11, "bold"),
            text_color=estado_text_color,
            fg_color=estado_color,
            corner_radius=6,
            width=widths[4],
            height=28
        )
        estado_badge.pack(side="left", padx=10)
        
        # Último acceso
        ctk.CTkLabel(
            row,
            text=last_access,
            font=("Arial", 12),
            text_color="#6c757d",
            width=widths[5],
            anchor="center"
        ).pack(side="left", padx=10)
        
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
        
        # Permisos
        ctk.CTkButton(
            actions_frame,
            text="🔑",
            width=35,
            height=35,
            font=("Segoe UI Emoji", 14),
            fg_color="#fff4e6",
            hover_color="#ffe8cc",
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
    app = UsersView(root)
    root.mainloop()