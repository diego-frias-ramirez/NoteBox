"""
NoteBox - Sistema de Gestión de Inventario
Validadores de datos
"""

import re
import json
import os # <-- Añade esta línea
from datetime import datetime

class Validators:
    """Clase con métodos de validación para diferentes tipos de datos"""

    # Cargar configuración de validaciones usando ruta absoluta
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # <-- Obtiene la carpeta donde está validators.py
    APP_SETTINGS_FILE = os.path.join(CURRENT_DIR, '..', 'config', 'app_settings.json') # <-- Construye la ruta absoluta

    try:
        with open(APP_SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        validations = settings['validations']
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {APP_SETTINGS_FILE}")
        validations = {} # <-- Fallback a un diccionario vacío
    except json.JSONDecodeError:
        print(f"Error: El archivo {APP_SETTINGS_FILE} no tiene un formato JSON válido.")
        validations = {} # <-- Fallback a un diccionario vacío
    except KeyError:
        print(f"Error: La clave 'validations' no se encontró en {APP_SETTINGS_FILE}")
        validations = {} # <-- Fallback a un diccionario vacío


    @staticmethod
    def validate_not_empty(value, field_name="Campo"):
        """Valida que un campo no esté vacío"""
        if not value or str(value).strip() == "":
            return False, f"{field_name} no puede estar vacío"
        return True, ""

    @staticmethod
    def validate_string_length(value, max_length, field_name="Campo"):
        """Valida la longitud de una cadena"""
        if len(str(value)) > max_length:
            return False, f"{field_name} no puede exceder {max_length} caracteres"
        return True, ""

    @staticmethod
    def validate_product_name(name):
        """Valida el nombre de un producto"""
        # No vacío
        is_valid, msg = Validators.validate_not_empty(name, "Nombre del producto")
        if not is_valid:
            return False, msg

        # Longitud máxima
        max_length = Validators.validations.get('max_product_name_length', 100) # <-- Usa .get() con fallback
        is_valid, msg = Validators.validate_string_length(name, max_length, "Nombre del producto")
        if not is_valid:
            return False, msg

        return True, ""

    @staticmethod
    def validate_category_name(name):
        """Valida el nombre de una categoría"""
        # No vacío
        is_valid, msg = Validators.validate_not_empty(name, "Nombre de categoría")
        if not is_valid:
            return False, msg

        # Longitud máxima
        max_length = Validators.validations.get('max_category_name_length', 50) # <-- Usa .get() con fallback
        is_valid, msg = Validators.validate_string_length(name, max_length, "Nombre de categoría")
        if not is_valid:
            return False, msg

        return True, ""

    @staticmethod
    def validate_price(price):
        """Valida un precio"""
        try:
            price_float = float(price)

            min_price = Validators.validations.get('min_price', 0.01) # <-- Usa .get() con fallback
            max_price = Validators.validations.get('max_price', 999999.99) # <-- Usa .get() con fallback

            if price_float < min_price:
                return False, f"El precio debe ser mayor o igual a ${min_price}"

            if price_float > max_price:
                return False, f"El precio no puede exceder ${max_price:,.2f}"

            return True, ""
        except ValueError:
            return False, "El precio debe ser un número válido"

    @staticmethod
    def validate_stock(stock):
        """Valida la cantidad de stock"""
        try:
            stock_int = int(stock)

            if stock_int < 0:
                return False, "El stock no puede ser negativo"

            max_stock = Validators.validations.get('max_stock', 999999) # <-- Usa .get() con fallback
            if stock_int > max_stock:
                return False, f"El stock no puede exceder {max_stock:,} unidades"

            return True, ""
        except ValueError:
            return False, "El stock debe ser un número entero válido"

    @staticmethod
    def validate_positive_number(value, field_name="Cantidad"):
        """Valida que un número sea positivo"""
        try:
            num = float(value)
            if num <= 0:
                return False, f"{field_name} debe ser mayor a 0"
            return True, ""
        except ValueError:
            return False, f"{field_name} debe ser un número válido"

    @staticmethod
    def validate_integer(value, field_name="Campo"):
        """Valida que un valor sea un entero"""
        try:
            int(value)
            return True, ""
        except ValueError:
            return False, f"{field_name} debe ser un número entero"

    @staticmethod
    def validate_email(email):
        """Valida un correo electrónico"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Correo electrónico inválido"

    @staticmethod
    def validate_phone(phone):
        """Valida un número telefónico (formato México)"""
        # Remover espacios y guiones
        phone_clean = re.sub(r'[\s\-\(\)]', '', phone)

        # Validar que sea solo números y tenga 10 dígitos
        if re.match(r'^\d{10}$', phone_clean):
            return True, ""
        return False, "Teléfono debe tener 10 dígitos"

    @staticmethod
    def validate_date(date_str, format="%d/%m/%Y"):
        """Valida una fecha"""
        try:
            datetime.strptime(date_str, format)
            return True, ""
        except ValueError:
            return False, f"Fecha inválida. Formato esperado: {format}"

    @staticmethod
    def validate_product_data(data):
        """Valida todos los datos de un producto"""
        errors = []

        # Validar nombre
        is_valid, msg = Validators.validate_product_name(data.get('nombre', ''))
        if not is_valid:
            errors.append(msg)

        # Validar categoría
        if not data.get('categoria_id'):
            errors.append("Debe seleccionar una categoría")

        # Validar precio
        is_valid, msg = Validators.validate_price(data.get('precio', 0))
        if not is_valid:
            errors.append(msg)

        # Validar stock
        is_valid, msg = Validators.validate_stock(data.get('stock', 0))
        if not is_valid:
            errors.append(msg)

        # Validar stock mínimo
        is_valid, msg = Validators.validate_stock(data.get('stock_minimo', 0))
        if not is_valid:
            errors.append(f"Stock mínimo: {msg}")

        if errors:
            return False, "\n".join(errors)
        return True, ""