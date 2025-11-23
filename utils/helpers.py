"""
NoteBox - Sistema de Gestión de Inventario
Funciones auxiliares generales
"""

import os
import json
from datetime import datetime, timedelta

class Helpers:
    """Clase con funciones auxiliares del sistema"""

    @staticmethod
    def _load_settings():
        """
        Carga la configuración de la aplicación de forma segura.
        Retorna un diccionario con la configuración o uno vacío si hay error.
        """
        # Obtener la ruta del archivo helpers.py
        current_file = os.path.abspath(__file__)
        # Ir 2 niveles arriba para llegar a la raíz del proyecto (utils/helpers.py -> / -> proyecto)
        project_root = os.path.dirname(os.path.dirname(current_file))
        config_path = os.path.join(project_root, "config", "app_settings.json")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de configuración en {config_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: El archivo {config_path} no es un JSON válido.")
            return {}
        except Exception as e:
            print(f"Error inesperado al cargar la configuración: {e}")
            return {}

    @staticmethod
    def format_currency(amount):
        """Formatea un número como moneda"""
        try:
            # Cargar la configuración cada vez que se necesita
            settings = Helpers._load_settings()
            symbol = settings.get('formats', {}).get('currency_symbol', '$')
            return f"{symbol}{float(amount):,.2f}"
        except (ValueError, TypeError):
            # Si amount no se puede convertir a float, devolver 0.00
            return "$0.00"

    @staticmethod
    def format_date(date_obj, format=None):
        """Formatea una fecha"""
        if format is None:
            settings = Helpers._load_settings()
            format = settings.get('formats', {}).get('date_format', '%d/%m/%Y')

        if isinstance(date_obj, str):
            return date_obj

        return date_obj.strftime(format)

    @staticmethod
    def format_datetime(datetime_obj, format=None):
        """Formatea una fecha y hora"""
        if format is None:
            settings = Helpers._load_settings()
            format = settings.get('formats', {}).get('datetime_format', '%d/%m/%Y %H:%M')

        if isinstance(datetime_obj, str):
            return datetime_obj

        return datetime_obj.strftime(format)

    @staticmethod
    def parse_date(date_str, format=None):
        """Convierte una cadena a objeto datetime"""
        if format is None:
            settings = Helpers._load_settings()
            format = settings.get('formats', {}).get('date_format', '%d/%m/%Y')

        try:
            return datetime.strptime(date_str, format)
        except:
            return None

    @staticmethod
    def get_stock_status(stock, stock_minimo):
        """Determina el estado del stock"""
        settings = Helpers._load_settings()
        thresholds = settings.get('alerts', {})
        stock_medio_threshold = thresholds.get('stock_medio_threshold', 50)
        
        if stock <= 0:
            return "Sin stock"
        elif stock <= stock_minimo:
            return "Stock bajo"
        elif stock <= stock_medio_threshold:
            return "Stock medio"
        else:
            return "Stock alto"

    @staticmethod
    def get_stock_color(stock, stock_minimo):
        """Retorna el color según el nivel de stock"""
        # Este método depende de un archivo de colores que quizás no uses
        # Si no lo usas, puedes eliminarlo o implementar una lógica simple
        # Por ahora, retornaremos un color por defecto
        return "#10B981"  # Verde por defecto

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

    # --- NUEVA FUNCIÓN PARA EXPORTACIÓN ---

    @staticmethod
    def generate_export_filename(base_name, file_format="csv"):
        """
        Genera un nombre de archivo único para exportaciones.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.{file_format}"

    @staticmethod
    def get_exports_dir(subdir="reports"):
        """
        Obtiene la ruta del directorio de exportaciones.
        """
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file))
        exports_dir = os.path.join(project_root, "exports", subdir)
        os.makedirs(exports_dir, exist_ok=True)
        return exports_dir