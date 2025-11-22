"""
NoteBox - Sistema de Gestión de Inventario
Sistema de alertas y notificaciones
"""

from tkinter import messagebox
import json
from assets.styles.colors import Colors
from model.alert_model import AlertModel # Importar el modelo de alertas

class AlertManager:
    """Clase para gestionar las alertas del sistema."""

    # Cargar configuración
    with open('../config/app_settings.json', 'r', encoding='utf-8') as f:
        settings = json.load(f)

    def __init__(self):
        self.alert_model = AlertModel() # Instanciar el modelo de alertas

    def show_info(self, title, message):
        """Muestra un mensaje informativo"""
        messagebox.showinfo(title, message)

    def show_warning(self, title, message):
        """Muestra una advertencia"""
        messagebox.showwarning(title, message)

    def show_error(self, title, message):
        """Muestra un error"""
        messagebox.showerror(title, message)

    def show_success(self, title, message):
        """Muestra un mensaje de éxito"""
        messagebox.showinfo(title, f"✓ {message}")

    def confirm(self, title, message):
        """Muestra un diálogo de confirmación"""
        return messagebox.askyesno(title, message)

    def confirm_delete(self, item_name="este elemento"):
        """Confirma la eliminación de un elemento"""
        return self.confirm(
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar {item_name}?\n\nEsta acción no se puede deshacer."
        )

    def success_save(self):
        """Mensaje de guardado exitoso"""
        self.show_success("Éxito", "Los datos se guardaron correctamente")

    def success_delete(self):
        """Mensaje de eliminación exitosa"""
        self.show_success("Éxito", "El elemento se eliminó correctamente")

    def success_update(self):
        """Mensaje de actualización exitosa"""
        self.show_success("Éxito", "Los datos se actualizaron correctamente")

    def error_save(self):
        """Mensaje de error al guardar"""
        self.show_error("Error", "No se pudieron guardar los datos")

    def error_delete(self):
        """Mensaje de error al eliminar"""
        self.show_error("Error", "No se pudo eliminar el elemento")

    def error_load(self):
        """Mensaje de error al cargar datos"""
        self.show_error("Error", "No se pudieron cargar los datos")

    def error_database(self):
        """Mensaje de error de base de datos"""
        self.show_error(
            "Error de Base de Datos",
            "No se pudo conectar a la base de datos.\nVerifique la configuración."
        )

    def validation_error(self, message):
        """Muestra un error de validación"""
        self.show_warning("Error de Validación", message)

    def empty_fields(self):
        """Alerta de campos vacíos"""
        self.validation_error("Por favor complete todos los campos obligatorios")

    def no_selection(self):
        """Alerta de no selección"""
        self.show_warning("Sin selección", "Por favor seleccione un elemento de la lista")

    def stock_alert(self, product_name, stock_actual, stock_minimo):
        """Alerta de stock bajo"""
        message = f"¡Atención!\n\n"
        message += f"Producto: {product_name}\n"
        message += f"Stock actual: {stock_actual} unidades\n"
        message += f"Stock mínimo: {stock_minimo} unidades\n\n"
        message += "Es necesario reabastecer este producto."

        self.show_warning("Alerta de Stock Bajo", message)

    def get_stock_alerts_count(self, products):
        """Cuenta productos con stock bajo"""
        count = 0
        threshold = self.settings['alerts']['stock_bajo_threshold']

        for product in products:
            if product.get('stock', 0) <= threshold:
                count += 1

        return count

    def get_low_rotation_alerts_count(self, products):
        """Cuenta productos con baja rotación"""
        from utils.helpers import Helpers

        count = 0
        days_threshold = self.settings['alerts']['dias_sin_movimiento']

        for product in products:
            last_movement = product.get('ultima_actualizacion')
            if last_movement:
                days = Helpers.calculate_days_difference(last_movement)
                if days >= days_threshold:
                    count += 1

        return count

    def show_stock_summary(self, total_products, low_stock, no_stock, low_rotation):
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

        self.show_info("Resumen de Inventario", message)

    def ask_custom(self, title, message, options=("Sí", "No")):
        """Diálogo personalizado con opciones"""
        # Por simplicidad, usa askyesno
        # En una implementación más completa, se podría crear un diálogo personalizado
        return messagebox.askyesno(title, message)

    # --- NUEVAS FUNCIONES PARA INTERACTUAR CON EL MODELO ---
    def generate_stock_alert(self, product):
        """
        Genera una alerta de stock bajo o agotado y la guarda en la base de datos.
        Utiliza el AlertModel para interactuar con la base de datos.

        Args:
            product (dict): Diccionario con datos del producto (id, nombre, stock, stock_minimo).

        Returns:
            int: ID de la alerta creada, o None si falla.
        """
        tipo_alerta = None
        descripcion = ""

        if product.get('stock', 0) <= 0:
            tipo_alerta = 'Producto agotado'
            descripcion = f"El producto '{product['nombre']}' se ha agotado completamente."
        elif product.get('stock', 0) <= product.get('stock_minimo', 10): # Usar stock_minimo del producto o un valor por defecto
            tipo_alerta = 'Stock bajo'
            descripcion = f"El producto '{product['nombre']}' tiene solo {product['stock']} unidades disponibles (mínimo: {product.get('stock_minimo', 10)})."

        if tipo_alerta:
            # Crear alerta en la base de datos usando el modelo
            alert_id = self.alert_model.create_alert(tipo=tipo_alerta, producto_id=product['id'], descripcion=descripcion)
            if alert_id:
                # Opcional: Mostrar alerta visual también
                if tipo_alerta == 'Stock bajo':
                    self.stock_alert(product['nombre'], product['stock'], product.get('stock_minimo', 10))
            return alert_id

        return None # No se generó alerta

    def generate_inactive_product_alert(self, product):
        """
        Genera una alerta de producto sin movimiento y la guarda en la base de datos.
        Utiliza el AlertModel para interactuar con la base de datos.

        Args:
            product (dict): Diccionario con datos del producto (id, nombre, dias_sin_movimiento).

        Returns:
            int: ID de la alerta creada, o None si falla.
        """
        if product.get('dias_sin_movimiento', 0) >= 30:
            tipo_alerta = 'Sin movimiento'
            descripcion = f"El producto '{product['nombre']}' lleva {product['dias_sin_movimiento']} días sin rotación."

            # Crear alerta en la base de datos usando el modelo
            alert_id = self.alert_model.create_alert(tipo=tipo_alerta, producto_id=product['id'], descripcion=descripcion)
            if alert_id:
                # Opcional: Mostrar alerta visual también
                # self.show_warning("Alerta de Producto Inactivo", descripcion) # Ejemplo de alerta visual
                pass # No se requiere alerta visual inmediata aquí, se verá en el dashboard o lista de alertas

            return alert_id

        return None # No se generó alerta

    def get_active_alerts(self):
        """
        Obtiene las alertas activas desde el modelo de alertas (base de datos).
        """
        return self.alert_model.get_active_alerts()

    def mark_alert_as_read(self, alert_id):
        """
        Marca una alerta como leída en la base de datos usando el modelo.
        """
        return self.alert_model.mark_alert_as_read(alert_id)

# Instancia global del gestor de alertas
alert_manager = AlertManager()