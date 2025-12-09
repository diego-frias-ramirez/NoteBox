"""
NoteBox - Componente de Pantalla de Carga (Diseño Mejorado)
Ubicación: components/loading_overlay.py
"""

import customtkinter as ctk
import tkinter as tk

class LoadingOverlay(ctk.CTkFrame):
    """
    Overlay minimalista y elegante que cubre el contenedor principal mientras se cargan datos.
    Diseño: Fondo blanco con animación de puntos suave.
    """
    def __init__(self, master, message="Cargando"):
        super().__init__(master, fg_color="white", corner_radius=0)
        
        # Contenedor central
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Mensaje "Cargando"
        self.message_label = ctk.CTkLabel(
            self.center_frame, 
            text=message,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1E293B"
        )
        self.message_label.pack(pady=(0, 20))
        
        # Frame para los puntos animados
        self.dots_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.dots_frame.pack()
        
        # Crear 3 puntos
        self.dots = []
        self.dot_colors = ["#CBD5E1", "#94A3B8", "#64748B"]  # Grises suaves
        
        for i in range(3):
            dot = ctk.CTkLabel(
                self.dots_frame,
                text="●",
                font=ctk.CTkFont(size=32),
                text_color=self.dot_colors[0],
                width=30
            )
            dot.pack(side="left", padx=8)
            self.dots.append(dot)
        
        # Estado de animación
        self.animation_step = 0
        self.animate_id = None
        self.animate()

    def animate(self):
        """Anima los puntos con efecto de onda."""
        # Calcular qué punto debe estar activo
        for i, dot in enumerate(self.dots):
            # Determinar el color basado en la posición en la animación
            offset = (self.animation_step - i) % 3
            
            if offset == 0:
                # Punto activo - color oscuro
                color = "#00B4D8"
                scale = 1.2
            elif offset == 1:
                # Punto siguiente - color medio
                color = "#64748B"
                scale = 1.0
            else:
                # Punto inactivo - color claro
                color = "#CBD5E1"
                scale = 0.8
            
            dot.configure(text_color=color)
        
        # Incrementar paso de animación
        self.animation_step = (self.animation_step + 1) % 3
        
        # Continuar animación
        if self.winfo_exists():
            self.animate_id = self.after(400, self.animate)  # 400ms por ciclo

    def stop(self):
        """Detiene la animación."""
        if self.animate_id:
            self.after_cancel(self.animate_id)
            self.animate_id = None
            
    def destroy(self):
        self.stop()
        super().destroy()
