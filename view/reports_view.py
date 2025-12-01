"""
NoteBox - Vista del Módulo de Reportes (LAYOUT CORREGIDO SEGÚN FIGMA)
Ubicación: view/reports_view.py
"""

import customtkinter as ctk
from PIL import Image
import os
from datetime import datetime

from components.base_view import BaseView
from controller.reports_controller import ReportsController
from utils.logger import Logger
from utils.helpers import Helpers

class ReportsView(BaseView):
    """Vista del Módulo de Reportes."""

    def __init__(self, user_data):
        self.images = {}
        self.icon_refs = {}
        
        # Instancia del controlador
        self.controller = ReportsController(user_data)
        
        # Cargar datos iniciales
        self.metrics = {}
        self.low_rotation_products = []
        self.category_data = ([], [])
        self.inventory_evolution = ([], [])
        self.load_data()
        
        # Llamar al constructor de la clase base
        super().__init__(
            user_data=user_data,
            page_id="reportes",
            page_title="Generación de Reportes",
            page_subtitle="Visualizar y exportar información del inventario"
        )

    def load_data(self):
        """Carga datos desde el controlador."""
        try:
            self.metrics = self.controller.get_inventory_metrics()
            self.low_rotation_products = self.controller.get_low_rotation_products(limit=5)
            self.category_data = self.controller.get_category_distribution()
            self.inventory_evolution = self.controller.get_inventory_evolution(months=6)
            Logger.info("Datos de reportes cargados correctamente", "REPORTS_VIEW")
        except Exception as e:
            Logger.error(f"Error cargando datos de reportes: {e}", "REPORTS_VIEW")

    def create_content(self):
        """Crea el contenido específico del módulo de reportes (SEGÚN FIGMA)."""
        content_frame = self.content_frame
        
        # 1. SECCIÓN SUPERIOR: Generación de reportes
        self.create_report_generator(content_frame)
        
        # 2. FILA 1: Gráfico Evolución (izq) + Gráfico Categorías (der)
        charts_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        charts_row.pack(fill="x", pady=(20, 15))
        
        # Gráfico de Evolución (50%)
        evolution_frame = ctk.CTkFrame(charts_row, fg_color="transparent")
        evolution_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.create_evolution_chart(evolution_frame)
        
        # Gráfico de Categorías (50%)
        category_frame = ctk.CTkFrame(charts_row, fg_color="transparent")
        category_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))
        self.create_category_chart(category_frame)
        
        # 3. FILA 2: 4 Tarjetas de métricas (ancho completo)
        self.create_metrics_cards(content_frame)
        
        # 4. FILA 3: Tabla de Baja Rotación (izq) + Imagen decorativa (der)
        bottom_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_row.pack(fill="both", expand=True, pady=(15, 0))
        
        # Tabla de productos (65%)
        table_container = ctk.CTkFrame(bottom_row, fg_color="transparent")
        table_container.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.create_low_rotation_table(table_container)
        
        # Imagen decorativa (35%)
        image_container = ctk.CTkFrame(bottom_row, fg_color="transparent", width=350)
        image_container.pack(side="right", fill="y")
        image_container.pack_propagate(False)
        self.create_decorative_image(image_container)

    def create_report_generator(self, parent):
        """Crea la sección de generación de reportes."""
        generator_card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15, height=100)
        generator_card.pack(fill="x", pady=(0, 0))
        generator_card.pack_propagate(False)
        
        inner = ctk.CTkFrame(generator_card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Título y descripción (izquierda)
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            header, text="Generar Reportes",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header, text="Exporte datos en diferentes formatos",
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(anchor="w", pady=(2, 0))
        
        # Filtros de fecha (centro)
        filters_frame = ctk.CTkFrame(inner, fg_color="transparent")
        filters_frame.pack(side="left", fill="y", padx=(50, 20))
        
        date_inputs = ctk.CTkFrame(filters_frame, fg_color="transparent")
        date_inputs.pack()

        # Start date with calendar icon
        start_container = ctk.CTkFrame(date_inputs, fg_color="transparent")
        start_container.pack(side="left", padx=(0, 8))

        self.start_date_entry = ctk.CTkEntry(
            start_container, placeholder_text="📅 Fecha inicio",
            width=120, height=38, font=ctk.CTkFont(size=12),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8
        )
        self.start_date_entry.pack(side="left")

        ctk.CTkButton(
            start_container, text="📅", width=38, height=38,
            fg_color="transparent", text_color="#475569",
            hover_color="#F1F5F9", corner_radius=8,
            command=lambda: self.open_calendar_for(self.start_date_entry)
        ).pack(side="left", padx=(6, 0))

        ctk.CTkLabel(
            date_inputs, text="—",
            font=ctk.CTkFont(size=14), text_color="#94A3B8"
        ).pack(side="left", padx=6)

        # End date with calendar icon
        end_container = ctk.CTkFrame(date_inputs, fg_color="transparent")
        end_container.pack(side="left", padx=(8, 0))

        self.end_date_entry = ctk.CTkEntry(
            end_container, placeholder_text="📅 Fecha fin",
            width=120, height=38, font=ctk.CTkFont(size=12),
            fg_color="#F8FAFC", border_color="#E2E8F0", border_width=1,
            corner_radius=8
        )
        self.end_date_entry.pack(side="left")

        ctk.CTkButton(
            end_container, text="📅", width=38, height=38,
            fg_color="transparent", text_color="#475569",
            hover_color="#F1F5F9", corner_radius=8,
            command=lambda: self.open_calendar_for(self.end_date_entry)
        ).pack(side="left", padx=(6, 0))
        
        # Botones de exportación (derecha)
        buttons_frame = ctk.CTkFrame(inner, fg_color="transparent")
        buttons_frame.pack(side="right", fill="y")
        
        pdf_btn = ctk.CTkButton(
            buttons_frame, text="📄 PDF", width=90, height=38,
            font=ctk.CTkFont(size=13, weight="bold"), 
            fg_color="#EF4444", text_color="#FFFFFF", 
            hover_color="#DC2626", corner_radius=8,
            command=lambda: self.export_report("pdf")
        )
        pdf_btn.pack(side="left", padx=(0, 10))
        
        excel_btn = ctk.CTkButton(
            buttons_frame, text="📊 Excel", width=90, height=38,
            font=ctk.CTkFont(size=13, weight="bold"), 
            fg_color="#10B981", text_color="#FFFFFF", 
            hover_color="#059669", corner_radius=8,
            command=lambda: self.export_report("excel")
        )
        excel_btn.pack(side="left")


    def open_calendar_for(self, entry_widget):
        """Abre un calendario visual y coloca la fecha seleccionada en el campo dado."""
        try:
            from tkcalendar import Calendar  # type: ignore
            has_tkcalendar = True
        except Exception:
            has_tkcalendar = False

        dialog = ctk.CTkToplevel(self)
        dialog.title("Seleccionar fecha")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color="#FFFFFF")

        dialog.update_idletasks()
        w, h = 320, 320
        x = self.winfo_x() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")

        inner = ctk.CTkFrame(dialog, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(inner, text="Seleccione una fecha:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#1E293B").pack(anchor="w", pady=(0, 10))

        if has_tkcalendar:
            cal = Calendar(inner, date_pattern='dd/MM/yyyy', selectmode='day')
            cal.pack(pady=10)
        else:
            cal = None
            ctk.CTkLabel(inner, text="(Para un selector visual instala 'tkcalendar')", font=ctk.CTkFont(size=10), text_color="#94A3B8").pack(anchor="w", pady=(8, 0))

        def on_select():
            if cal:
                date_str = cal.get_date()
            else:
                date_str = datetime.now().strftime('%d/%m/%Y')
            entry_widget.delete(0, "end")
            entry_widget.insert(0, date_str)
            dialog.destroy()

        ctk.CTkButton(inner, text="Seleccionar", width=120, command=on_select, fg_color="#0EA5A4", text_color="#FFFFFF").pack(pady=(18, 0))
        ctk.CTkButton(inner, text="Cancelar", width=120, command=dialog.destroy, fg_color="#F1F5F9", text_color="#475569").pack(pady=(8, 0))

    def show_date_picker_dialog(self, format_type):
        """Muestra un diálogo (agenda) para seleccionar fecha inicio/fin.

        Usa `tkcalendar.DateEntry` si está disponible. Si no, muestra
        campos `CTkEntry` para que el usuario ingrese manualmente.
        """
        try:
            from tkcalendar import DateEntry  # type: ignore
            has_tkcalendar = True
        except Exception:
            has_tkcalendar = False

        dialog = ctk.CTkToplevel(self)
        dialog.title("Seleccionar rango de fechas")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color="#FFFFFF")

        dialog.update_idletasks()
        w, h = 420, 220
        x = self.winfo_x() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")

        inner = ctk.CTkFrame(dialog, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(inner, text="Seleccione Fecha Inicio y Fecha Fin:",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#1E293B").pack(anchor="w")

        fields = ctk.CTkFrame(inner, fg_color="transparent")
        fields.pack(fill="x", pady=(12, 8))

        # Fecha inicio
        ctk.CTkLabel(fields, text="Fecha inicio:", font=ctk.CTkFont(size=11), text_color="#64748B").grid(row=0, column=0, sticky="w")
        # Fecha fin
        ctk.CTkLabel(fields, text="Fecha fin:", font=ctk.CTkFont(size=11), text_color="#64748B").grid(row=1, column=0, sticky="w", pady=(8, 0))

        if has_tkcalendar:
            # Mostrar dos calendarios visuales (inicio / fin)
            try:
                from tkcalendar import Calendar  # type: ignore

                cal_container = ctk.CTkFrame(fields, fg_color="transparent")
                cal_container.grid(row=0, column=1, rowspan=2, padx=(8, 0))

                left_frame = ctk.CTkFrame(cal_container, fg_color="transparent")
                left_frame.pack(side="left", padx=(0, 6))
                right_frame = ctk.CTkFrame(cal_container, fg_color="transparent")
                right_frame.pack(side="left")

                start_widget = Calendar(left_frame, date_pattern='dd/MM/yyyy', selectmode='day')
                start_widget.pack()
                end_widget = Calendar(right_frame, date_pattern='dd/MM/yyyy', selectmode='day')
                end_widget.pack()

            except Exception:
                # Si por alguna razón Calendar falla, volver a usar DateEntry
                start_widget = DateEntry(fields, date_pattern='dd/MM/yyyy')
                end_widget = DateEntry(fields, date_pattern='dd/MM/yyyy')
        else:
            start_widget = ctk.CTkEntry(fields, placeholder_text="DD/MM/YYYY", width=180)
            end_widget = ctk.CTkEntry(fields, placeholder_text="DD/MM/YYYY", width=180)

        start_widget.grid(row=0, column=1, padx=(8, 0))
        end_widget.grid(row=1, column=1, padx=(8, 0), pady=(8, 0))

        # Prellenar con valores actuales o hoy
        try:
            cur_start = self.start_date_entry.get().strip()
            cur_end = self.end_date_entry.get().strip()
        except Exception:
            cur_start = cur_end = ""

        # Prellenar widgets: soportar tanto DateEntry/Entry como Calendar
        def _set_widget_date(widget, date_str):
            if not date_str:
                return
            try:
                # Para widgets tipo Entry / DateEntry
                widget.delete(0, 'end')
                widget.insert(0, date_str)
            except Exception:
                try:
                    # Para tkcalendar.Calendar
                    from datetime import datetime as _dt
                    d = _dt.strptime(date_str, '%d/%m/%Y').date()
                    if hasattr(widget, 'selection_set'):
                        widget.selection_set(d)
                    elif hasattr(widget, 'set_date'):
                        widget.set_date(d)
                except Exception:
                    pass

        _set_widget_date(start_widget, cur_start)
        _set_widget_date(end_widget, cur_end)

        # Formatos (PDF / Excel)
        formats_frame = ctk.CTkFrame(inner, fg_color="transparent")
        formats_frame.pack(fill="x", pady=(6, 0))

        pdf_var = ctk.BooleanVar(value=(format_type == "pdf" or format_type is None))
        excel_var = ctk.BooleanVar(value=(format_type == "excel" or format_type is None))

        ctk.CTkCheckBox(formats_frame, text="Exportar PDF", variable=pdf_var).pack(side="left", padx=(0, 12))
        ctk.CTkCheckBox(formats_frame, text="Exportar Excel", variable=excel_var).pack(side="left")

        # Botones
        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.pack(fill="x", pady=(14, 0))

        def _get_widget_date(widget):
            try:
                return widget.get().strip()
            except Exception:
                try:
                    return widget.get_date()
                except Exception:
                    try:
                        # Calendar
                        return widget.get_date()
                    except Exception:
                        return ''


        def on_ok():
            s = _get_widget_date(start_widget) or ""
            e = _get_widget_date(end_widget) or ""

            # Setear en los campos visibles para mantener compatibilidad
            try:
                self.start_date_entry.delete(0, "end")
                self.start_date_entry.insert(0, s)
                self.end_date_entry.delete(0, "end")
                self.end_date_entry.insert(0, e)
            except Exception:
                pass

            # Validar selección de formato
            selected_pdf = pdf_var.get()
            selected_excel = excel_var.get()

            if not selected_pdf and not selected_excel:
                self.show_message("Selecciona al menos un formato (PDF y/o Excel)", "warning")
                return

            dialog.destroy()

            # Llamar al exportador con las fechas ya en los campos para cada formato seleccionado
            if selected_pdf:
                self.export_report("pdf")
            if selected_excel:
                self.export_report("excel")

        def on_cancel():
            dialog.destroy()

        ctk.CTkButton(btns, text="Cancelar", width=120, command=on_cancel,
                      fg_color="#F1F5F9", text_color="#475569").pack(side="left")
        ctk.CTkButton(btns, text="Generar", width=120, command=on_ok,
                      fg_color="#0EA5A4", text_color="#FFFFFF").pack(side="right")

        if not has_tkcalendar:
            # Si no hay tkcalendar, mostrar nota para instalar (no obligatorio)
            ctk.CTkLabel(inner, text="(Para un selector visual instala 'tkcalendar')",
                         font=ctk.CTkFont(size=10), text_color="#94A3B8").pack(anchor="w", pady=(8, 0))

    def create_evolution_chart(self, parent):
        """Crea el gráfico de evolución del inventario."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        chart_card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15, height=300)
        chart_card.pack(fill="both", expand=True)
        chart_card.pack_propagate(False)
        
        # Header
        ctk.CTkLabel(
            chart_card, text="Evolución del Inventario",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w", padx=25, pady=(20, 10))
        
        # Obtener datos
        months, values = self.inventory_evolution
        
        if not months or not values:
            ctk.CTkLabel(
                chart_card, text="No hay datos disponibles",
                font=ctk.CTkFont(size=13), text_color="#94A3B8"
            ).pack(expand=True)
            return
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(6.5, 2.8), dpi=85)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#FFFFFF')
        
        # Línea con marcadores
        ax.plot(months, values, 
                color='#00B4D8', linewidth=2.5, 
                marker='o', markersize=9, 
                markerfacecolor='#00B4D8', 
                markeredgewidth=0,
                zorder=3)
        
        # Estilo
        ax.set_ylabel('Valor (Miles $)', fontsize=10, color='#64748B', fontweight='500')
        ax.tick_params(axis='x', labelsize=10, colors='#64748B', length=0)
        ax.tick_params(axis='y', labelsize=10, colors='#64748B', length=0)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E2E8F0')
        ax.spines['left'].set_linewidth(1)
        ax.spines['bottom'].set_color('#E2E8F0')
        ax.spines['bottom'].set_linewidth(1)
        
        ax.grid(axis='y', color='#F1F5F9', linestyle='-', linewidth=1.2, zorder=0)
        ax.set_axisbelow(True)
        ax.margins(x=0.05)
        
        plt.tight_layout(pad=1.5)
        
        # Integrar
        canvas = FigureCanvasTkAgg(fig, chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def create_category_chart(self, parent):
        """Crea el gráfico de distribución por categoría."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        chart_card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15, height=300)
        chart_card.pack(fill="both", expand=True)
        chart_card.pack_propagate(False)
        
        # Header
        ctk.CTkLabel(
            chart_card, text="Distribución por Categoría",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w", padx=25, pady=(20, 10))
        
        # Obtener datos
        sizes, labels = self.category_data
        
        if not sizes or not labels:
            ctk.CTkLabel(
                chart_card, text="No hay datos disponibles",
                font=ctk.CTkFont(size=13), text_color="#94A3B8"
            ).pack(expand=True)
            return
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(6, 2.8), dpi=85)
        fig.patch.set_facecolor('#FFFFFF')
        
        # Colores del diseño de Figma
        colors = ['#00B4D8', '#90E0EF', '#F59E0B', '#8B5A3C']
        
        # Gráfico de pastel
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.0f%%',
            startangle=90, 
            colors=colors[:len(sizes)],
            textprops={'fontsize': 10, 'color': '#1E293B', 'weight': '500'},
            wedgeprops={'edgecolor': '#FFFFFF', 'linewidth': 2.5}
        )
        
        # Estilo de porcentajes
        for autotext in autotexts:
            autotext.set_color('#FFFFFF')
            autotext.set_fontsize(11)
            autotext.set_weight('bold')
        
        # Estilo de etiquetas
        for text in texts:
            text.set_fontsize(9)
            text.set_color('#64748B')
        
        ax.axis('equal')
        plt.tight_layout(pad=1)
        
        # Integrar
        canvas = FigureCanvasTkAgg(fig, chart_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def create_metrics_cards(self, parent):
        """Crea las 4 tarjetas de métricas (ANCHO COMPLETO)."""
        cards_container = ctk.CTkFrame(parent, fg_color="transparent", height=130)
        cards_container.pack(fill="x", pady=(0, 15))
        cards_container.pack_propagate(False)
        
        cards_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Obtener datos reales
        valor_total = self.metrics.get('valor_total', '$0')
        rotacion = self.metrics.get('rotacion', '0x')
        cobertura = self.metrics.get('cobertura', '0 días')
        sin_rotacion = self.metrics.get('sin_rotacion', 0)
        
        cards_data = [
            {
                "title": "Valor Total",
                "value": valor_total,
                "subtitle": "↑ 8.5%",
                "subtitle_color": "#10B981",
                "icon": "📦",
                "icon_bg": "#E0F7FA"
            },
            {
                "title": "Rotación",
                "value": rotacion,
                "subtitle": "Mensual",
                "subtitle_color": "#64748B",
                "icon": "📈",
                "icon_bg": "#D1FAE5"
            },
            {
                "title": "Cobertura",
                "value": cobertura,
                "subtitle": "Promedio",
                "subtitle_color": "#64748B",
                "icon": "📅",
                "icon_bg": "#FEF3C7"
            },
            {
                "title": "Sin Rotac.",
                "value": str(sin_rotacion),
                "subtitle": "+30 días",
                "subtitle_color": "#EF4444",
                "icon": "📉",
                "icon_bg": "#FEE2E2"
            }
        ]
        
        for i, data in enumerate(cards_data):
            card = self.create_metric_card(cards_container, data)
            card.grid(row=0, column=i, sticky="nsew", padx=6, pady=0)

    def create_metric_card(self, parent, data):
        """Crea una tarjeta de métrica individual."""
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=12)
        card.pack_propagate(False)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=18)
        
        # Header con título e icono
        header = ctk.CTkFrame(inner, fg_color="transparent", height=40)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Título a la izquierda
        ctk.CTkLabel(
            header, text=data["title"],
            font=ctk.CTkFont(size=12), text_color="#64748B"
        ).pack(side="left", anchor="w")
        
        # Icono a la derecha
        icon_frame = ctk.CTkFrame(header, fg_color=data["icon_bg"], width=40, height=40, corner_radius=10)
        icon_frame.pack(side="right")
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame, text=data["icon"], font=ctk.CTkFont(size=18)
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Valor principal
        ctk.CTkLabel(
            inner, text=data["value"],
            font=ctk.CTkFont(size=26, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w", pady=(5, 2))
        
        # Subtítulo
        ctk.CTkLabel(
            inner, text=data["subtitle"],
            font=ctk.CTkFont(size=11, weight="bold" if "↑" in data["subtitle"] or "↓" in data["subtitle"] else "normal"), 
            text_color=data["subtitle_color"]
        ).pack(anchor="w")
        
        return card

    def create_low_rotation_table(self, parent):
        """Crea la tabla de productos de baja rotación."""
        table_card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15)
        table_card.pack(fill="both", expand=True)
        
        # Header
        header_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))
        
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(side="left")
        
        ctk.CTkLabel(
            title_container, text="Productos de Baja Rotación",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_container, text="Productos sin movimiento en los últimos 30 días",
            font=ctk.CTkFont(size=11), text_color="#64748B"
        ).pack(anchor="w", pady=(2, 0))
        
        # Encabezados
        headers_frame = ctk.CTkFrame(table_card, fg_color="#F8FAFC", height=45)
        headers_frame.pack(fill="x", padx=20, pady=(5, 0))
        headers_frame.pack_propagate(False)
        
        headers_container = ctk.CTkFrame(headers_frame, fg_color="transparent")
        headers_container.pack(fill="both", expand=True, padx=12, pady=10)
        
        headers = ["Producto", "Días sin Movimiento", "Stock Actual", "Estado"]
        widths = [0.3, 0.25, 0.2, 0.25]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                headers_container, text=header,
                font=ctk.CTkFont(size=11, weight="bold"), 
                text_color="#64748B", anchor="w"
            ).place(relx=sum(widths[:i]), rely=0.5, anchor="w", relwidth=width)
        
        # Contenedor de filas
        rows_container = ctk.CTkScrollableFrame(
            table_card, fg_color="transparent",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        rows_container.pack(fill="both", expand=True, padx=20, pady=(5, 15))
        
        # Agregar productos
        if self.low_rotation_products:
            for product in self.low_rotation_products:
                self.create_product_row(rows_container, product)
        else:
            ctk.CTkLabel(
                rows_container, text="✅ No hay productos de baja rotación",
                font=ctk.CTkFont(size=12), text_color="#10B981"
            ).pack(pady=40)
        
        # Botón ver más
        btn_frame = ctk.CTkFrame(table_card, fg_color="transparent", height=45)
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        btn_frame.pack_propagate(False)
        
        ctk.CTkButton(
            btn_frame, text="Ver informe completo →",
            fg_color="transparent", text_color="#00B4D8",
            hover_color="#E0F7FA", font=ctk.CTkFont(size=12),
            height=30, command=self.show_full_report
        ).pack(anchor="center")

    def create_product_row(self, parent, product):
        """Crea una fila de producto."""
        row_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", height=60, corner_radius=8)
        row_frame.pack(fill="x", pady=3)
        row_frame.pack_propagate(False)
        
        inner = ctk.CTkFrame(row_frame, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=12, pady=10)
        
        widths = [0.3, 0.25, 0.2, 0.25]
        
        # Producto con icono
        product_frame = ctk.CTkFrame(inner, fg_color="transparent")
        product_frame.place(relx=0, rely=0.5, anchor="w", relwidth=widths[0])
        
        icon_frame = ctk.CTkFrame(product_frame, fg_color="#FEE2E2", width=35, height=35, corner_radius=8)
        icon_frame.pack(side="left", padx=(0, 10))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(icon_frame, text="⚠", font=ctk.CTkFont(size=16)).place(relx=0.5, rely=0.5, anchor="center")
        
        name = product.get('nombre', 'Sin nombre')
        if len(name) > 18:
            name = name[:15] + "..."
        
        ctk.CTkLabel(
            product_frame, text=name,
            font=ctk.CTkFont(size=11), text_color="#1E293B", anchor="w"
        ).pack(side="left", fill="y")
        
        # Días
        days = product.get('dias_sin_movimiento', 0)
        ctk.CTkLabel(
            inner, text=f"{days} días",
            font=ctk.CTkFont(size=11), text_color="#64748B", anchor="center"
        ).place(relx=sum(widths[:1]), rely=0.5, anchor="w", relwidth=widths[1])
        
        # Stock
        stock = product.get('stock', 0)
        ctk.CTkLabel(
            inner, text=f"{stock} unidades",
            font=ctk.CTkFont(size=11), text_color="#1E293B", anchor="center"
        ).place(relx=sum(widths[:2]), rely=0.5, anchor="w", relwidth=widths[2])
        
        # Estado
        badge_container = ctk.CTkFrame(inner, fg_color="transparent")
        badge_container.place(relx=sum(widths[:3]), rely=0.5, anchor="w", relwidth=widths[3])
        
        badge = ctk.CTkFrame(badge_container, fg_color="#FEE2E2", corner_radius=12, height=26)
        badge.pack(anchor="center")
        
        ctk.CTkLabel(
            badge, text="Atención Requerida",
            font=ctk.CTkFont(size=9, weight="bold"), text_color="#DC2626"
        ).pack(padx=10, pady=4)

    def create_decorative_image(self, parent):
        """Crea la imagen decorativa del lado derecho."""
        image_card = ctk.CTkFrame(parent, fg_color="#FEF3E3", corner_radius=15)
        image_card.pack(fill="both", expand=True)
        
        # Título decorativo
        title_frame = ctk.CTkFrame(image_card, fg_color="#FFFFFF", corner_radius=20, height=50)
        title_frame.pack(pady=20, padx=20)
        title_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            title_frame, text="Más Vendido",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#1E293B"
        ).pack(expand=True)
        
        # Intentar cargar imagen de productos
        image_path = Helpers.get_asset_path('reports_top_product_image', 'assets/images/products_showcase.png')

        try:
            img = Image.open(image_path)
            img = img.resize((300, 300), Image.LANCZOS)
            self.images["products"] = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))

            ctk.CTkLabel(
                image_card, image=self.images["products"], text=""
            ).pack(expand=True, pady=20)
        except Exception:
            # Placeholder con emoji si no hay imagen
            placeholder = ctk.CTkFrame(image_card, fg_color="#FFFFFF", corner_radius=15)
            placeholder.pack(fill="both", expand=True, padx=20, pady=20)

            ctk.CTkLabel(
                placeholder, text="🎨\n\nColoca una imagen aquí:\n'assets/images/\nproducts_showcase.png'",
                font=ctk.CTkFont(size=14), text_color="#94A3B8", justify="center"
            ).pack(expand=True)

    def export_report(self, format_type):
        """Exporta el reporte."""
        try:
            start_date = self.start_date_entry.get().strip() or None
            end_date = self.end_date_entry.get().strip() or None
            
            if start_date:
                try:
                    start_date = datetime.strptime(start_date, "%d/%m/%Y")
                except ValueError:
                    self.show_message("Formato de fecha inicio incorrecto\nUse: DD/MM/YYYY", "error")
                    return
            
            if end_date:
                try:
                    end_date = datetime.strptime(end_date, "%d/%m/%Y")
                except ValueError:
                    self.show_message("Formato de fecha fin incorrecto\nUse: DD/MM/YYYY", "error")
                    return
            
            success, filepath = self.controller.export_report(
                format_type=format_type,
                start_date=start_date,
                end_date=end_date
            )
            
            if success:
                Logger.success(f"Reporte exportado: {filepath}", "REPORTS_VIEW")
                filename = os.path.basename(filepath)
                self.show_message(f"✅ Reporte exportado\n\n{filename}", "success")
            else:
                Logger.error(f"Error al exportar: {filepath}", "REPORTS_VIEW")
                self.show_message(f"❌ Error:\n{filepath}", "error")
                
        except Exception as e:
            Logger.error(f"Error en exportación: {e}", "REPORTS_VIEW")
            self.show_message(f"❌ Error: {str(e)}", "error")

    def show_full_report(self):
        """Muestra informe completo."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Informe Completo - Productos de Baja Rotación")
        dialog.geometry("950x650")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color="#F8FAFC")
        
        x = self.winfo_x() + (self.winfo_width() - 950) // 2
        y = self.winfo_y() + (self.winfo_height() - 650) // 2
        dialog.geometry(f"950x650+{x}+{y}")
        
        # Header
        header = ctk.CTkFrame(dialog, fg_color="#FFFFFF", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="both", expand=True, padx=30, pady=20)
        
        ctk.CTkLabel(
            header_inner, text="📊 Productos sin Movimiento (30+ días)",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#1E293B"
        ).pack(anchor="w")
        
        all_products = self.controller.get_low_rotation_products(limit=100)
        
        ctk.CTkLabel(
            header_inner, text=f"Total: {len(all_products)} productos",
            font=ctk.CTkFont(size=13), text_color="#64748B"
        ).pack(anchor="w")
        
        # Tabla
        table_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(15, 15))
        
        for product in all_products:
            self.create_product_row(table_frame, product)
        
        # Botón
        btn_frame = ctk.CTkFrame(dialog, fg_color="#FFFFFF", height=70)
        btn_frame.pack(fill="x")
        btn_frame.pack_propagate(False)
        
        ctk.CTkButton(
            btn_frame, text="Cerrar", width=140, height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#64748B", hover_color="#475569",
            corner_radius=10, command=dialog.destroy
           ).pack(pady=14)
        
    def show_message(self, message, msg_type="info"):
            """Muestra mensaje temporal."""
            colors = {"info": "#3B82F6", "success": "#10B981", "warning": "#F59E0B", "error": "#EF4444"}
            color = colors.get(msg_type, "#3B82F6")
            
            popup = ctk.CTkToplevel(self)
            popup.title("")
            popup.geometry("420x140")
            popup.resizable(False, False)
            popup.configure(fg_color="#FFFFFF")
            popup.transient(self)
            popup.grab_set()
            
            popup.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() // 2) - (420 // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (140 // 2)
            popup.geometry(f"420x140+{x}+{y}")
            
            ctk.CTkLabel(
                popup, text=message, wraplength=380,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=color, justify="center"
            ).pack(expand=True, padx=20, pady=20)
            
            popup.after(3000, popup.destroy)