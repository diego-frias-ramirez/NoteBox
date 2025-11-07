import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class ImprovedDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Principal - Sistema de Inventario")
        self.root.geometry("1400x850")
        self.root.configure(bg="#f5f6fa")
        
        # Datos de ejemplo
        self.init_data()
        
        # Crear UI del Dashboard
        self.create_dashboard_ui()
    
    def init_data(self):
        self.products_file = "products.json"
        if os.path.exists(self.products_file):
            with open(self.products_file, 'r') as f:
                self.products = json.load(f)
        else:
            self.products = []
        
        # Datos de ventas
        self.weekly_sales = {
            "Lun": 1250,
            "Mar": 980,
            "Mié": 1580,
            "Jue": 1120,
            "Vie": 1450,
            "Sáb": 920,
            "Dom": 1080
        }
    
    def create_dashboard_ui(self):
        # ===== SIDEBAR IZQUIERDO =====
        sidebar = tk.Frame(self.root, bg="#2c3e50", width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo y título del sistema
        logo_frame = tk.Frame(sidebar, bg="#2c3e50")
        logo_frame.pack(pady=30)
        
        logo = tk.Label(logo_frame, text="📦", font=("Segoe UI", 36), bg="#2c3e50")
        logo.pack()
        
        app_name = tk.Label(logo_frame, text="Inventario Pro", 
                           font=("Segoe UI", 14, "bold"), 
                           bg="#2c3e50", fg="white")
        app_name.pack(pady=5)
        
        app_subtitle = tk.Label(logo_frame, text="Papelería El Estudiante", 
                               font=("Segoe UI", 9), 
                               bg="#2c3e50", fg="#95a5a6")
        app_subtitle.pack()
        
        # Menú de navegación
        menu_frame = tk.Frame(sidebar, bg="#2c3e50")
        menu_frame.pack(fill="x", pady=20)
        
        menu_items = [
            ("🏠", "Dashboard", True),
            ("📦", "Productos", False),
            ("🛒", "Ventas", False),
            ("👥", "Clientes", False),
            ("📊", "Reportes", False),
            ("⚙️", "Configuración", False)
        ]
        
        for icon, text, active in menu_items:
            self.create_menu_item(menu_frame, icon, text, active)
        
        # Usuario en la parte inferior
        user_frame = tk.Frame(sidebar, bg="#34495e")
        user_frame.pack(side="bottom", fill="x", pady=20, padx=15)
        
        user_icon = tk.Label(user_frame, text="👤", font=("Segoe UI", 24), 
                            bg="#34495e", fg="white")
        user_icon.pack(side="left", padx=10)
        
        user_info = tk.Frame(user_frame, bg="#34495e")
        user_info.pack(side="left", fill="x", expand=True)
        
        user_name = tk.Label(user_info, text="Administrador", 
                            font=("Segoe UI", 11, "bold"), 
                            bg="#34495e", fg="white", anchor="w")
        user_name.pack(anchor="w")
        
        user_role = tk.Label(user_info, text="Admin", 
                            font=("Segoe UI", 9), 
                            bg="#34495e", fg="#95a5a6", anchor="w")
        user_role.pack(anchor="w")
        
        # ===== CONTENIDO PRINCIPAL =====
        main_content = tk.Frame(self.root, bg="#f5f6fa")
        main_content.pack(side="right", fill="both", expand=True)
        
        # Header superior
        header = tk.Frame(main_content, bg="white", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Título y fecha
        header_left = tk.Frame(header, bg="white")
        header_left.pack(side="left", padx=30, pady=20)
        
        page_title = tk.Label(header_left, text="Hola, Bienvenido! 👋", 
                             font=("Segoe UI", 22, "bold"), 
                             bg="white", fg="#2c3e50")
        page_title.pack(anchor="w")
        
        date_label = tk.Label(header_left, 
                             text=datetime.now().strftime("%A, %d de %B del %Y"), 
                             font=("Segoe UI", 10), 
                             bg="white", fg="#7f8c8d")
        date_label.pack(anchor="w")
        
        # Búsqueda y notificaciones
        header_right = tk.Frame(header, bg="white")
        header_right.pack(side="right", padx=30, pady=20)
        
        search_frame = tk.Frame(header_right, bg="#f5f6fa", relief="flat")
        search_frame.pack(side="left", padx=10)
        
        search_icon = tk.Label(search_frame, text="🔍", font=("Segoe UI", 12), 
                              bg="#f5f6fa")
        search_icon.pack(side="left", padx=10)
        
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), 
                               bg="#f5f6fa", relief="flat", bd=0, 
                               width=25, fg="#7f8c8d")
        search_entry.pack(side="left", ipady=8)
        search_entry.insert(0, "Buscar...")
        
        notif_btn = tk.Label(header_right, text="🔔", font=("Segoe UI", 18), 
                            bg="white", cursor="hand2")
        notif_btn.pack(side="left", padx=15)
        
        # Contenedor de contenido
        content_container = tk.Frame(main_content, bg="#f5f6fa")
        content_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # ===== TARJETAS DE ESTADÍSTICAS =====
        stats_frame = tk.Frame(content_container, bg="#f5f6fa")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Calcular estadísticas
        total_products = len(self.products)
        low_stock = len([p for p in self.products if p.get('stock', 0) < 20])
        total_sales = sum(self.weekly_sales.values())
        active_products = len([p for p in self.products if p.get('stock', 0) > 0])
        
        stats_data = [
            {
                "title": "Total Productos",
                "value": str(total_products),
                "icon": "📦",
                "color": "#3498db",
                "bg": "#e3f2fd",
                "change": "+12%",
                "change_positive": True
            },
            {
                "title": "Stock Bajo",
                "value": str(low_stock),
                "icon": "⚠️",
                "color": "#e74c3c",
                "bg": "#ffebee",
                "change": "-5%",
                "change_positive": True
            },
            {
                "title": "Ventas Semanales",
                "value": f"${total_sales:,}",
                "icon": "💰",
                "color": "#2ecc71",
                "bg": "#e8f5e9",
                "change": "+23%",
                "change_positive": True
            },
            {
                "title": "Productos Activos",
                "value": str(active_products),
                "icon": "✅",
                "color": "#f39c12",
                "bg": "#fff3e0",
                "change": "+8%",
                "change_positive": True
            }
        ]
        
        for i, stat in enumerate(stats_data):
            self.create_stat_card(stats_frame, stat, i)
        
        # ===== SECCIÓN INFERIOR: GRÁFICAS Y PRODUCTOS =====
        bottom_section = tk.Frame(content_container, bg="#f5f6fa")
        bottom_section.pack(fill="both", expand=True)
        
        # Frame izquierdo - Gráfica de ventas
        chart_frame = tk.Frame(bottom_section, bg="white", relief="solid", bd=1)
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header de la gráfica
        chart_header = tk.Frame(chart_frame, bg="white")
        chart_header.pack(fill="x", padx=20, pady=15)
        
        chart_title = tk.Label(chart_header, text="Ventas Semanales", 
                              font=("Segoe UI", 14, "bold"), 
                              bg="white", fg="#2c3e50")
        chart_title.pack(side="left")
        
        chart_subtitle = tk.Label(chart_header, text="Últimos 7 días", 
                                 font=("Segoe UI", 9), 
                                 bg="white", fg="#95a5a6")
        chart_subtitle.pack(side="left", padx=10)
        
        # Filtro de período
        period_frame = tk.Frame(chart_header, bg="white")
        period_frame.pack(side="right")
        
        for period in ["Día", "Semana", "Mes"]:
            btn_bg = "#3498db" if period == "Semana" else "#ecf0f1"
            btn_fg = "white" if period == "Semana" else "#7f8c8d"
            period_btn = tk.Button(period_frame, text=period, 
                                  font=("Segoe UI", 9), 
                                  bg=btn_bg, fg=btn_fg, 
                                  relief="flat", cursor="hand2",
                                  padx=15, pady=5)
            period_btn.pack(side="left", padx=2)
        
        # Canvas para la gráfica
        self.create_sales_chart(chart_frame)
        
        # Frame derecho - Productos recientes
        products_frame = tk.Frame(bottom_section, bg="white", 
                                 relief="solid", bd=1, width=380)
        products_frame.pack(side="right", fill="y")
        products_frame.pack_propagate(False)
        
        # Header de productos
        prod_header = tk.Frame(products_frame, bg="white")
        prod_header.pack(fill="x", padx=20, pady=15)
        
        prod_title = tk.Label(prod_header, text="Productos Bajo Stock", 
                             font=("Segoe UI", 14, "bold"), 
                             bg="white", fg="#2c3e50")
        prod_title.pack(side="left")
        
        view_all = tk.Label(prod_header, text="Ver todos →", 
                           font=("Segoe UI", 9), 
                           bg="white", fg="#3498db", cursor="hand2")
        view_all.pack(side="right")
        
        # Lista de productos
        self.create_product_list(products_frame)
    
    def create_menu_item(self, parent, icon, text, active):
        bg_color = "#34495e" if active else "#2c3e50"
        
        item_frame = tk.Frame(parent, bg=bg_color)
        item_frame.pack(fill="x", pady=2)
        
        if active:
            indicator = tk.Frame(item_frame, bg="#3498db", width=4)
            indicator.pack(side="left", fill="y")
        
        item_content = tk.Frame(item_frame, bg=bg_color)
        item_content.pack(side="left", fill="x", expand=True, pady=12, padx=20)
        
        icon_label = tk.Label(item_content, text=icon, 
                             font=("Segoe UI", 16), 
                             bg=bg_color, fg="white")
        icon_label.pack(side="left", padx=(0, 15))
        
        text_label = tk.Label(item_content, text=text, 
                             font=("Segoe UI", 11, "bold" if active else "normal"), 
                             bg=bg_color, fg="white", anchor="w")
        text_label.pack(side="left", fill="x", expand=True)
        
        # Hover effect
        item_frame.bind("<Enter>", lambda e: item_content.config(bg="#34495e"))
        item_content.bind("<Enter>", lambda e: item_content.config(bg="#34495e"))
        icon_label.bind("<Enter>", lambda e: icon_label.config(bg="#34495e"))
        text_label.bind("<Enter>", lambda e: text_label.config(bg="#34495e"))
        
        if not active:
            item_frame.bind("<Leave>", lambda e: item_content.config(bg="#2c3e50"))
            item_content.bind("<Leave>", lambda e: item_content.config(bg="#2c3e50"))
            icon_label.bind("<Leave>", lambda e: icon_label.config(bg="#2c3e50"))
            text_label.bind("<Leave>", lambda e: text_label.config(bg="#2c3e50"))
    
    def create_stat_card(self, parent, data, col):
        card = tk.Frame(parent, bg="white", relief="solid", bd=1)
        card.grid(row=0, column=col, padx=8, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        # Contenido
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header con icono
        header = tk.Frame(content, bg="white")
        header.pack(fill="x")
        
        icon_frame = tk.Frame(header, bg=data['bg'], width=50, height=50)
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        icon = tk.Label(icon_frame, text=data['icon'], 
                       font=("Segoe UI", 20), 
                       bg=data['bg'])
        icon.place(relx=0.5, rely=0.5, anchor="center")
        
        # Cambio porcentual
        change_text = data['change']
        change_color = "#2ecc71" if data['change_positive'] else "#e74c3c"
        change_label = tk.Label(header, text=change_text, 
                               font=("Segoe UI", 10, "bold"), 
                               bg="white", fg=change_color)
        change_label.pack(side="right")
        
        # Valor principal
        value_label = tk.Label(content, text=data['value'], 
                              font=("Segoe UI", 32, "bold"), 
                              bg="white", fg=data['color'])
        value_label.pack(anchor="w", pady=(15, 5))
        
        # Título
        title_label = tk.Label(content, text=data['title'], 
                              font=("Segoe UI", 11), 
                              bg="white", fg="#7f8c8d")
        title_label.pack(anchor="w")
    
    def create_sales_chart(self, parent):
        canvas = tk.Canvas(parent, bg="white", height=300, 
                          highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        days = list(self.weekly_sales.keys())
        values = list(self.weekly_sales.values())
        
        max_value = max(values)
        bar_width = 50
        spacing = 100
        start_x = 80
        start_y = 270
        max_height = 200
        
        # Grid horizontal
        for i in range(5):
            y = start_y - (i * max_height / 4)
            canvas.create_line(50, y, 780, y, fill="#ecf0f1", width=1)
            value = int(max_value * i / 4)
            canvas.create_text(35, y, text=f"${value}", 
                             font=("Segoe UI", 8), fill="#95a5a6")
        
        # Dibujar barras
        for i, (day, value) in enumerate(zip(days, values)):
            x = start_x + i * spacing
            bar_height = (value / max_value) * max_height
            y = start_y - bar_height
            
            # Sombra de la barra
            canvas.create_rectangle(x + 2, start_y, x + bar_width + 2, y + 2, 
                                   fill="#e0e0e0", outline="")
            
            # Barra con gradiente (simulado)
            gradient_color = "#3498db"
            canvas.create_rectangle(x, start_y, x + bar_width, y, 
                                   fill=gradient_color, outline="")
            
            # Barra superior más clara
            canvas.create_rectangle(x, y, x + bar_width, y + 5, 
                                   fill="#5dade2", outline="")
            
            # Etiqueta del día
            canvas.create_text(x + bar_width/2, start_y + 20, 
                             text=day, font=("Segoe UI", 10, "bold"), 
                             fill="#7f8c8d")
            
            # Valor encima de la barra
            canvas.create_text(x + bar_width/2, y - 15, 
                             text=f"${value}", 
                             font=("Segoe UI", 10, "bold"), 
                             fill="#2c3e50")
    
    def create_product_list(self, parent):
        list_frame = tk.Frame(parent, bg="white")
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Productos de ejemplo con stock bajo
        low_stock_products = [p for p in self.products if p.get('stock', 0) < 20][:5]
        
        if not low_stock_products:
            low_stock_products = [
                {"name": "Cuaderno 100 hojas", "stock": 12, "status": "Bajo"},
                {"name": "Tijeras escolares", "stock": 8, "status": "Crítico"},
                {"name": "Regla 30cm", "stock": 15, "status": "Bajo"},
                {"name": "Pegamento líquido", "stock": 18, "status": "Bajo"},
                {"name": "Corrector líquido", "stock": 5, "status": "Crítico"}
            ]
        
        for product in low_stock_products:
            self.create_product_item(list_frame, product)
    
    def create_product_item(self, parent, product):
        item = tk.Frame(parent, bg="white")
        item.pack(fill="x", pady=8)
        
        # Icono del producto
        icon_frame = tk.Frame(item, bg="#f5f6fa", width=45, height=45)
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        icon = tk.Label(icon_frame, text="📦", font=("Segoe UI", 18), 
                       bg="#f5f6fa")
        icon.place(relx=0.5, rely=0.5, anchor="center")
        
        # Info del producto
        info = tk.Frame(item, bg="white")
        info.pack(side="left", fill="x", expand=True, padx=12)
        
        name = tk.Label(info, text=product.get('name', 'Producto'), 
                       font=("Segoe UI", 10, "bold"), 
                       bg="white", fg="#2c3e50", anchor="w")
        name.pack(anchor="w")
        
        stock = product.get('stock', 0)
        status_text = "Crítico" if stock < 10 else "Bajo"
        status_color = "#e74c3c" if stock < 10 else "#f39c12"
        
        status_label = tk.Label(info, text=f"Stock: {stock} - {status_text}", 
                               font=("Segoe UI", 9), 
                               bg="white", fg=status_color, anchor="w")
        status_label.pack(anchor="w")
        
        # Indicador de stock
        stock_indicator = tk.Frame(item, bg=status_color, width=4, height=45)
        stock_indicator.pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImprovedDashboard(root)
    root.mainloop()