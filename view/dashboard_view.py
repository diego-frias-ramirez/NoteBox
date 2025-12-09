"""
NoteBox - Vista del Dashboard Principal (Corregido)
Ubicación: view/dashboard_view.py
"""

import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from PIL import Image
import os

from components.base_view import BaseView
from model.report_model import ReportModel
from model.alert_model import AlertModel
from utils.logger import Logger
from utils.helpers import Helpers

class DashboardView(BaseView):
    """Vista del Dashboard Principal."""
    
    def __init__(self, user_data):
        self.inventory_summary = {}
        self.low_stock_products = []
        self.active_alerts = []
        self.category_data = []
        self.images = {}
        self.icon_refs = {}
        
        self.report_model = ReportModel()
        self.alert_model = AlertModel()
        
        # NO cargar datos aquí - se hará después de crear la UI
        
        super().__init__(
            user_data=user_data,
            page_id="dashboard",
            page_title="Dashboard Principal",
            page_subtitle="Bienvenido al sistema de gestión",
            defer_content_creation=True  # No crear contenido hasta que los datos estén listos
        )
        
        # Cargar datos de forma asíncrona DESPUÉS de crear la UI
        self.after(100, self.start_async_data_load)
    
    def load_data(self):
        """Carga datos desde la base de datos."""
        try:
            self.inventory_summary = self.report_model.get_inventory_summary() or {}
            self.low_stock_products = self.report_model.get_low_stock_products() or []
            self.active_alerts = self.alert_model.get_active_alerts() or []
            self.category_data = self.report_model.get_products_by_category() or []
            Logger.info("Datos del dashboard cargados", "DASHBOARD")
        except Exception as e:
            Logger.error(f"Error cargando datos: {e}", "DASHBOARD")
    
    def start_async_data_load(self):
        """Inicia la carga asíncrona de datos."""
        self.show_loading("Cargando dashboard...")
        
        # Ejecutar carga en background
        self.run_background_task(
            task_func=self._load_data_background,
            callback_func=self._on_data_loaded,
            error_callback=self._on_data_load_error
        )
    
    def _load_data_background(self):
        """Función que se ejecuta en background thread para cargar datos."""
        try:
            inventory_summary = self.report_model.get_inventory_summary() or {}
            low_stock_products = self.report_model.get_low_stock_products() or []
            active_alerts = self.alert_model.get_active_alerts() or []
            category_data = self.report_model.get_products_by_category() or []
            
            return {
                'inventory_summary': inventory_summary,
                'low_stock_products': low_stock_products,
                'active_alerts': active_alerts,
                'category_data': category_data
            }
        except Exception as e:
            Logger.error(f"Error cargando datos en background: {e}", "DASHBOARD")
            raise
    
    def _on_data_loaded(self, data):
        """Callback que se ejecuta cuando los datos están listos."""
        self.inventory_summary = data['inventory_summary']
        self.low_stock_products = data['low_stock_products']
        self.active_alerts = data['active_alerts']
        self.category_data = data['category_data']
        
        # Actualizar la UI con los nuevos datos (sin recrear todo)
        self.update_content_with_data()
        
        # Ocultar loading
        self.hide_loading()
        Logger.info("Dashboard cargado exitosamente", "DASHBOARD")
    
    def _on_data_load_error(self, error):
        """Callback que se ejecuta si hay error al cargar datos."""
        Logger.error(f"Error al cargar dashboard: {error}", "DASHBOARD")
        self.hide_loading()
        # Mostrar mensaje de error al usuario
        try:
            from tkinter import messagebox
            messagebox.showerror("Error", "No se pudieron cargar los datos del dashboard.")
        except:
            pass
    
    def update_content_with_data(self):
        """Actualiza el contenido existente con los datos cargados."""
        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Recrear con datos reales
        self.create_content()
    
    def create_content(self):
        """Crea el contenido principal del dashboard (solo llamado después de cargar datos)."""
        # Banner de bienvenida
        self.create_welcome_banner()
        
        # Grid principal
        main_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_grid.pack(fill="both", expand=True, pady=(20, 0))
        
        # Columna izquierda
        left_col = ctk.CTkFrame(main_grid, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        self.create_stats_section(left_col)
        self.create_chart_section(left_col)
        
        # Columna derecha
        right_col = ctk.CTkFrame(main_grid, fg_color="transparent", width=300)
        right_col.pack(side="right", fill="y")
        right_col.pack_propagate(False)
        
        self.create_alerts_section(right_col)
    
    def create_welcome_banner(self):
        """Banner de bienvenida."""
        banner = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=20, height=150)
        banner.pack(fill="x", pady=(0, 0))
        banner.pack_propagate(False)
        
        content = ctk.CTkFrame(banner, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=35, pady=25)
        
        hour = datetime.now().hour
        greeting = "Buenos días" if hour < 12 else ("Buenas tardes" if hour < 18 else "Buenas noches")
        
        ctk.CTkLabel(
            content, text=f"Hola ! {greeting}",
            font=ctk.CTkFont(size=32, weight="bold"), text_color="#00B4D8"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            content, text=f"De nuevo {self.user_data.get('nombre', 'Usuario')}",
            font=ctk.CTkFont(size=26, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w", pady=(5, 0))
        
        # Imagen decorativa
        img_path = Helpers.get_asset_path('dashboard_banner', 'assets/images/banner.png')
        try:
            img = Image.open(img_path)
            img = img.resize((509, 113), Image.LANCZOS)
            self.images["banner"] = ctk.CTkImage(light_image=img, dark_image=img, size=(509, 113))
            ctk.CTkLabel(banner, image=self.images["banner"], text="").pack(side="right", padx=15)
        except:
            placeholder = ctk.CTkFrame(banner, fg_color="#F1F5F9", width=400, height=100, corner_radius=15)
            placeholder.pack(side="right", padx=15)
            placeholder.pack_propagate(False)
            ctk.CTkLabel(placeholder, text="🖼️", font=ctk.CTkFont(size=40), text_color="#94A3B8").place(relx=0.5, rely=0.5, anchor="center")
    
    def create_stats_section(self, parent):
        """Tarjetas de estadísticas en grid 2x2."""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 15))
        
        cards_frame.grid_columnconfigure((0, 1), weight=1)
        cards_frame.grid_rowconfigure((0, 1), weight=1)
        
        total = self.inventory_summary.get('total_productos', 0)
        disponibles = self.inventory_summary.get('productos_disponibles', 0)
        stock_bajo = self.inventory_summary.get('productos_stock_bajo', 0)
        agotados = self.inventory_summary.get('productos_agotados', 0)
        valor_total = self.inventory_summary.get('valor_total_inventario', 0)
        
        cards = [
            {
                "title": "Productos Totales",
                "value": f"{total:,}",
                "sub": f"↑ Disponibles: {disponibles}",
                "sub_color": "#10B981",
                "bg": "#FFFFFF",
                "icon": "products.png",
                "icon_bg": "#E0F7FA"
            },
            {
                "title": "Stock Bajo",
                "value": str(stock_bajo),
                "sub": "Requieren reabastecimiento",
                "sub_color": "#64748B",
                "bg": "#FFFFFF",
                "icon": "low_stock.png",
                "icon_bg": "#FEE2E2"
            },
            {
                "title": "Valor del Inventario",
                "value": Helpers.format_currency(valor_total),
                "sub": f"{total} productos registrados",
                "sub_color": "#E0F7FA",
                "bg": "#00B4D8",
                "icon": "money.png",
                "icon_bg": "#0096B4",
                "text": "#FFFFFF"
            },
            {
                "title": "Alertas Activas",
                "value": str(len(self.active_alerts)),
                "sub": f"Agotados: {agotados}",
                "sub_color": "#64748B",
                "bg": "#FFFFFF",
                "icon": "alert.png",
                "icon_bg": "#FEF3C7"
            }
        ]
        
        for i, c in enumerate(cards):
            card = self.create_stat_card(cards_frame, c)
            card.grid(row=i//2, column=i%2, sticky="nsew", padx=8, pady=8)
    
    def create_stat_card(self, parent, data):
        """Crea una tarjeta de estadística."""
        text_color = data.get("text", "#1E293B")
        is_highlight = data["bg"] == "#00B4D8"
        
        card = ctk.CTkFrame(parent, fg_color=data["bg"], corner_radius=15, height=125)
        card.pack_propagate(False)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header con título e icono
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header, text=data["title"], font=ctk.CTkFont(size=13),
            text_color="#E0F7FA" if is_highlight else "#64748B"
        ).pack(side="left")
        
        # Icono desde archivo
        icon_frame = ctk.CTkFrame(header, fg_color=data["icon_bg"], width=38, height=38, corner_radius=10)
        icon_frame.pack(side="right")
        icon_frame.pack_propagate(False)
        
        icon_path = os.path.join(self.base_path, "..", "assets", "icons", data["icon"])
        try:
            img = Image.open(icon_path)
            img = img.resize((20, 20), Image.LANCZOS)
            icon_img = ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
            self.icon_refs[data["icon"]] = icon_img
            ctk.CTkLabel(icon_frame, image=icon_img, text="").place(relx=0.5, rely=0.5, anchor="center")
        except:
            ctk.CTkLabel(icon_frame, text="•", font=ctk.CTkFont(size=16)).place(relx=0.5, rely=0.5, anchor="center")
        
        # Valor
        ctk.CTkLabel(
            inner, text=data["value"],
            font=ctk.CTkFont(size=26, weight="bold"), text_color=text_color
        ).pack(anchor="w", pady=(8, 3))
        
        # Subtítulo
        ctk.CTkLabel(
            inner, text=data["sub"],
            font=ctk.CTkFont(size=11), text_color=data["sub_color"]
        ).pack(anchor="w")
        
        return card
    
    def create_chart_section(self, parent):
        """Gráfico de barras con matplotlib."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        chart_card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15, height=280)
        chart_card.pack(fill="x", pady=(10, 0))
        chart_card.pack_propagate(False)
        
        ctk.CTkLabel(
            chart_card, text="Inventario por Categoría",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w", padx=25, pady=(20, 10))
        
        # Preparar datos reales
        if self.category_data:
            categories = [c.get('categoria', 'Sin cat.')[:12] for c in self.category_data[:5]]
            stocks = [int(c.get('total_unidades', 0) or 0) for c in self.category_data[:5]]
        else:
            categories, stocks = [], []
        
        # Si no hay datos
        if not categories or all(s == 0 for s in stocks):
            ctk.CTkLabel(
                chart_card, text="No hay datos para mostrar",
                font=ctk.CTkFont(size=12), text_color="#94A3B8"
            ).pack(expand=True)
            return
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#FFFFFF')
        
        # Barras
        bars = ax.bar(categories, stocks, color='#00B4D8', edgecolor='#00B4D8', width=0.6)
        
        # Estilo
        ax.set_ylabel('Unidades', fontsize=9, color='#64748B')
        ax.tick_params(axis='x', labelsize=8, colors='#64748B', rotation=15)
        ax.tick_params(axis='y', labelsize=8, colors='#64748B')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E2E8F0')
        ax.spines['bottom'].set_color('#E2E8F0')
        ax.grid(axis='y', color='#E2E8F0', linestyle='--', linewidth=0.5, alpha=0.7)
        
        # Valores sobre barras
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.annotate(f'{int(h)}', xy=(bar.get_x() + bar.get_width()/2, h),
                           xytext=(0, 3), textcoords="offset points",
                           ha='center', va='bottom', fontsize=8, color='#1E293B')
        
        plt.tight_layout()
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def create_alerts_section(self, parent):
        """Panel de alertas lateral."""
        panel = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        panel.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            panel, text="Últimas Alertas",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        # Contenedor de alertas (sin scroll)
        alerts_container = ctk.CTkFrame(panel, fg_color="transparent")
        alerts_container.pack(fill="x", padx=12, pady=(0, 10))
        
        # Mostrar máximo 5 alertas
        if self.low_stock_products:
            for p in self.low_stock_products[:5]:
                stock = p.get('stock', 0)
                alert_type = "danger" if stock == 0 else "warning"
                name = p.get('nombre', 'Producto')[:22]
                title = f"{'Agotado' if stock == 0 else 'Stock bajo'}: {name}"
                detail = f"Quedan {stock} unidades"
                self.create_alert_item(alerts_container, alert_type, title, detail)
        else:
            ctk.CTkLabel(
                alerts_container, text="✅ No hay alertas activas",
                font=ctk.CTkFont(size=12), text_color="#10B981"
            ).pack(pady=20)
        
        # Botón ver todas
        ctk.CTkButton(
            panel, text="Ver todas las alertas →",
            fg_color="transparent", text_color="#00B4D8",
            hover_color="#E0F7FA", font=ctk.CTkFont(size=12),
            command=lambda: self.navigate_to("inventario")
        ).pack(pady=(10, 20))
    
    def create_alert_item(self, parent, alert_type, title, detail):
        """Crea un item de alerta."""
        styles = {
            "warning": {"bg": "#FEF3C7", "icon": "alert.png"},
            "danger": {"bg": "#FEE2E2", "icon": "alert_yellow.png"},
            "info": {"bg": "#E0F2FE", "icon": "alert_info.png"}
        }
        style = styles.get(alert_type, styles["info"])
        
        item = ctk.CTkFrame(parent, fg_color=style["bg"], corner_radius=10, height=65)
        item.pack(fill="x", pady=4)
        item.pack_propagate(False)
        
        inner = ctk.CTkFrame(item, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=12, pady=10)
        
        # Icono desde archivo
        icon_path = os.path.join(self.base_path, "..", "assets", "icons", style["icon"])
        try:
            img = Image.open(icon_path)
            img = img.resize((18, 18), Image.LANCZOS)
            icon_img = ctk.CTkImage(light_image=img, dark_image=img, size=(18, 18))
            self.icon_refs[style["icon"]] = icon_img
            ctk.CTkLabel(inner, image=icon_img, text="").pack(side="left", padx=(0, 10))
        except:
            ctk.CTkLabel(inner, text="!", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(inner, fg_color="transparent")
        text_frame.pack(side="left", fill="y")
        
        ctk.CTkLabel(text_frame, text=title, font=ctk.CTkFont(size=11, weight="bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=detail, font=ctk.CTkFont(size=10), text_color="#64748B").pack(anchor="w")
    
    def navigate_to(self, page_id):
        """Navega a otra página."""
        self.destroy()
        
        if page_id == "dashboard":
            DashboardView(self.user_data).run()
        elif page_id == "inventario":
            from view.inventory_view import InventoryView
            InventoryView(self.user_data).run()
        elif page_id == "movimientos":
            from view.movements_view import MovementsView
            MovementsView(self.user_data).run()
        elif page_id == "reportes":
            from view.reports_view import ReportsView
            ReportsView(self.user_data).run()
        elif page_id == "usuarios":
            from view.users_view import UsersView
            UsersView(self.user_data).run()
        elif page_id == "configuracion":
            from view.settings_view import SettingsView
            SettingsView(self.user_data).run()
        elif page_id == "ayuda":
            from view.help_view import HelpView
            HelpView(self.user_data).run()
    
    def get_notification_count(self):
        return len(self.active_alerts)

