"""
NoteBox - Vista del Login
"""

import customtkinter as ctk
from PIL import Image
import os

# Configuración del tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class NoteBoxLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de ventana
        self.title("NoteBox - Login")
        self.geometry("420x580")
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")
        
        # Ruta base del proyecto
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Centrar ventana
        self.center_window()
        
        # Crear controlador
        from controller.login_controller import LoginController
        self.controller = LoginController()
        
        # Crear UI
        self.create_widgets()
    
    def center_window(self):
        self.update_idletasks()
        w, h = 420, 580
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
    
    def load_logo(self):
        # Cargar logo desde assets/icons/
        logo_path = os.path.join(self.base_path, "..", "assets", "icons", "logo.png")
        
        try:
            img = Image.open(logo_path)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
        except FileNotFoundError:
            print(f"Logo no encontrado en: {logo_path}")
            print("Asegúrate de tener la imagen en assets/icons/logo.png")
            return None
    
    def create_widgets(self):
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=40, pady=30)
        
        # Logo desde assets/icons/
        logo_img = self.load_logo()
        logo_label = ctk.CTkLabel(main_frame, image=logo_img, text="") if logo_img else ctk.CTkLabel(main_frame, text="📦", font=ctk.CTkFont(size=50))
        logo_label.pack(pady=(20, 10))
        
        # Título
        title = ctk.CTkLabel(
            main_frame, text="NoteBox",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#1a1a2e"
        )
        title.pack(pady=(5, 0))
        
        # Subtítulo
        subtitle = ctk.CTkLabel(
            main_frame, text="Sistema de Gestión de Inventario",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#6b7280"
        )
        subtitle.pack(pady=(0, 35))
        
        # Campo Usuario
        user_label = ctk.CTkLabel(
            main_frame, text="Usuario",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#374151", anchor="w"
        )
        user_label.pack(fill="x", pady=(0, 5))
        
        self.user_entry = ctk.CTkEntry(
            main_frame, height=48, corner_radius=10,
            placeholder_text="  👤  Ingrese su usuario",
            font=ctk.CTkFont(size=13),
            fg_color="#F3F4F6", border_color="#E5E7EB",
            border_width=1, text_color="#1f2937"
        )
        self.user_entry.pack(fill="x", pady=(0, 15))
        
        # Campo Contraseña
        pass_label = ctk.CTkLabel(
            main_frame, text="Contraseña",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#374151", anchor="w"
        )
        pass_label.pack(fill="x", pady=(0, 5))
        
        self.pass_entry = ctk.CTkEntry(
            main_frame, height=48, corner_radius=10,
            placeholder_text="  🔒  Ingrese su contraseña",
            font=ctk.CTkFont(size=13), show="•",
            fg_color="#F3F4F6", border_color="#E5E7EB",
            border_width=1, text_color="#1f2937"
        )
        self.pass_entry.pack(fill="x", pady=(0, 10))
        
        # Checkbox Recordar
        self.remember_var = ctk.BooleanVar()
        remember_check = ctk.CTkCheckBox(
            main_frame, text="Recordar usuario",
            font=ctk.CTkFont(size=12),
            variable=self.remember_var,
            fg_color="#00B4D8", hover_color="#0096C7",
            text_color="#6b7280", corner_radius=5
        )
        remember_check.pack(anchor="w", pady=(5, 20))
        
        # Botón Ingresar
        login_btn = ctk.CTkButton(
            main_frame, text="INGRESAR", height=50,
            corner_radius=25, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#00B4D8", hover_color="#0096C7",
            text_color="white", command=self.login
        )
        login_btn.pack(fill="x", pady=(0, 15))
        
        # Link olvidó contraseña
        forgot_btn = ctk.CTkButton(
            main_frame, text="¿Olvidó su contraseña?",
            font=ctk.CTkFont(size=12), fg_color="transparent",
            text_color="#00B4D8", hover_color="#E0F7FF",
            command=self.forgot_password
        )
        forgot_btn.pack(pady=(0, 30))
        
        # Separador
        separator = ctk.CTkFrame(main_frame, height=1, fg_color="#E5E7EB")
        separator.pack(fill="x", pady=(10, 15))
        
        # Versión
        version = ctk.CTkLabel(
            main_frame, text="NoteBox v1.0 - 2025",
            font=ctk.CTkFont(size=11),
            text_color="#9CA3AF"
        )
        version.pack(pady=(5, 0))
    
    def login(self):
        user = self.user_entry.get()
        pwd = self.pass_entry.get()
        
        if not user or not pwd:
            self.show_message("Por favor complete todos los campos", "warning")
            return
        
        # Autenticar con el controlador
        user_data = self.controller.authenticate_user(user, pwd)
        
        if user_data:
            # Recordar usuario si está marcado
            self.controller.remember_user(user, self.remember_var.get())
            
            # Mostrar mensaje de éxito
            self.show_message(f"¡Bienvenido, {user_data['nombre']}!", "success")
            
            # Cerrar ventana de login y abrir dashboard
            self.destroy()
            from view.dashboard_view import DashboardView
            DashboardView(user_data).run()
        else:
            self.show_message("Usuario o contraseña incorrectos", "error")
    
    def forgot_password(self):
        self.show_message("Contacte al administrador", "info")
    
    def show_message(self, msg, type="info"):
        colors = {
            "success": "#10B981", "error": "#EF4444",
            "warning": "#F59E0B", "info": "#3B82F6"
        }
        
        popup = ctk.CTkToplevel(self)
        popup.title("")
        popup.geometry("300x100")
        popup.resizable(False, False)
        popup.configure(fg_color="#FFFFFF")
        popup.transient(self)
        popup.grab_set()
        
        # Centrar popup
        popup.update_idletasks()
        x = self.winfo_x() + (420 - 300) // 2
        y = self.winfo_y() + (580 - 100) // 2
        popup.geometry(f"300x100+{x}+{y}")
        
        label = ctk.CTkLabel(
            popup, text=msg,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=colors.get(type, "#374151")
        )
        label.pack(expand=True)
        
        popup.after(2000, popup.destroy)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = NoteBoxLogin()
    app.run()