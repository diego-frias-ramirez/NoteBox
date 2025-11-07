import tkinter as tk
from tkinter import ttk, messagebox
from products_controller import ProductController

class ProductsView:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Gestión de Productos")
        self.root.geometry("1200x600")
        self.root.configure(bg="#f5f6fa")
        self.product_controller = ProductController()
        
        self.center_window()
        self.create_widgets()
        self.load_products()
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
            text=f"Bienvenido/a, {self.username}",
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
        ).pack(side="right", padx=10)
        
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
            text="Usuarios",
            font=("Segoe UI", 10),
            bg="#95a5a6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.volver_usuarios,
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
            (" Agregar Producto", "#27ae60", self.add_product),
            (" Actualizar Producto", "#f39c12", self.edit_product),
            (" Eliminar Producto", "#e74c3c", self.delete_product),
            (" Actualizar Lista", "#3498db", self.load_products)
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
            columns=("ID", "Producto", "Marca", "Precio", "Stock", "Proveedor", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        columns = [
            ("ID", 50),
            ("Producto", 180),
            ("Marca", 120),
            ("Precio", 100),
            ("Stock", 80),
            ("Proveedor", 150),
            ("Status", 80)
        ]
        
        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center" if col in ["ID", "Precio", "Stock", "Status"] else "w")
    
    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for product in self.product_controller.obtener_productos():
            status_text = "Activo" if product['status'] == 1 else "Inactivo"
            self.tree.insert("", "end", values=(
                product['id_producto'],
                product['nombre_producto'],
                product['marca'] or "N/A",
                f"${product['precio']:,}",
                product['stock'],
                product['proveedor'],
                status_text
            ))
    
    def add_product(self):
        ProductFormDialog(self.root, self, mode="add")
    
    def edit_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        product_id = self.tree.item(selected[0])['values'][0]
        product_data = self.product_controller.obtener_producto(product_id)
        if product_data:
            ProductFormDialog(self.root, self, mode="edit", product_data=product_data)
    
    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        values = self.tree.item(selected[0])['values']
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{values[1]}'?"):
            success, msg = self.product_controller.eliminar_producto(values[0])
            messagebox.showinfo("Resultado", msg) if success else messagebox.showerror("Error", msg)
            self.load_products()
    
    def volver_usuarios(self):
        self.product_controller.close()
        self.root.destroy()
        
        from user_view import UserView
        new_root = tk.Tk()
        UserView(new_root, self.username)
        new_root.mainloop()
    
    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Cerrar sesión?"):
            self.product_controller.close()
            self.root.destroy()
            
            from login_view import LoginView
            new_root = tk.Tk()
            LoginView(new_root)
            new_root.mainloop()
    
    def ir_dashboard(self):
        self.product_controller.close()
        self.root.destroy()
        
        from dashboard_view import DashboardView
        new_root = tk.Tk()
        DashboardView(new_root, self.username)
        new_root.mainloop()
    
    def on_closing(self):
        self.product_controller.close()
        self.root.destroy()


class ProductFormDialog:
    def __init__(self, parent, products_view, mode="add", product_data=None):
        self.parent = parent
        self.products_view = products_view
        self.mode = mode
        self.product_data = product_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Producto" if mode == "add" else "Actualizar Producto")
        self.dialog.geometry("500x550")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg="#f5f6fa")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.center_window()
        self.create_widgets()
        
        if mode == "edit" and product_data:
            self.fill_form()
    
    def center_window(self):
        self.dialog.update_idletasks()
        w, h = self.dialog.winfo_width(), self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (h // 2)
        self.dialog.geometry(f'{w}x{h}+{x}+{y}')
    
    def create_widgets(self):
        # Canvas y Scrollbar para el formulario
        canvas = tk.Canvas(self.dialog, bg="#f5f6fa", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f5f6fa")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido del formulario
        main_frame = tk.Frame(scrollable_frame, bg="#f5f6fa")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        title = "Agregar Producto" if self.mode == "add" else "Actualizar Producto"
        tk.Label(
            main_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg="#f5f6fa",
            fg="#2c3e50"
        ).pack(pady=(0, 25))
        
        fields = [
            ("Nombre del Producto:", "nombre_producto"),
            ("Stock:", "stock"),
            ("Proveedor:", "proveedor"),
            ("Precio:", "precio"),
            ("Status (1=Activo, 0=Inactivo):", "status"),
            ("Marca:", "marca"),
            ("Descripción:", "descripcion")
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
            entry.pack(fill="x", ipady=8, pady=(0, 12))
            self.entries[field_name] = entry
        
        btn_frame = tk.Frame(main_frame, bg="#f5f6fa")
        btn_frame.pack(fill="x", pady=(10, 0))
        
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
        
        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def fill_form(self):
        self.entries['nombre_producto'].insert(0, self.product_data['nombre_producto'])
        self.entries['stock'].insert(0, str(self.product_data['stock']))
        self.entries['proveedor'].insert(0, self.product_data['proveedor'])
        self.entries['precio'].insert(0, str(self.product_data['precio']))
        self.entries['status'].insert(0, str(self.product_data['status']))
        self.entries['marca'].insert(0, self.product_data['marca'] or "")
        self.entries['descripcion'].insert(0, self.product_data['descripcion'] or "")
    
    def save(self):
        nombre = self.entries['nombre_producto'].get().strip()
        stock = self.entries['stock'].get().strip()
        proveedor = self.entries['proveedor'].get().strip()
        precio = self.entries['precio'].get().strip()
        status = self.entries['status'].get().strip()
        marca = self.entries['marca'].get().strip()
        descripcion = self.entries['descripcion'].get().strip()
        
        if self.mode == "add":
            success, msg = self.products_view.product_controller.crear_producto(
                nombre, stock, proveedor, precio, status, marca, descripcion
            )
        else:
            success, msg = self.products_view.product_controller.modificar_producto(
                self.product_data['id_producto'], nombre, stock, proveedor, 
                precio, status, marca, descripcion
            )
        
        if success:
            messagebox.showinfo("Éxito", msg)
            self.products_view.load_products()
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", msg)