"""
NoteBox - Componente Toast Notification
Ubicación: components/toast.py
"""

import customtkinter as ctk
import time

class ToastNotification(ctk.CTkFrame):
    """
    Notificación flotante tipo 'Toast' que aparece y desaparece automáticamente.
    Diseño estilo 'Card' moderno y limpio.
    """
    
    def __init__(self, master, title, message, icon="info", duration=3000, 
                 fg_color="#FFFFFF", border_color="#E2E8F0", width=350):
        super().__init__(master, fg_color=fg_color, border_width=1, 
                         border_color=border_color, corner_radius=12, width=width)
        
        self.duration = duration
        self.start_time = None
        self.is_destroying = False
        
        # Elevación visual (Sombra simulada con borde sutil)
        self.configure(border_width=1, border_color="#CBD5E1")
        
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
        
        # Barra de color lateral (indicador visual)
        self.icon_frame = ctk.CTkFrame(self, fg_color=icon_color, width=6, corner_radius=6)
        self.icon_frame.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        
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
            wraplength=width-50, # Ajuste para evitar desborde
            justify="left"
        )
        self.msg_lbl.pack(anchor="w", pady=(2, 0))
        
        # Botón cerrar pequeño
        self.close_btn = ctk.CTkButton(
            self, text="×", width=24, height=24, 
            fg_color="transparent", text_color="#94A3B8",
            hover_color="#F1F5F9", font=ctk.CTkFont(size=18),
            command=self.animate_destroy,
            corner_radius=12
        )
        self.close_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-8, y=8)
        
    def show_toast(self, x, y):
        """Muestra el toast en la posición dada."""
        self.place(x=x, y=y)
        self.lift()
        
        # Iniciar temporizador de desvanecimiento
        self.after(self.duration, self.animate_destroy)

    def animate_destroy(self):
        """Destruye el widget."""
        if not self.is_destroying:
            self.is_destroying = True
            try:
                self.destroy()
            except Exception:
                pass

class ToastManager:
    """Gestor para mostrar Toasts en cola con posicionamiento robusto."""
    
    def __init__(self, master_window):
        self.master = master_window
        self.active_toasts = []
        self.spacing = 12
        self.start_y = 90  # Un poco más abajo del header
        self.end_x = 25    # Margen derecho consistente
        
        # Vincular evento de redimensionamiento para ajustar posiciones
        try:
            self.master.bind("<Configure>", self._on_window_resize, add="+")
        except Exception:
            pass
            
    def show_toast(self, title, message, icon="info", duration=4000):
        """Crea y muestra una nueva notificación toast."""
        # Limitar número de toasts simultáneos para no saturar
        max_toasts = 4
        if len(self.active_toasts) >= max_toasts:
            # Eliminar el más antiguo
            try:
                oldest = self.active_toasts.pop(0)
                oldest.destroy()
            except Exception:
                pass

        try:
            toast = ToastNotification(self.master, title, message, icon, duration)
            
            # Calcular posición inicial
            self._update_toast_position(toast, len(self.active_toasts))
            
            self.active_toasts.append(toast)
            
            # Limpiar referencia cuando se destruya
            toast.bind("<Destroy>", lambda e: self._on_toast_destroy(toast))
            
        except Exception as e:
            print(f"Error showing toast: {e}")
        
    def _update_toast_position(self, toast, index):
        """Calcula y aplica la posición de un toast específico."""
        try:
            if not toast.winfo_exists():
                return
                
            # Calcular Y basado en el índice en la pila
            current_y = self.start_y
            for i in range(index):
                if i < len(self.active_toasts):
                    prev_toast = self.active_toasts[i]
                    if prev_toast.winfo_exists():
                        current_y += prev_toast.winfo_reqheight() + self.spacing
            
            # Calcular X (siempre alineado a la derecha)
            window_width = self.master.winfo_width()
            # Si la ventana no está renderizada aún, usar valor por defecto seguro
            if window_width < 100: 
                window_width = 1000 
                
            toast_width = toast.winfo_reqwidth()
            pos_x = window_width - toast_width - self.end_x
            
            toast.show_toast(pos_x, current_y)
        except Exception:
            pass

    def _on_toast_destroy(self, toast):
        """Callback cuando un toast se destruye."""
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)
            # Reorganizar los restantes con un pequeño delay para suavidad
            self.master.after(10, self._reposition_all_toasts)
            
    def _reposition_all_toasts(self):
        """Recalcula la posición de todos los toasts activos."""
        current_y = self.start_y
        window_width = self.master.winfo_width()
        
        for toast in self.active_toasts:
            try:
                if toast.winfo_exists():
                    toast_width = toast.winfo_reqwidth()
                    pos_x = window_width - toast_width - self.end_x
                    toast.place(x=pos_x, y=current_y)
                    current_y += toast.winfo_reqheight() + self.spacing
            except Exception:
                pass

    def _on_window_resize(self, event):
        """Manejador del evento resize de la ventana principal."""
        # Solo reaccionar si es evento de la ventana principal
        if event.widget == self.master:
            self._reposition_all_toasts()

