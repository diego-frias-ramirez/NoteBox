import tkinter as tk
from tkinter import ttk, messagebox
from user_controller import UserController
from products_controller import ProductController

class DashboardView:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Dashboard - Sistema de Gestión")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f5f6fa")
        
        # Controllers
        self.user_controller = UserController()
        self.product_controller = ProductController()
        
        self.center_window()
        self.create_widgets()
        self.load_stats()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def create_widgets(self):
        # Header
        top_frame = tk.Frame(self.root, bg="#27ae60", height=80)  
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)
        
        tk.Label(
            top_frame,
            text=f"Dashboard - Bienvenido/a, {self.username}",
            font=("Segoe UI", 20, "bold"),
            bg="#27ae60",
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
            text="Usuarios",
            font=("Segoe UI", 10),
            bg="#9b59b6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.ir_usuarios,
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
        
        # Stats Cards
        stats_frame = tk.Frame(main_frame, bg="#f5f6fa")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        self.stats_cards = []
        stats_data = [
            ("Usuarios Registrados", "#27ae60", "user_count"),
            ("Productos Activos", "#3498db", "product_active"),
            ("Total Productos", "#9b59b6", "product_total"),
            ("Inactivos", "#e74c3c", "product_inactive")
        ]
        
        for title, color, key in stats_data:
            card = self.create_stat_card(stats_frame, title, color, key)
            self.stats_cards.append(card)
        
        # Quick Actions
        actions_frame = tk.Frame(main_frame, bg="#f5f6fa")
        actions_frame.pack(fill="x", pady=(20, 0))
        
        tk.Label(
            actions_frame,
            text="Acciones Rápidas",
            font=("Segoe UI", 14, "bold"),
            bg="#f5f6fa",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))
        
        btn_frame = tk.Frame(actions_frame, bg="#f5f6fa")
        btn_frame.pack(fill="x")
        
        actions = [
            (" Agregar Usuario", "#27ae60", self.ir_usuarios),
            (" Agregar Producto", "#3498db", self.ir_productos),
            (" Actualizar Estadísticas", "#95a5a6", self.load_stats)
        ]
        
        for text, color, cmd in actions:
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
    
    def create_stat_card(self, parent, title, color, key):
        card = tk.Frame(parent, bg=color, width=250, height=120)
        card.pack_propagate(False)
        card.pack(side="left", padx=(0, 15), pady=5)
        
        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg=color,
            fg="white"
        ).pack(pady=(15, 5))
        
        value_label = tk.Label(
            card,
            text="Cargando...",
            font=("Segoe UI", 24, "bold"),
            bg=color,
            fg="white"
        )
        value_label.pack(expand=True)
        
        return {"label": value_label, "key": key}
    
    def load_stats(self):
        # Cargar estadísticas
        users = self.user_controller.obtener_usuarios()
        products = self.product_controller.obtener_productos()
        
        active_products = [p for p in products if p['status'] == 1]
        inactive_products = [p for p in products if p['status'] == 0]
        
        stats = {
            "user_count": len(users),
            "product_active": len(active_products),
            "product_total": len(products),
            "product_inactive": len(inactive_products)
        }
        
        for card in self.stats_cards:
            key = card["key"]
            value = stats.get(key, 0)
            card["label"].config(text=str(value))
    
    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Cerrar sesión?"):
            self.user_controller.close()
            self.product_controller.close()
            self.root.destroy()
            
            from login_view import LoginView
            new_root = tk.Tk()
            LoginView(new_root)
            new_root.mainloop()
    
    def ir_usuarios(self):
        self.user_controller.close()
        self.product_controller.close()
        self.root.destroy()
        
        from user_view import UserView
        new_root = tk.Tk()
        UserView(new_root, self.username)
        new_root.mainloop()
    
    def ir_productos(self):
        self.user_controller.close()
        self.product_controller.close()
        self.root.destroy()
        
        from products_view import ProductsView
        new_root = tk.Tk()
        ProductsView(new_root, self.username)
        new_root.mainloop()
    
    def on_closing(self):
        self.user_controller.close()
        self.product_controller.close()
        self.root.destroy()