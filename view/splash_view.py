"""
NoteBox - Vista del Splash Screen (CORREGIDO)
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
from controller.splash_controller import SplashScreenController
from utils.helpers import Helpers

class NoteBoxSplash:
    """Vista del Splash Screen."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NoteBox")
        self.root.geometry("500x280")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.center_window()
        
        self.canvas = tk.Canvas(self.root, width=500, height=280, 
                                 highlightthickness=0, bg="#1E293B")
        self.canvas.pack(fill="both", expand=True)
        
        self.load_images()
        self.create_ui()
        
        self.controller = SplashScreenController()
        
        # Iniciar animación después de mostrar la ventana
        self.root.after(500, self.animate)
    
    def center_window(self):
        w, h = 500, 280
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
    
    def round_corners(self, img, radius):
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], 
                                radius=radius, fill=255)
        img_rounded = img.copy()
        img_rounded.putalpha(mask)
        return img_rounded
    
    def load_images(self):
        bg_path = Helpers.get_asset_path('splash_image', 'assets/images/splash_bg.png')
        try:
            img = Image.open(bg_path)
            img = img.resize((500, 280), Image.LANCZOS)
            img = img.convert("RGBA")
            img = self.round_corners(img, 20)
            self.bg_image = ImageTk.PhotoImage(img)
        except:
            self.bg_image = None
        
        logo_path = Helpers.get_asset_path('splash_logo', 'assets/icons/logo.png')
        try:
            logo = Image.open(logo_path)
            logo = logo.resize((50, 50), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(logo)
        except:
            self.logo_image = None
    
    def create_ui(self):
        if self.bg_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        else:
            self.canvas.create_rectangle(0, 0, 500, 280, fill="#374151", outline="")
        
        if self.logo_image:
            self.canvas.create_image(25, 20, anchor="nw", image=self.logo_image)
        
        self.canvas.create_text(90, 45, text="NoteBox", anchor="w",
                                 font=("Segoe UI", 28, "bold"), fill="white")
        
        bar_y, bar_height, bar_width, bar_x = 245, 12, 420, 40
        
        self.canvas.create_rectangle(bar_x - 5, bar_y - 5, 
            bar_x + bar_width + 5, bar_y + bar_height + 5,
            fill="#FFFFFF", outline="")
        
        self.canvas.create_rectangle(bar_x, bar_y, 
            bar_x + bar_width, bar_y + bar_height,
            fill="#E0E0E0", outline="")
        
        self.progress_bar = self.canvas.create_rectangle(
            bar_x, bar_y, bar_x, bar_y + bar_height,
            fill="#00B4D8", outline="")
        
        self.status_text = self.canvas.create_text(
            250, 210, text="Iniciando NoteBox...", anchor="center",
            font=("Segoe UI", 10), fill="white")
        
        self.bar_x, self.bar_y = bar_x, bar_y
        self.bar_width, self.bar_height = bar_width, bar_height
    
    def update_progress_bar(self, progress):
        """Actualiza visualmente la barra de progreso."""
        new_width = self.bar_x + (self.bar_width * progress / 100)
        self.canvas.coords(self.progress_bar, 
            self.bar_x, self.bar_y, new_width, self.bar_y + self.bar_height)
        self.root.update_idletasks()
    
    def animate(self):
        """Ejecuta los pasos de carga."""
        if self.controller.is_complete():
            # Todos los pasos completados
            self.canvas.itemconfig(self.status_text, text="¡Listo!")
            self.update_progress_bar(100)
            self.root.after(500, self.open_main_window)
            return
        
        # Obtener paso actual
        if self.controller.current_step < self.controller.total_steps:
            step_name, _ = self.controller.steps[self.controller.current_step]
            self.canvas.itemconfig(self.status_text, text=step_name)
        
        # Ejecutar siguiente paso
        success = self.controller.next_step()
        
        if success:
            # Actualizar barra de progreso
            self.update_progress_bar(self.controller.get_progress())
            # Continuar con el siguiente paso
            self.root.after(300, self.animate)
        else:
            # Error crítico - mostrar mensaje
            self.canvas.itemconfig(self.status_text, 
                text="Error al iniciar. Revisa los logs.", fill="#EF4444")
            self.root.after(3000, self.root.destroy)
    
    def open_main_window(self):
        """Abre la ventana principal (login o dashboard)."""
        self.root.destroy()
        
        if self.controller.should_go_to_dashboard():
            # Ir directo al dashboard (hay sesión guardada)
            # from view.dashboard_view import NoteBoxDashboard
            # NoteBoxDashboard().run()
            pass
        else:
            # Ir al login
            from view.login_view import NoteBoxLogin
            NoteBoxLogin().run()
    
    def run(self):
        self.root.mainloop()