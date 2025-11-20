"""
NoteBox - Vista de Login
UI Moderna estilo Figma
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import os
from controller.login_controller import LoginController
from utils.logger import Logger

# Configuración de tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginView:
    """Vista de inicio de sesión moderna"""
    
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.controller = LoginController()
        
        # Configurar ventana
        self.setup_window()
        
        # Crear interfaz
        self.create_widgets()
        
        Logger.info("Vista de login inicializada", "LOGIN_VIEW")
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("NoteBox")
        
        # Tamaño y posición
        window_width = 520
        window_height = 900
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        
        # Color de fondo
        self.root.configure(fg_color="#FFFFFF")
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal centrado
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color="#FFFFFF",
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=60, pady=60)
        
        # Logo
        self.create_logo(main_frame)
        
        # Título
        self.create_title(main_frame)
        
        # Formulario
        self.create_form(main_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_logo(self, parent):
        """Crea el logo con ícono de caja 3D"""
        logo_container = ctk.CTkFrame(parent, fg_color="transparent")
        logo_container.pack(pady=(0, 20))
        
        # Frame con gradiente azul para el logo
        logo_frame = ctk.CTkFrame(
            logo_container,
            width=90,
            height=90,
            corner_radius=20,
            fg_color="#00A8E8"
        )
        logo_frame.pack()
        logo_frame.pack_propagate(False)
        
        # Ícono de caja (simulado con texto)
        icon_label = ctk.CTkLabel(
            logo_frame,
            text="📦",
            font=ctk.CTkFont(size=45),
            text_color="#FFFFFF"
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def create_title(self, parent):
        """Crea el título y subtítulo"""
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(pady=(0, 40))
        
        # Título principal
        title = ctk.CTkLabel(
            title_frame,
            text="NoteBox",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#1A1A1A"
        )
        title.pack()
        
        # Subtítulo
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Sistema de Gestión de Inventario",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#6B7280"
        )
        subtitle.pack(pady=(5, 0))
    
    def create_form(self, parent):
        """Crea el formulario de login"""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 30))
        
        # Campo Usuario
        user_label = ctk.CTkLabel(
            form_frame,
            text="Usuario",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#374151",
            anchor="w"
        )
        user_label.pack(fill="x", pady=(0, 8))
        
        # Frame para entry con ícono
        user_entry_frame = ctk.CTkFrame(
            form_frame,
            fg_color="#F9FAFB",
            corner_radius=10,
            border_width=1,
            border_color="#E5E7EB"
        )
        user_entry_frame.pack(fill="x", pady=(0, 20))
        
        # Ícono de usuario
        user_icon = ctk.CTkLabel(
            user_entry_frame,
            text="👤",
            font=ctk.CTkFont(size=16),
            text_color="#9CA3AF",
            width=35
        )
        user_icon.pack(side="left", padx=(12, 0))
        
        # Entry de usuario
        self.username_entry = ctk.CTkEntry(
            user_entry_frame,
            placeholder_text="Ingrese su usuario",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="transparent",
            border_width=0,
            text_color="#1F2937",
            height=48
        )
        self.username_entry.pack(side="left", fill="x", expand=True, padx=(5, 15))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.username_entry.bind("<FocusIn>", lambda e: self.on_entry_focus(user_entry_frame, True))
        self.username_entry.bind("<FocusOut>", lambda e: self.on_entry_focus(user_entry_frame, False))
        
        # Campo Contraseña
        pass_label = ctk.CTkLabel(
            form_frame,
            text="Contraseña",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#374151",
            anchor="w"
        )
        pass_label.pack(fill="x", pady=(0, 8))
        
        # Frame para password con ícono
        pass_entry_frame = ctk.CTkFrame(
            form_frame,
            fg_color="#F9FAFB",
            corner_radius=10,
            border_width=1,
            border_color="#E5E7EB"
        )
        pass_entry_frame.pack(fill="x", pady=(0, 15))
        
        # Ícono de candado
        pass_icon = ctk.CTkLabel(
            pass_entry_frame,
            text="🔒",
            font=ctk.CTkFont(size=16),
            text_color="#9CA3AF",
            width=35
        )
        pass_icon.pack(side="left", padx=(12, 0))
        
        # Entry de contraseña
        self.password_entry = ctk.CTkEntry(
            pass_entry_frame,
            placeholder_text="Ingrese su contraseña",
            show="●",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="transparent",
            border_width=0,
            text_color="#1F2937",
            height=48
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(5, 15))
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<FocusIn>", lambda e: self.on_entry_focus(pass_entry_frame, True))
        self.password_entry.bind("<FocusOut>", lambda e: self.on_entry_focus(pass_entry_frame, False))
        
        # Checkbox recordar usuario
        remember_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        remember_frame.pack(fill="x", pady=(0, 25))
        
        self.remember_var = ctk.BooleanVar()
        remember_check = ctk.CTkCheckBox(
            remember_frame,
            text="Recordar usuario",
            variable=self.remember_var,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#6B7280",
            fg_color="#00A8E8",
            hover_color="#0095D1",
            corner_radius=4,
            border_width=2,
            border_color="#D1D5DB"
        )
        remember_check.pack(side="left")
        
        # Botón INGRESAR
        login_button = ctk.CTkButton(
            form_frame,
            text="INGRESAR",
            height=52,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#00A8E8",
            hover_color="#0095D1",
            corner_radius=10,
            command=self.handle_login,
            cursor="hand2"
        )
        login_button.pack(fill="x", pady=(0, 15))
        
        # Link "¿Olvidó su contraseña?"
        forgot_link = ctk.CTkLabel(
            form_frame,
            text="¿Olvidó su contraseña?",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#00A8E8",
            cursor="hand2"
        )
        forgot_link.pack()
        forgot_link.bind("<Button-1>", lambda e: self.forgot_password())
        
        # Efecto hover en el link
        forgot_link.bind("<Enter>", lambda e: forgot_link.configure(text_color="#0095D1"))
        forgot_link.bind("<Leave>", lambda e: forgot_link.configure(text_color="#00A8E8"))
    
    def create_footer(self, parent):
        """Crea el pie de página"""
        footer_frame = ctk.CTkFrame(parent, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", pady=(30, 0))
        
        # Separador
        separator = ctk.CTkFrame(
            footer_frame,
            height=1,
            fg_color="#E5E7EB"
        )
        separator.pack(fill="x", pady=(0, 20))
        
        # Botón de test de conexión
        test_button = ctk.CTkButton(
            footer_frame,
            text="🔌 Probar Conexión BD",
            height=42,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="transparent",
            hover_color="#F3F4F6",
            text_color="#6B7280",
            border_width=1,
            border_color="#E5E7EB",
            corner_radius=8,
            command=self.test_connection,
            cursor="hand2"
        )
        test_button.pack(fill="x", pady=(0, 20))
        
        # Info de credenciales de prueba
        cred_label = ctk.CTkLabel(
            footer_frame,
            text="💡 Usuario: admin | Contraseña: admin123",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#9CA3AF"
        )
        cred_label.pack(pady=(0, 15))
        
        # Copyright
        copyright_label = ctk.CTkLabel(
            footer_frame,
            text="NoteBox v1.0 - 2025",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#D1D5DB"
        )
        copyright_label.pack()
    
    def on_entry_focus(self, frame, focused):
        """Maneja el efecto de foco en los campos"""
        if focused:
            frame.configure(border_color="#00A8E8", border_width=2)
        else:
            frame.configure(border_color="#E5E7EB", border_width=1)
    
    def handle_login(self):
        """Maneja el evento de inicio de sesión"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validar campos vacíos
        if not username or not password:
            self.show_error("Por favor ingrese usuario y contraseña")
            return
        
        Logger.info(f"Intentando login con usuario: {username}", "LOGIN_VIEW")
        
        # Validar credenciales
        success, message, user_data = self.controller.validate_credentials(username, password)
        
        if success:
            Logger.success(f"Login exitoso: {username}", "LOGIN_VIEW")
            self.show_success("¡Bienvenido!")
            self.root.after(800, lambda: self.complete_login(user_data))
        else:
            Logger.warning(f"Login fallido: {message}", "LOGIN_VIEW")
            self.show_error(message)
            self.password_entry.delete(0, "end")
            self.password_entry.focus()
    
    def complete_login(self, user_data):
        """Completa el proceso de login"""
        self.root.destroy()
        if self.on_login_success:
            self.on_login_success(user_data)
    
    def forgot_password(self):
        """Maneja el clic en olvidó contraseña"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Recuperar Contraseña")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        
        # Centrar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 200) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Contenido
        info_label = ctk.CTkLabel(
            dialog,
            text="📧",
            font=ctk.CTkFont(size=40)
        )
        info_label.pack(pady=(30, 10))
        
        message = ctk.CTkLabel(
            dialog,
            text="Contacte al administrador del sistema\npara recuperar su contraseña",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#6B7280",
            justify="center"
        )
        message.pack(pady=(0, 20))
        
        ok_button = ctk.CTkButton(
            dialog,
            text="Entendido",
            width=120,
            height=40,
            fg_color="#00A8E8",
            hover_color="#0095D1",
            command=dialog.destroy
        )
        ok_button.pack()
        
        dialog.transient(self.root)
        dialog.grab_set()
    
    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        Logger.info("Probando conexión a base de datos...", "LOGIN_VIEW")
        
        success = self.controller.test_database_connection()
        
        if success:
            self.show_dialog(
                "✓",
                "#10B981",
                "Conexión Exitosa",
                "La conexión a la base de datos\nfue exitosa\n\nBase de datos: notebox_db"
            )
        else:
            self.show_dialog(
                "✗",
                "#EF4444",
                "Error de Conexión",
                "No se pudo conectar a la BD\n\nVerifique que MySQL esté ejecutándose"
            )
    
    def show_error(self, message):
        """Muestra un mensaje de error"""
        if hasattr(self, 'notification_label'):
            self.notification_label.destroy()
        
        self.notification_label = ctk.CTkFrame(
            self.root,
            fg_color="#FEE2E2",
            corner_radius=8,
            border_width=1,
            border_color="#FCA5A5"
        )
        self.notification_label.place(relx=0.5, rely=0.92, anchor="center")
        
        text = ctk.CTkLabel(
            self.notification_label,
            text=f"⚠  {message}",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#991B1B"
        )
        text.pack(padx=20, pady=10)
        
        self.root.after(3500, lambda: self.notification_label.destroy() if hasattr(self, 'notification_label') else None)
    
    def show_success(self, message):
        """Muestra un mensaje de éxito"""
        if hasattr(self, 'notification_label'):
            self.notification_label.destroy()
        
        self.notification_label = ctk.CTkFrame(
            self.root,
            fg_color="#D1FAE5",
            corner_radius=8,
            border_width=1,
            border_color="#6EE7B7"
        )
        self.notification_label.place(relx=0.5, rely=0.92, anchor="center")
        
        text = ctk.CTkLabel(
            self.notification_label,
            text=f"✓  {message}",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#065F46"
        )
        text.pack(padx=20, pady=10)
    
    def show_dialog(self, icon, color, title, message):
        """Muestra un diálogo modal"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("380x240")
        dialog.resizable(False, False)
        
        # Centrar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 380) // 2
        y = (dialog.winfo_screenheight() - 240) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Contenido
        icon_label = ctk.CTkLabel(
            dialog,
            text=icon,
            font=ctk.CTkFont(size=50),
            text_color=color
        )
        icon_label.pack(pady=(25, 10))
        
        title_label = ctk.CTkLabel(
            dialog,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#1F2937"
        )
        title_label.pack(pady=(0, 10))
        
        message_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#6B7280",
            justify="center"
        )
        message_label.pack(pady=(0, 20))
        
        ok_button = ctk.CTkButton(
            dialog,
            text="Aceptar",
            width=120,
            height=38,
            fg_color=color,
            hover_color=color,
            command=dialog.destroy
        )
        ok_button.pack()
        
        dialog.transient(self.root)
        dialog.grab_set()
    
    def run(self):
        """Inicia el loop principal"""
        self.root.mainloop()


# Para probar independientemente
if __name__ == "__main__":
    def on_success(user_data):
        print(f"Login exitoso: {user_data}")
    
    root = ctk.CTk()
    app = LoginView(root, on_success)
    app.run()