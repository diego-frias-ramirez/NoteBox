# view/login_view.py

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteBox")
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Tamaño de la ventana
        window_width = 480
        window_height = 720
        
        # Calcular posición central
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        
        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_var = tk.BooleanVar()
        
        # Mostrar loading primero
        self.show_loading()
    
    def show_loading(self):
        """Pantalla de carga inicial"""
        # Frame principal
        self.loading_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.loading_frame.pack(fill="both", expand=True)
        
        # Contenedor central
        center_frame = ctk.CTkFrame(self.loading_frame, fg_color="white")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo - Caja 3D
        logo_container = ctk.CTkFrame(
            center_frame,
            fg_color="#00b4d8",
            corner_radius=20,
            width=100,
            height=100
        )
        logo_container.pack(pady=(0, 20))
        logo_container.pack_propagate(False)
        
        logo_label = ctk.CTkLabel(
            logo_container,
            text="📦",
            font=("Segoe UI Emoji", 50),
            text_color="white"
        )
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        title_label = ctk.CTkLabel(
            center_frame,
            text="NoteBox",
            font=("Arial", 48, "bold"),
            text_color="#2b2d42"
        )
        title_label.pack(pady=(0, 10))
        
        # Barra de progreso
        self.progress = ctk.CTkProgressBar(
            center_frame,
            width=350,
            height=6,
            corner_radius=3,
            fg_color="#e8e8e8",
            progress_color="#00b4d8",
            mode="indeterminate"
        )
        self.progress.pack(pady=(30, 0))
        self.progress.start()
        
        # Simular carga y mostrar login
        self.root.after(2000, self.show_login)
    
    def show_login(self):
        """Mostrar pantalla de login"""
        # Detener y destruir loading
        self.progress.stop()
        self.loading_frame.destroy()
        
        # Frame principal con padding
        main_container = ctk.CTkFrame(self.root, fg_color="white")
        main_container.pack(fill="both", expand=True)
        
        # Frame central con contenido
        login_frame = ctk.CTkFrame(
            main_container,
            fg_color="white",
            width=400,
            height=600
        )
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        login_frame.pack_propagate(False)
        
        # === HEADER CON LOGO ===
        header_frame = ctk.CTkFrame(login_frame, fg_color="white", height=160)
        header_frame.pack(fill="x", pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Logo pequeño
        logo_box = ctk.CTkFrame(
            header_frame,
            fg_color="#00b4d8",
            corner_radius=15,
            width=70,
            height=70
        )
        logo_box.pack(pady=(0, 15))
        logo_box.pack_propagate(False)
        
        logo_icon = ctk.CTkLabel(
            logo_box,
            text="📦",
            font=("Segoe UI Emoji", 35),
            text_color="white"
        )
        logo_icon.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        title = ctk.CTkLabel(
            header_frame,
            text="NoteBox",
            font=("Arial", 32, "bold"),
            text_color="#2b2d42"
        )
        title.pack()
        
        # Subtítulo
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Sistema de Gestión de Inventario",
            font=("Arial", 13),
            text_color="#8d99ae"
        )
        subtitle.pack(pady=(5, 0))
        
        # === FORMULARIO ===
        form_frame = ctk.CTkFrame(login_frame, fg_color="white")
        form_frame.pack(fill="x", padx=30, pady=(20, 0))
        
        # Label Usuario
        user_label = ctk.CTkLabel(
            form_frame,
            text="Usuario",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        )
        user_label.pack(fill="x", pady=(0, 8))
        
        # Entry Usuario con icono
        user_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        user_frame.pack(fill="x", pady=(0, 20))
        
        user_icon = ctk.CTkLabel(
            user_frame,
            text="👤",
            font=("Segoe UI Emoji", 16),
            width=40
        )
        user_icon.pack(side="left")
        
        self.user_entry = ctk.CTkEntry(
            user_frame,
            textvariable=self.username_var,
            placeholder_text="Ingrese su usuario",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=2,
            border_color="#e0e0e0",
            fg_color="white"
        )
        self.user_entry.pack(side="left", fill="x", expand=True)
        
        # Label Contraseña
        pass_label = ctk.CTkLabel(
            form_frame,
            text="Contraseña",
            font=("Arial", 13, "bold"),
            text_color="#2b2d42",
            anchor="w"
        )
        pass_label.pack(fill="x", pady=(0, 8))
        
        # Entry Contraseña con icono
        pass_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        pass_frame.pack(fill="x", pady=(0, 15))
        
        pass_icon = ctk.CTkLabel(
            pass_frame,
            text="🔒",
            font=("Segoe UI Emoji", 16),
            width=40
        )
        pass_icon.pack(side="left")
        
        self.pass_entry = ctk.CTkEntry(
            pass_frame,
            textvariable=self.password_var,
            placeholder_text="Ingrese su contraseña",
            show="●",
            height=45,
            font=("Arial", 13),
            corner_radius=8,
            border_width=2,
            border_color="#e0e0e0",
            fg_color="white"
        )
        self.pass_entry.pack(side="left", fill="x", expand=True)
        
        # Checkbox Recordar
        remember_check = ctk.CTkCheckBox(
            form_frame,
            text="Recordar usuario",
            variable=self.remember_var,
            font=("Arial", 12),
            text_color="#6c757d",
            fg_color="#00b4d8",
            hover_color="#0096c7",
            corner_radius=4
        )
        remember_check.pack(anchor="w", pady=(0, 25))
        
        # Botón Ingresar
        login_btn = ctk.CTkButton(
            form_frame,
            text="INGRESAR",
            command=self.login,
            height=50,
            font=("Arial", 14, "bold"),
            fg_color="#00b4d8",
            hover_color="#0077b6",
            corner_radius=8,
            cursor="hand2"
        )
        login_btn.pack(fill="x", pady=(0, 15))
        
        # Link contraseña
        forgot_btn = ctk.CTkButton(
            form_frame,
            text="¿Olvidó su contraseña?",
            command=self.forgot_password,
            font=("Arial", 12),
            text_color="#00b4d8",
            fg_color="transparent",
            hover_color="#f8f9fa",
            cursor="hand2",
            height=30
        )
        forgot_btn.pack()
        
        # === FOOTER ===
        footer = ctk.CTkLabel(
            login_frame,
            text="NoteBox v1.0 - 2025",
            font=("Arial", 11),
            text_color="#adb5bd"
        )
        footer.pack(side="bottom", pady=20)
        
        # Focus en campo usuario
        self.user_entry.focus()
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Procesar login"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning(
                "Campos vacíos",
                "Por favor complete todos los campos"
            )
            return
        
        # Aquí conectar con el controller
        print(f"Login attempt: {username}")
        messagebox.showinfo("Éxito", f"Bienvenido {username}")
        
    def forgot_password(self):
        """Recuperar contraseña"""
        messagebox.showinfo(
            "Recuperar contraseña",
            "Contacte al administrador del sistema"
        )


# Ejecutar
if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginView(root)
    root.mainloop()