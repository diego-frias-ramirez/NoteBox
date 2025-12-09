"""
NoteBox - Componente Toast Notification
Ubicación: components/toast.py
"""

import customtkinter as ctk
import time

class ToastNotification(ctk.CTkFrame):
    """
    Notificación flotante tipo 'Toast' que aparece y desaparece automáticamente.
    Diseño estilo 'Card' bonita.
    """
    
    def __init__(self, master, title, message, icon="info", duration=3000, 
                 fg_color="#FFFFFF", border_color="#E2E8F0", width=350):
        super().__init__(master, fg_color=fg_color, border_width=1, 
                         border_color=border_color, corner_radius=15, width=width)
        
        self.duration = duration
        self.start_time = None
        self.is_destroying = False
        
        # Sombra/Elevación simulada (opcional, simplificado para CTk)
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Icono
        icon_colors = {
            "info": "#3B82F6",    # Azul
            "success": "#10B981", # Verde
            "warning": "#F59E0B", # Naranja
            "error": "#EF4444"    # Rojo
        }
        icon_color = icon_colors.get(icon, icon_colors["info"])
        
        self.icon_frame = ctk.CTkFrame(self, fg_color=icon_color, width=5, corner_radius=5)
        self.icon_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        
        # Contenido
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=12)
        
        self.title_lbl = ctk.CTkLabel(
            self.content, 
            text=title, 
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#1E293B"
        )
        self.title_lbl.pack(anchor="w")
        
        self.msg_lbl = ctk.CTkLabel(
            self.content, 
            text=message, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#64748B",
            wraplength=width-40,
            justify="left"
        )
        self.msg_lbl.pack(anchor="w", pady=(2, 0))
        
        # Botón cerrar pequeño
        self.close_btn = ctk.CTkButton(
            self, text="×", width=20, height=20, 
            fg_color="transparent", text_color="#94A3B8",
            hover_color="#F1F5F9", font=ctk.CTkFont(size=16),
            command=self.animate_destroy
        )
        self.close_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)
        
    def show_toast(self, x, y):
        """Muestra el toast en la posición dada."""
        self.place(x=x, y=y)
        self.lift()
        
        # Iniciar temporizador de desvanecimiento
        self.after(self.duration, self.animate_destroy)

    def animate_destroy(self):
        """Destruye el widget con una animación simple (si fuera posible, aquí solo destroy)."""
        if not self.is_destroying:
            self.is_destroying = True
            self.destroy()

class ToastManager:
    """Gestor para mostrar Toasts en cola."""
    
    def __init__(self, master_window):
        self.master = master_window
        self.queue = []
        self.active_toasts = []
        self.spacing = 10
        self.start_y = 80  # Debajo del header
        self.end_x = 20    # Margen derecho
        
    def show_toast(self, title, message, icon="info", duration=4000):
        """Crea y encola un nuevo toast."""
        # Limitar número de toasts simultáneos
        if len(self.active_toasts) >= 3:
            # Eliminar el más antiguo inmediatamente para hacer espacio
            oldest = self.active_toasts.pop(0)
            oldest.destroy()

        toast = ToastNotification(self.master, title, message, icon, duration)
        
        # Calcular posición Y
        current_y = self.start_y
        for t in self.active_toasts:
            current_y += t.winfo_reqheight() + self.spacing
            
        # Posición X (alineado a la derecha)
        window_width = self.master.winfo_width()
        toast_width = toast.winfo_reqwidth()
        pos_x = window_width - toast_width - self.end_x
        
        toast.show_toast(pos_x, current_y)
        self.active_toasts.append(toast)
        
        # Limpiar referencia cuando se destruya
        toast.bind("<Destroy>", lambda e: self._on_toast_destroy(toast))
        
    def _on_toast_destroy(self, toast):
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)
            self._reposition_toasts()
            
    def _reposition_toasts(self):
        """Reorganiza los toasts restantes hacia arriba."""
        current_y = self.start_y
        window_width = self.master.winfo_width()
        
        for t in self.active_toasts:
            try:
                if t.winfo_exists():
                    t_width = t.winfo_reqwidth()
                    pos_x = window_width - t_width - self.end_x
                    t.place(x=pos_x, y=current_y)
                    current_y += t.winfo_reqheight() + self.spacing
            except Exception:
                pass
