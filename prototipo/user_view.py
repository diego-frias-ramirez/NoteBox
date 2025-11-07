import tkinter as tk
from tkinter import ttk, messagebox
from user_controller import UserController

class UserView:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Gestión de Usuarios")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f5f6fa")
        self.user_controller = UserController()
        
        self.center_window()
        self.create_widgets()
        self.load_users()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def create_widgets(self):
        # Header
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=70)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)
        
        tk.Label(
            top_frame,
            text=f"Hola, {self.username}",
            font=("Segoe UI", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(side="left", padx=30, pady=20)
        
        tk.Button(
            top_frame,
            text="Cerrar Sesión",
            font=("Segoe UI", 10),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.logout,
            padx=20,
            pady=8
        ).pack(side="right", padx=30)
        
        tk.Button(
            top_frame,
            text="Dashboard",
            font=("Segoe UI", 10),
            bg="#27ae60",  # Verde como pediste
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.ir_dashboard,
            padx=20,
            pady=8
        ).pack(side="right", padx=10)
        
        tk.Button(
            top_frame,
            text="Productos",
            font=("Segoe UI", 10),
            bg="#3498db",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.ir_productos,
            padx=20,
            pady=8
        ).pack(side="right", padx=10)
        
        # Main content
        main_frame = tk.Frame(self.root, bg="#f5f6fa")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#f5f6fa")
        btn_frame.pack(fill="x", pady=(0, 20))
        
        buttons = [
            (" Agregar", "#27ae60", self.add_user),
            (" Modificar", "#f39c12", self.edit_user),
            (" Eliminar", "#e74c3c", self.delete_user),
            (" Actualizar", "#3498db", self.load_users)
        ]
        
        for text, color, cmd in buttons:
            tk.Button(
                btn_frame,
                text=text,
                bg=color,
                fg="white",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                cursor="hand2",
                command=cmd,
                padx=20,
                pady=10
            ).pack(side="left", padx=(0, 10))
        
        # Table
        self.setup_table(main_frame)
    
    def setup_table(self, parent):
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(fill="both", expand=True)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="#2c3e50", 
                       rowheight=35, fieldbackground="white", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#34495e", foreground="white",
                       font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[("selected", "#3498db")])
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Usuario", "Nombre", "Correo"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        for col, width in [("ID", 80), ("Usuario", 150), ("Nombre", 250), ("Correo", 250)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center" if col == "ID" else "w")
    
    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for user in self.user_controller.obtener_usuarios():
            self.tree.insert("", "end", values=(
                user['id_usuario'], user['username'], user['nombre'], user['correo']
            ))
    
    def add_user(self):
        UserFormDialog(self.root, self, mode="add")
    
    def edit_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un usuario")
            return
        
        user_id = self.tree.item(selected[0])['values'][0]
        user_data = self.user_controller.obtener_usuario(user_id)
        if user_data:
            UserFormDialog(self.root, self, mode="edit", user_data=user_data)
    
    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un usuario")
            return
        
        values = self.tree.item(selected[0])['values']
        if messagebox.askyesno("Confirmar", f"¿Eliminar a '{values[1]}'?"):
            success, msg = self.user_controller.eliminar_usuario(values[0])
            messagebox.showinfo("Resultado", msg) if success else messagebox.showerror("Error", msg)
            self.load_users()
    
    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Cerrar sesión?"):
            self.user_controller.close()
            self.root.destroy()
            
            from login_view import LoginView
            new_root = tk.Tk()
            LoginView(new_root)
            new_root.mainloop()
    
    def ir_productos(self):
        self.user_controller.close()
        self.root.destroy()
        
        from products_view import ProductsView
        new_root = tk.Tk()
        ProductsView(new_root, self.username)
        new_root.mainloop()
    
    def ir_dashboard(self):
        self.user_controller.close()
        self.root.destroy()
        
        from dashboard_view import DashboardView
        new_root = tk.Tk()
        DashboardView(new_root, self.username)
        new_root.mainloop()
    
    def on_closing(self):
        self.user_controller.close()
        self.root.destroy()


class UserFormDialog:
    def __init__(self, parent, user_view, mode="add", user_data=None):
        self.parent = parent
        self.user_view = user_view
        self.mode = mode
        self.user_data = user_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Usuario" if mode == "add" else "Modificar Usuario")
        self.dialog.geometry("400x550")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#f5f6fa")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.center_window()
        self.create_widgets()
        
        if mode == "edit" and user_data:
            self.fill_form()
    
    def center_window(self):
        self.dialog.update_idletasks()
        w, h = self.dialog.winfo_width(), self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (h // 2)
        self.dialog.geometry(f'{w}x{h}+{x}+{y}')
    
    def create_widgets(self):
        main_frame = tk.Frame(self.dialog, bg="#f5f6fa")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        title = "Agregar Usuario" if self.mode == "add" else "Modificar Usuario"
        tk.Label(
            main_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg="#f5f6fa",
            fg="#2c3e50"
        ).pack(pady=(0, 25))
        
        fields = [
            ("Usuario:", "username"),
            ("Nombre:", "nombre"),
            ("Correo:", "correo"),
            ("Contraseña:", "password")
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            tk.Label(
                main_frame,
                text=label_text,
                font=("Segoe UI", 10),
                bg="#f5f6fa",
                fg="#2c3e50",
                anchor="w"
            ).pack(fill="x", pady=(0, 5))
            
            entry = tk.Entry(
                main_frame,
                font=("Segoe UI", 11),
                bg="white",
                fg="#2c3e50",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#dfe6e9",
                highlightcolor="#3498db"
            )
            
            if field_name == "password":
                entry.config(show="•")
            
            entry.pack(fill="x", ipady=8, pady=(0, 15))
            self.entries[field_name] = entry
        
        if self.mode == "edit":
            tk.Label(
                main_frame,
                text="Deja vacía la contraseña para no cambiarla",
                font=("Segoe UI", 9, "italic"),
                bg="#f5f6fa",
                fg="#7f8c8d"
            ).pack(pady=(0, 15))
        
        btn_frame = tk.Frame(main_frame, bg="#f5f6fa")
        btn_frame.pack(fill="x", pady=(5, 0))
        
        tk.Button(
            btn_frame,
            text="Guardar",
            font=("Segoe UI", 11, "bold"),
            bg="#27ae60",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.save,
            padx=30,
            pady=10
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=("Segoe UI", 11),
            bg="#95a5a6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.dialog.destroy,
            padx=30,
            pady=10
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))
    
    def fill_form(self):
        self.entries['username'].insert(0, self.user_data['username'])
        self.entries['nombre'].insert(0, self.user_data['nombre'])
        self.entries['correo'].insert(0, self.user_data['correo'])
    
    def save(self):
        username = self.entries['username'].get().strip()
        nombre = self.entries['nombre'].get().strip()
        correo = self.entries['correo'].get().strip()
        password = self.entries['password'].get().strip()
        
        if self.mode == "add":
            success, msg = self.user_view.user_controller.crear_usuario(
                username, nombre, correo, password
            )
        else:
            success, msg = self.user_view.user_controller.modificar_usuario(
                self.user_data['id_usuario'], username, nombre, correo, 
                password if password else None
            )
        
        if success:
            messagebox.showinfo("Éxito", msg)
            self.user_view.load_users()
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", msg)