import tkinter as tk
from tkinter import messagebox
from auth_controller import AuthController
from dashboard_view import DashboardView  

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistema de Gestión")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6fa")
        
        self.auth_controller = AuthController()
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#f5f6fa")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Título
        tk.Label(
            main_frame, 
            text="Iniciar Sesión",
            font=("Segoe UI", 24, "bold"),
            bg="#f5f6fa",
            fg="#2c3e50"
        ).pack(pady=(0, 10))
        
        tk.Label(
            main_frame,
            text="Sistema de Gestión de Usuarios",
            font=("Segoe UI", 10),
            bg="#f5f6fa",
            fg="#7f8c8d"
        ).pack(pady=(0, 40))
        
        # Campos
        input_frame = tk.Frame(main_frame, bg="#f5f6fa")
        input_frame.pack(fill="x")
        
        for label_text, is_password in [("Usuario", False), ("Contraseña", True)]:
            tk.Label(
                input_frame,
                text=label_text,
                font=("Segoe UI", 10),
                bg="#f5f6fa",
                fg="#2c3e50",
                anchor="w"
            ).pack(fill="x", pady=(20 if label_text == "Contraseña" else 0, 5))
            
            entry = tk.Entry(
                input_frame,
                font=("Segoe UI", 11),
                bg="white",
                fg="#2c3e50",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#dfe6e9",
                highlightcolor="#3498db",
                show="•" if is_password else None
            )
            entry.pack(fill="x", ipady=8)
            
            if label_text == "Usuario":
                self.username_entry = entry
            else:
                self.password_entry = entry
        
        # Botón login
        tk.Button(
            input_frame,
            text="Iniciar Sesión",
            font=("Segoe UI", 11, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.login,
            activebackground="#2980b9",
            activeforeground="white"
        ).pack(fill="x", pady=(30, 0), ipady=10)
        
        # Info
        info_frame = tk.Frame(main_frame, bg="#ecf0f1")
        info_frame.pack(fill="x", pady=(30, 0))
        
        tk.Label(
            info_frame,
            text="Usuarios: admin/admin123 | juan/juan123 | maria/maria123",
            font=("Segoe UI", 9),
            bg="#ecf0f1",
            fg="#7f8c8d"
        ).pack(pady=10)
        
        # Bindings
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        success, message, user_data = self.auth_controller.login(username, password)
        
        if success:
            messagebox.showinfo("¡Bienvenido/a!", f"¡Bienvenido/a!\n\n{user_data['correo']}")
            self.auth_controller.close()
            self.root.destroy()
            
            # Nueva ventana con el nombre de usuario → Dashboard
            new_root = tk.Tk()
            DashboardView(new_root, user_data['username'])
            new_root.mainloop()
        else:
            messagebox.showerror("Error", message)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()