"""
NoteBox - Sistema de Gestión de Inventario
Funciones auxiliares generales
"""

import os
import json
from datetime import datetime, timedelta

class Helpers:
    """Clase con funciones auxiliares del sistema"""

    # Obtener la ruta absoluta del directorio actual (donde está helpers.py)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta absoluta al archivo app_settings.json
    APP_SETTINGS_FILE = os.path.join(CURRENT_DIR, '..', 'config', 'app_settings.json')
    
    # Cargar configuración
    try:
        with open(APP_SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {APP_SETTINGS_FILE}")
        settings = {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {APP_SETTINGS_FILE} no tiene un formato JSON válido.")
        settings = {}

    @staticmethod
    def format_currency(amount):
        """Formatea un número como moneda"""
        try:
            symbol = Helpers.settings['formats']['currency_symbol']
            return f"{symbol}{float(amount):,.2f}"
        except:
            return f"${float(amount):,.2f}"

    @staticmethod
    def format_date(date_obj, format=None):
        """Formatea una fecha"""
        if format is None:
            format = Helpers.settings['formats']['date_format']

        if isinstance(date_obj, str):
            return date_obj

        return date_obj.strftime(format)

    @staticmethod
    def format_datetime(datetime_obj, format=None):
        """Formatea una fecha y hora"""
        if format is None:
            format = Helpers.settings['formats']['datetime_format']

        if isinstance(datetime_obj, str):
            return datetime_obj

        return datetime_obj.strftime(format)

    @staticmethod
    def parse_date(date_str, format=None):
        """Convierte una cadena a objeto datetime"""
        if format is None:
            format = Helpers.settings['formats']['date_format']

        try:
            return datetime.strptime(date_str, format)
        except:
            return None

    @staticmethod
    def get_stock_status(stock, stock_minimo):
        """Determina el estado del stock"""
        thresholds = Helpers.settings['alerts']
        
        if stock <= 0:
            return "Sin stock"
        elif stock <= stock_minimo:
            return "Stock bajo"
        elif stock <= thresholds['stock_medio_threshold']:
            return "Stock medio"
        else:
            return "Stock alto"

    @staticmethod
    def get_stock_color(stock, stock_minimo):
        """Retorna el color según el nivel de stock"""
        from assets.styles.colors import Colors
        
        if stock <= 0:
            return Colors.ACCENT
        elif stock <= stock_minimo:
            return Colors.STOCK_BAJO
        elif stock <= Helpers.settings['alerts']['stock_medio_threshold']:
            return Colors.STOCK_MEDIO
        else:
            return Colors.STOCK_ALTO

    @staticmethod
    def calculate_days_difference(date1, date2=None):
        """Calcula la diferencia en días entre dos fechas"""
        if date2 is None:
            date2 = datetime.now()
        
        if isinstance(date1, str):
            date1 = Helpers.parse_date(date1)
        if isinstance(date2, str):
            date2 = Helpers.parse_date(date2)
        
        if date1 and date2:
            return abs((date2 - date1).days)
        return 0

    @staticmethod
    def truncate_text(text, max_length=50, suffix="..."):
        """Trunca un texto si excede la longitud máxima"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def sanitize_filename(filename):
        """Sanitiza un nombre de archivo"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    @staticmethod
    def generate_report_filename(report_type, extension="pdf"):
        """Genera un nombre de archivo para un reporte"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"NoteBox_{report_type}_{timestamp}.{extension}"
        return Helpers.sanitize_filename(filename)

    @staticmethod
    def format_number(number, decimals=0):
        """Formatea un número con separadores de miles"""
        try:
            if decimals > 0:
                return f"{float(number):,.{decimals}f}"
            return f"{int(number):,}"
        except:
            return str(number)

    @staticmethod
    def calculate_percentage(part, total):
        """Calcula un porcentaje"""
        try:
            if total == 0:
                return 0
            return (part / total) * 100
        except:
            return 0

    @staticmethod
    def format_percentage(value, decimals=2):
        """Formatea un porcentaje"""
        return f"{float(value):.{decimals}f}%"

    @staticmethod
    def get_date_range(days_back=30):
        """Obtiene un rango de fechas"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        return start_date, end_date

    @staticmethod
    def is_valid_number(value):
        """Verifica si un valor es un número válido"""
        try:
            float(value)
            return True
        except:
            return False

    @staticmethod
    def clean_numeric_input(value):
        """Limpia un input numérico"""
        # Remover caracteres no numéricos excepto punto decimal
        import re
        return re.sub(r'[^\d.]', '', str(value))

    @staticmethod
    def center_window(window, width, height):
        """Centra una ventana en la pantalla"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")