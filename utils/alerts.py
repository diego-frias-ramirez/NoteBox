"""
NoteBox - Sistema de Gestión de Inventario
Sistema de alertas y notificaciones
"""

from tkinter import messagebox
import json
from assets.styles.colors import Colors

class Alerts:
    """Clase para manejar alertas y notificaciones del sistema"""

    # Cargar configuración
    with open('../config/app_settings.json', 'r', encoding='utf-8') as f:
        settings = json.load(f)

    @staticmethod
    def show_info(title, message):
        """Muestra un mensaje informativo"""
        messagebox.showinfo(title, message)

    @staticmethod
    def show_warning(title, message):
        """Muestra una advertencia"""
        messagebox.showwarning(title, message)

    @staticmethod
    def show_error(title, message):
        """Muestra un error"""
        messagebox.showerror(title, message)

    @staticmethod
    def show_success(title, message):
        """Muestra un mensaje de éxito"""
        messagebox.showinfo(title, f"✓ {message}")

    @staticmethod
    def confirm(title, message):
        """Muestra un diálogo de confirmación"""
        return messagebox.askyesno(title, message)

    @staticmethod
    def confirm_delete(item_name="este elemento"):
        """Confirma la eliminación de un elemento"""
        return Alerts.confirm(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar {item_name}?\n\nEsta acción no se puede deshacer."
        )

    @staticmethod
    def success_save():
        """Mensaje de guardado exitoso"""
        Alerts.show_success("Éxito", "Los datos se guardaron correctamente")

    @staticmethod
    def success_delete():
        """Mensaje de eliminación exitosa"""
        Alerts.show_success("Éxito", "El elemento se eliminó correctamente")

    @staticmethod
    def success_update():
        """Mensaje de actualización exitosa"""
        Alerts.show_success("Éxito", "Los datos se actualizaron correctamente")

    @staticmethod
    def error_save():
        """Mensaje de error al guardar"""
        Alerts.show_error("Error", "No se pudieron guardar los datos")

    @staticmethod
    def error_delete():
        """Mensaje de error al eliminar"""
        Alerts.show_error("Error", "No se pudo eliminar el elemento")

    @staticmethod
    def error_load():
        """Mensaje de error al cargar datos"""
        Alerts.show_error("Error", "No se pudieron cargar los datos")

    @staticmethod
    def error_database():
        """Mensaje de error de base de datos"""
        Alerts.show_error(
            "Error de Base de Datos",
            "No se pudo conectar a la base de datos.\nVerifique la configuración."
        )

    @staticmethod
    def validation_error(message):
        """Muestra un error de validación"""
        Alerts.show_warning("Error de Validación", message)

    @staticmethod
    def empty_fields():
        """Alerta de campos vacíos"""
        Alerts.validation_error("Por favor complete todos los campos obligatorios")

    @staticmethod
    def no_selection():
        """Alerta de no selección"""
        Alerts.show_warning("Sin selección", "Por favor seleccione un elemento de la lista")

    @staticmethod
    def stock_alert(product_name, stock_actual, stock_minimo):
        """Alerta de stock bajo"""
        message = f"¡Atención!\n\n"
        message += f"Producto: {product_name}\n"
        message += f"Stock actual: {stock_actual} unidades\n"
        message += f"Stock mínimo: {stock_minimo} unidades\n\n"
        message += "Es necesario reabastecer este producto."

        Alerts.show_warning("Alerta de Stock Bajo", message)

    @staticmethod
    def get_stock_alerts_count(products):
        """Cuenta productos con stock bajo"""
        count = 0
        threshold = Alerts.settings['alerts']['stock_bajo_threshold']

        for product in products:
            if product.get('stock', 0) <= threshold:
                count += 1

        return count

    @staticmethod
    def get_low_rotation_alerts_count(products):
        """Cuenta productos con baja rotación"""
        from utils.helpers import Helpers

        count = 0
        days_threshold = Alerts.settings['alerts']['dias_sin_movimiento']

        for product in products:
            last_movement = product.get('ultima_actualizacion')
            if last_movement:
                days = Helpers.calculate_days_difference(last_movement)
                if days >= days_threshold:
                    count += 1

        return count

    @staticmethod
    def show_stock_summary(total_products, low_stock, no_stock, low_rotation):
        """Muestra un resumen de alertas de inventario"""
        message = "=== RESUMEN DE INVENTARIO ===\n\n"
        message += f"Total de productos: {total_products}\n"
        message += f"Productos con stock bajo: {low_stock}\n"
        message += f"Productos sin stock: {no_stock}\n"
        message += f"Productos sin movimiento: {low_rotation}\n\n"

        if low_stock > 0 or no_stock > 0:
            message += "⚠ Requiere atención inmediata"
        else:
            message += "✓ Inventario en buen estado"

        Alerts.show_info("Resumen de Inventario", message)

    @staticmethod
    def ask_custom(title, message, options=("Sí", "No")):
        """Diálogo personalizado con opciones"""
        # Por simplicidad, usa askyesno
        # En una implementación más completa, se podría crear un diálogo personalizado
        return messagebox.askyesno(title, message)