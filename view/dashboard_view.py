"""
NoteBox - Vista del Dashboard Principal
Ubicación: view/dashboard_view.py
"""

import customtkinter as ctk
from components.base_view import BaseView
from model.report_model import ReportModel
from model.alert_model import AlertModel
from utils.logger import Logger
from PIL import Image
import os
from datetime import datetime  # Añadido para el saludo

class DashboardView(BaseView):
    """Vista del Dashboard Principal."""
    
    def __init__(self, user_data):
        # === 1. Inicializar todas las variables de instancia PRIMERO ===
        self.inventory_summary = {}
        self.low_stock_products = []
        self.active_alerts = []
        self.top_products = []
        self.stat_icons = {}  # <-- ¡ESTA LÍNEA ES CRÍTICA!
        self.welcome_icon_img = None
        
        # === 2. Instanciar modelos ===
        self.report_model = ReportModel()
        self.alert_model = AlertModel()
        
        # === 3. Cargar los datos ===
        self.load_dashboard_data()
        
        # === 4. Llamar al constructor de la clase base AL FINAL ===
        super().__init__(
            user_data=user_data,
            page_id="dashboard",
            page_title="Dashboard Principal",
            page_subtitle="Resumen del inventario y alertas"
        )
    
    def load_dashboard_data(self):
        """Carga los datos del dashboard desde los modelos."""
        try:
            self.inventory_summary = self.report_model.get_inventory_summary()
            self.low_stock_products = self.report_model.get_low_stock_products()
            self.active_alerts = self.alert_model.get_active_alerts()
            self.top_products = self.report_model.get_top_products(limit=5)
            Logger.info("Datos del dashboard cargados correctamente", "DASHBOARD_VIEW")
        except Exception as e:
            Logger.error(f"Error al cargar datos del dashboard: {e}", "DASHBOARD_VIEW")
            self.inventory_summary = {}
            self.low_stock_products = []
            self.active_alerts = []
            self.top_products = []
    
    def create_content(self):
        """Crea el contenido específico del dashboard."""
        self.create_welcome_banner()
        self.create_stats_section()
        self.create_quick_alerts_section()
        self.create_low_stock_section()
        self.create_top_products_section()
    
    def create_welcome_banner(self):
        """Crea el banner de bienvenida."""
        banner_frame = ctk.CTkFrame(self.content_frame, fg_color="#F0F9FF", corner_radius=15, height=120)
        banner_frame.pack(fill="x", pady=(0, 20), padx=0)
        banner_frame.pack_propagate(False)
        
        banner_content = ctk.CTkFrame(banner_frame, fg_color="transparent")
        banner_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Obtener saludo según la hora (SIN Helpers.get_greeting_message)
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Buenos días"
        elif hour < 18:
            greeting = "Buenas tardes"
        else:
            greeting = "Buenas noches"
        
        text_frame = ctk.CTkFrame(banner_content, fg_color="transparent")
        text_frame.pack(side="left", fill="y", expand=False)
        
        hello_label = ctk.CTkLabel(text_frame, text=f"{greeting},", font=ctk.CTkFont(size=24, weight="bold"), text_color="#0891B2")
        hello_label.pack(anchor="w")
        
        name_label = ctk.CTkLabel(text_frame, text=f"{self.user_data.get('nombre', 'Usuario')}!", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1E293B")
        name_label.pack(anchor="w", pady=(5, 0))
        
        subtitle_label = ctk.CTkLabel(text_frame, text="Aquí está el resumen de tu inventario.", font=ctk.CTkFont(size=12), text_color="#64748B")
        subtitle_label.pack(anchor="w", pady=(2, 0))
        
        # Ícono de bienvenida
        icon_path = os.path.join(self.base_path, "..", "assets", "icons", "dashboard.png")
        try:
            img = Image.open(icon_path)
            img = img.resize((80, 80), Image.LANCZOS)
            self.welcome_icon_img = ctk.CTkImage(light_image=img, dark_image=img)
            icon_label = ctk.CTkLabel(banner_content, image=self.welcome_icon_img, text="")
            icon_label.pack(side="right", padx=(0, 20))
        except FileNotFoundError:
            pass
    
    def create_stats_section(self):
        """Crea la sección de estadísticas."""
        title = ctk.CTkLabel(self.content_frame, text="Resumen General del Inventario", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        title.pack(fill="x", pady=(10, 10))
        
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats_data = [
            {"label": "Total de Productos", "value": self.inventory_summary.get('total_productos', 0), "color": "#E0F2FE", "icon": "dashboard.png"},
            {"label": "Disponibles", "value": self.inventory_summary.get('productos_disponibles', 0), "color": "#DCFCE7", "icon": "inventory.png"},
            {"label": "Stock Bajo", "value": self.inventory_summary.get('productos_stock_bajo', 0), "color": "#FEF3C7", "icon": "movements.png"},
            {"label": "Agotados", "value": self.inventory_summary.get('productos_agotados', 0), "color": "#FFE4E6", "icon": "reports.png"}
        ]
        
        for i, stat in enumerate(stats_data):
            card = self.create_stat_card(stats_frame, stat)
            card.grid(row=0, column=i, sticky="ew", padx=5)
            stats_frame.grid_columnconfigure(i, weight=1)
    
    def create_stat_card(self, parent, stat_data):
        """Crea una tarjeta de estadística."""
        card = ctk.CTkFrame(parent, fg_color=stat_data["color"], corner_radius=10, width=200, height=100)
        card.grid_propagate(False)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Cargar ícono
        icon_path = os.path.join(self.base_path, "..", "assets", "icons", stat_data["icon"])
        try:
            img = Image.open(icon_path)
            img = img.resize((24, 24), Image.LANCZOS)
            icon_img = ctk.CTkImage(light_image=img, dark_image=img)
            # Ahora SÍ existe self.stat_icons
            self.stat_icons[stat_data["icon"]] = icon_img
            ctk.CTkLabel(inner, image=icon_img, text="").pack(anchor="w")
        except FileNotFoundError:
            pass
        
        ctk.CTkLabel(inner, text=str(stat_data["value"]), font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(inner, text=stat_data["label"], font=ctk.CTkFont(size=12)).pack(anchor="w")
        
        return card
    
    def create_quick_alerts_section(self):
        """Crea la sección de alertas rápidas."""
        title = ctk.CTkLabel(self.content_frame, text="Alertas Rápidas", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        title.pack(fill="x", pady=(10, 10))
        
        alerts_frame = ctk.CTkFrame(self.content_frame, fg_color="#FEEBEE", corner_radius=10)
        alerts_frame.pack(fill="x", pady=(0, 20))
        
        if self.active_alerts:
            for alert in self.active_alerts[:3]:
                text = f"[{alert['tipo']}] {alert['descripcion']}"
                ctk.CTkLabel(alerts_frame, text=text, font=ctk.CTkFont(size=12), text_color="#B91C1C", anchor="w", padx=15, pady=10).pack(fill="x", padx=10, pady=2, anchor="w")
        else:
            ctk.CTkLabel(alerts_frame, text="No hay alertas activas.", font=ctk.CTkFont(size=12), text_color="#10B981", anchor="w", padx=15, pady=10).pack(fill="x", padx=10, pady=10)
    
    def create_low_stock_section(self):
        """Crea la sección de productos con stock bajo."""
        title = ctk.CTkLabel(self.content_frame, text="Productos con Stock Bajo", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        title.pack(fill="x", pady=(10, 10))
        
        if self.low_stock_products:
            header = ctk.CTkFrame(self.content_frame, fg_color="#F1F5F9", corner_radius=5)
            header.pack(fill="x", pady=(0, 5))
            for i, h in enumerate(["Código", "Nombre", "Categoría", "Stock", "Mínimo"]):
                ctk.CTkLabel(header, text=h, font=ctk.CTkFont(size=12, weight="bold"), width=150, anchor="w", padx=10).grid(row=0, column=i, sticky="w", padx=2)
            
            for i, p in enumerate(self.low_stock_products[:5]):
                color = "#FFFFFF" if i % 2 == 0 else "#F8FAFC"
                row = ctk.CTkFrame(self.content_frame, fg_color=color, height=30, corner_radius=0)
                row.pack(fill="x", pady=1)
                row.pack_propagate(False)
                values = [p.get('codigo', 'N/A'), p.get('nombre', 'N/A'), p.get('categoria_nombre', 'N/A'), str(p.get('stock', 0)), str(p.get('stock_minimo', 0))]
                for j, v in enumerate(values):
                    ctk.CTkLabel(row, text=v, font=ctk.CTkFont(size=12), width=150, anchor="w", padx=10).grid(row=0, column=j, sticky="w", padx=2)
        else:
            ctk.CTkLabel(self.content_frame, text="No hay productos con stock bajo.", font=ctk.CTkFont(size=12), text_color="#10B981", anchor="w", padx=15, pady=10).pack(fill="x", pady=10)
    
    def create_top_products_section(self):
        """Crea la sección de productos top."""
        title = ctk.CTkLabel(self.content_frame, text="Productos Más Valiosos", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        title.pack(fill="x", pady=(10, 10))
        
        if self.top_products:
            header = ctk.CTkFrame(self.content_frame, fg_color="#F1F5F9", corner_radius=5)
            header.pack(fill="x", pady=(0, 5))
            for i, h in enumerate(["Código", "Nombre", "Categoría", "Stock", "Precio", "Valor"]):
                ctk.CTkLabel(header, text=h, font=ctk.CTkFont(size=12, weight="bold"), width=120, anchor="w", padx=10).grid(row=0, column=i, sticky="w", padx=2)
            
            for i, p in enumerate(self.top_products):
                color = "#FFFFFF" if i % 2 == 0 else "#F8FAFC"
                row = ctk.CTkFrame(self.content_frame, fg_color=color, height=30, corner_radius=0)
                row.pack(fill="x", pady=1)
                row.pack_propagate(False)
                from utils.helpers import Helpers
                values = [
                    p.get('codigo', 'N/A'),
                    p.get('nombre', 'N/A'),
                    p.get('categoria_nombre', 'N/A'),
                    str(p.get('stock', 0)),
                    Helpers.format_currency(p.get('precio', 0)),
                    Helpers.format_currency(p.get('valor_total', 0))
                ]
                for j, v in enumerate(values):
                    ctk.CTkLabel(row, text=v, font=ctk.CTkFont(size=12), width=120, anchor="w", padx=10).grid(row=0, column=j, sticky="w", padx=2)
        else:
            ctk.CTkLabel(self.content_frame, text="No hay datos disponibles.", font=ctk.CTkFont(size=12), text_color="#6B7280", anchor="w", padx=15, pady=10).pack(fill="x", pady=10)

    def get_notification_count(self):
        """Obtiene el número de notificaciones."""
        return len(self.active_alerts)