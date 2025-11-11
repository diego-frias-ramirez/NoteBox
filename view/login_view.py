"""
NoteBox - Sistema de Gestión de Inventario
Login View con CustomTkinter
Papelería Valeria
"""

import customtkinter as ctk
from PIL import Image
import os

# Configuración de tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de ventana
        self.title("NoteBox - Login")
        self.geometry("500x700")
        self.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Frame principal con padding
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo (placeholder - caja azul con ícono)
        self.logo_frame = ctk.CTkFrame(
            self.main_frame, 
            width=100, 
            height=100, 
            corner_radius=20,
            fg_color="#1E90FF"
        )
        self.logo_frame.pack(pady=(40, 10))
        
        # Texto del logo (emoji de caja)
        self.logo_label = ctk.CTkLabel(
            self.logo_frame,
            text="📦",
            font=("Arial", 50),
            text_color="white"
        )
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="NoteBox",
            font=("Arial", 28, "bold"),
            text_color="#2C3E50"
        )
        self.title_label.pack(pady=(10, 5))
        
        # Subtítulo
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Sistema de Gestión de Inventario",
            font=("Arial", 14),
            text_color="#7F8C8D"
        )
        self.subtitle_label.pack(pady=(0, 40))
        
        # Label Usuario
        self.user_label = ctk.CTkLabel(
            self.main_frame,
            text="Usuario",
            font=("Arial", 13),
            text_color="#2C3E50",
            anchor="w"
        )
        self.user_label.pack(anchor="w", padx=40, pady=(0, 5))
        
        # Entry Usuario
        self.user_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="👤 Ingrese su usuario",
            width=380,
            height=50,
            font=("Arial", 13),
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0"
        )
        self.user_entry.pack(padx=40, pady=(0, 20))
        
        # Label Contraseña
        self.pass_label = ctk.CTkLabel(
            self.main_frame,
            text="Contraseña",
            font=("Arial", 13),
            text_color="#2C3E50",
            anchor="w"
        )
        self.pass_label.pack(anchor="w", padx=40, pady=(0, 5))
        
        # Entry Contraseña
        self.pass_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="🔒 Ingrese su contraseña",
            width=380,
            height=50,
            font=("Arial", 13),
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0",
            show="●"
        )
        self.pass_entry.pack(padx=40, pady=(0, 10))
        
        # Checkbox Recordar usuario
        self.remember_check = ctk.CTkCheckBox(
            self.main_frame,
            text="Recordar usuario",
            font=("Arial", 12),
            text_color="#7F8C8D",
            fg_color="#1E90FF",
            hover_color="#1873CC"
        )
        self.remember_check.pack(anchor="w", padx=40, pady=(0, 30))
        
        # Botón INGRESAR
        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="INGRESAR",
            width=380,
            height=50,
            font=("Arial", 14, "bold"),
            corner_radius=10,
            fg_color="#1E90FF",
            hover_color="#1873CC",
            command=self.login
        )
        self.login_button.pack(padx=40, pady=(0, 20))
        
        # Link recuperar contraseña
        self.forgot_button = ctk.CTkButton(
            self.main_frame,
            text="¿Olvidó su contraseña?",
            font=("Arial", 12, "underline"),
            text_color="#1E90FF",
            fg_color="transparent",
            hover_color="#F0F0F0",
            command=self.forgot_password
        )
        self.forgot_button.pack(pady=(0, 40))
        
        # Versión
        self.version_label = ctk.CTkLabel(
            self.main_frame,
            text="NoteBox v1.0 - 2025",
            font=("Arial", 11),
            text_color="#BDC3C7"
        )
        self.version_label.pack(side="bottom", pady=20)
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self.login())
        
    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        """Acción de login"""
        usuario = self.user_entry.get()
        password = self.pass_entry.get()
        
        if not usuario or not password:
            self.show_error("Por favor complete todos los campos")
            return
        
        # Aquí iría la lógica de autenticación
        print(f"Login attempt - User: {usuario}")
        self.show_success("Login exitoso")
    
    def forgot_password(self):
        """Acción recuperar contraseña"""
        print("Recuperar contraseña")
        self.show_info("Funcionalidad en desarrollo")
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        dialog = ctk.CTkInputDialog(
            text=message,
            title="Error"
        )
    
    def show_success(self, message):
        """Mostrar mensaje de éxito"""
        print(f"✓ {message}")
    
    def show_info(self, message):
        """Mostrar mensaje informativo"""
        print(f"ℹ {message}")


if __name__ == "__main__":
    app = LoginView()
    app.mainloop()