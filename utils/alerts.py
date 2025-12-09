"""
NoteBox - Sistema de Gestión de Inventario
Sistema de alertas y notificaciones
"""

from tkinter import messagebox
import customtkinter as ctk
import json
import queue
from assets.styles.colors import Colors
from model.alert_model import AlertModel
from utils.logger import Logger

class AlertManager:
    """Clase para gestionar las alertas del sistema."""

    # Cargar configuración
    import os
    _config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'app_settings.json')
    with open(_config_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)

    def __init__(self):
        self.alert_model = AlertModel()
        self.ui_queue = queue.Queue() # Cola para notificaciones en tiempo real

    def _create_custom_dialog(self, parent, title, message, dialog_type="info", buttons=None):
        """
        Crea un diálogo personalizado con CustomTkinter para mostrar mensajes largos.
        
        Args:
            parent: Ventana padre (puede ser None)
            title: Título del diálogo
            message: Mensaje a mostrar
            dialog_type: Tipo de diálogo ('info', 'warning', 'error', 'success')
            buttons: Lista de tuplas (texto, comando) para botones personalizados
        
        Returns:
            CTkToplevel: Ventana del diálogo
        """
        # Colores según tipo
        colors = {
            'info': {'bg': '#EFF6FF', 'fg': '#1E40AF', 'btn': '#3B82F6'},
            'warning': {'bg': '#FEF3C7', 'fg': '#92400E', 'btn': '#F59E0B'},
            'error': {'bg': '#FEE2E2', 'fg': '#991B1B', 'btn': '#EF4444'},
            'success': {'bg': '#D1FAE5', 'fg': '#065F46', 'btn': '#10B981'}
        }
        
        color_scheme = colors.get(dialog_type, colors['info'])
        
        # Crear ventana
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        
        # Calcular tamaño según longitud del mensaje
        message_lines = message.count('\n') + 1
        message_length = len(message)
        
        if message_length > 500 or message_lines > 10:
            width, height = 650, 550
        elif message_length > 200 or message_lines > 5:
            width, height = 550, 400
        else:
            width, height = 500, 300
        
        dialog.geometry(f"{width}x{height}")
        dialog.resizable(True, True)  # Permitir redimensionar
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - width) // 2
        y = (dialog.winfo_screenheight() - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Hacer modal
        dialog.transient(parent)
        dialog.grab_set()
        dialog.lift()
        dialog.focus_force()
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog, fg_color=color_scheme['bg'])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header con título
        header_frame = ctk.CTkFrame(main_frame, fg_color=color_scheme['btn'], height=60)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Icono según tipo
        icons = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅'
        }
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=icons.get(dialog_type, 'ℹ️'),
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left", padx=20, pady=15)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#FFFFFF"
        )
        title_label.pack(side="left", padx=(0, 20), pady=15)
        
        # Área de contenido con scroll
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # TextBox para mensaje largo con scroll
        text_box = ctk.CTkTextbox(
            content_frame,
            font=ctk.CTkFont(size=13),
            fg_color="#FFFFFF",
            text_color=color_scheme['fg'],
            wrap="word",
            activate_scrollbars=True,
            border_width=2,
            border_color="#E5E7EB"
        )
        text_box.pack(fill="both", expand=True)
        text_box.insert("1.0", message)
        text_box.configure(state="disabled")  # Solo lectura
        
        # Frame de botones
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=60)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        button_frame.pack_propagate(False)
        
        if buttons:
            # Botones personalizados
            for btn_text, btn_command in buttons:
                btn = ctk.CTkButton(
                    button_frame,
                    text=btn_text,
                    width=120,
                    height=40,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    fg_color=color_scheme['btn'],
                    hover_color=color_scheme['fg'],
                    command=lambda cmd=btn_command: [cmd() if cmd else None, dialog.destroy()]
                )
                btn.pack(side="right", padx=5)
        else:
            # Botón OK por defecto
            ok_btn = ctk.CTkButton(
                button_frame,
                text="OK",
                width=120,
                height=40,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=color_scheme['btn'],
                hover_color=color_scheme['fg'],
                command=dialog.destroy
            )
            ok_btn.pack(side="right", padx=5)
        
        return dialog

    def show_info(self, title, message, parent=None):
        """Muestra un mensaje informativo"""
        if len(message) > 150:
            self._create_custom_dialog(parent, title, message, "info")
        else:
            messagebox.showinfo(title, message)

    def show_warning(self, title, message, parent=None):
        """Muestra una advertencia"""
        if len(message) > 150:
            self._create_custom_dialog(parent, title, message, "warning")
        else:
            messagebox.showwarning(title, message)

    def show_error(self, title, message, parent=None):
        """Muestra un error"""
        if len(message) > 150:
            self._create_custom_dialog(parent, title, message, "error")
        else:
            messagebox.showerror(title, message)

    def show_success(self, title, message, parent=None):
        """Muestra un mensaje de éxito"""
        if len(message) > 150:
            self._create_custom_dialog(parent, title, f"✓ {message}", "success")
        else:
            messagebox.showinfo(title, f"✓ {message}")

    def confirm(self, title, message, parent=None):
        """Muestra un diálogo de confirmación"""
        if len(message) > 150:
            result = {'confirmed': False}
            
            def on_yes():
                result['confirmed'] = True
            
            dialog = self._create_custom_dialog(
                parent, title, message, "warning",
                buttons=[("No", None), ("Sí", on_yes)]
            )
            dialog.wait_window()
            return result['confirmed']
        else:
            return messagebox.askyesno(title, message)

    def confirm_delete(self, item_name="este elemento", parent=None):
        """Confirma la eliminación de un elemento"""
        message = f"¿Está seguro que desea eliminar {item_name}?\n\nEsta acción no se puede deshacer."
        return self.confirm("Confirmar eliminación", message, parent)

    def success_save(self, parent=None):
        """Mensaje de guardado exitoso"""
        self.show_success("Éxito", "Los datos se guardaron correctamente", parent)

    def success_delete(self, parent=None):
        """Mensaje de eliminación exitosa"""
        self.show_success("Éxito", "El elemento se eliminó correctamente", parent)

    def success_update(self, parent=None):
        """Mensaje de actualización exitosa"""
        self.show_success("Éxito", "Los datos se actualizaron correctamente", parent)

    def error_save(self, parent=None):
        """Mensaje de error al guardar"""
        self.show_error("Error", "No se pudieron guardar los datos", parent)

    def error_delete(self, parent=None):
        """Mensaje de error al eliminar"""
        self.show_error("Error", "No se pudo eliminar el elemento", parent)

    def error_load(self, parent=None):
        """Mensaje de error al cargar datos"""
        self.show_error("Error", "No se pudieron cargar los datos", parent)

    def error_database(self, parent=None):
        """Mensaje de error de base de datos"""
        self.show_error(
            "Error de Base de Datos",
            "No se pudo conectar a la base de datos.\nVerifique la configuración.",
            parent
        )

    def validation_error(self, message, parent=None):
        """Muestra un error de validación"""
        # Siempre usar ventana personalizada para validaciones
        self._create_custom_dialog(parent, "Error de Validación", message, "warning")

    def empty_fields(self, parent=None):
        """Alerta de campos vacíos"""
        message = "Por favor complete todos los campos obligatorios.\n\nAsegúrese de llenar toda la información requerida antes de continuar."
        self._create_custom_dialog(parent, "Campos Incompletos", message, "warning")

    def no_selection(self, parent=None):
        """Alerta de no selección"""
        self.show_warning("Sin selección", "Por favor seleccione un elemento de la lista", parent)

    def stock_alert(self, product_name, stock_actual, stock_minimo, parent=None):
        """Alerta de stock bajo con ventana personalizada"""
        message = f"¡Atención!\n\n"
        message += f"Producto: {product_name}\n"
        message += f"Stock actual: {stock_actual} unidades\n"
        message += f"Stock mínimo: {stock_minimo} unidades\n\n"
        message += f"Faltante: {stock_minimo - stock_actual} unidades\n\n"
        message += "Es necesario reabastecer este producto lo antes posible."

        self._create_custom_dialog(parent, "Alerta de Stock Bajo", message, "warning")

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

    def show_stock_summary(self, total_products, low_stock, no_stock, low_rotation, parent=None):
        """Muestra un resumen de alertas de inventario con ventana personalizada"""
        message = "=== RESUMEN DE INVENTARIO ===\n\n"
        message += f"📦 Total de productos: {total_products}\n"
        message += f"⚠️ Productos con stock bajo: {low_stock}\n"
        message += f"❌ Productos sin stock: {no_stock}\n"
        message += f"📉 Productos sin movimiento: {low_rotation}\n\n"

        if low_stock > 0 or no_stock > 0:
            message += "⚠️ ATENCIÓN: Requiere atención inmediata\n\n"
            if no_stock > 0:
                message += f"• {no_stock} producto(s) completamente agotado(s)\n"
            if low_stock > 0:
                message += f"• {low_stock} producto(s) por debajo del stock mínimo\n"
            if low_rotation > 0:
                message += f"• {low_rotation} producto(s) sin movimiento reciente\n"
        else:
            message += "✅ Inventario en buen estado\n"
            message += "Todos los productos tienen stock suficiente."

        dialog_type = "warning" if (low_stock > 0 or no_stock > 0) else "success"
        self._create_custom_dialog(parent, "Resumen de Inventario", message, dialog_type)

    def ask_custom(self, title, message, options=("Sí", "No"), parent=None):
        """Diálogo personalizado con opciones"""
        return self.confirm(title, message, parent)

    # --- FUNCIONES PARA INTERACTUAR CON EL MODELO ---
    def generate_stock_alert(self, product):
        """
        Genera una alerta de stock bajo o agotado y la guarda en la base de datos.
        Verifica si ya existe una alerta similar antes de crear una nueva.
        Resuelve alertas anteriores si el stock se ha normalizado.

        Args:
            product (dict): Diccionario con datos del producto (id, nombre, stock, stock_minimo).

        Returns:
            int: ID de la alerta creada, o None si falla o ya existe.
        """
        tipo_alerta = None
        descripcion = ""
        stock_minimo = product.get('stock_minimo', 10)

        if product.get('stock', 0) <= 0:
            tipo_alerta = 'Producto agotado'
            descripcion = f"El producto '{product['nombre']}' se ha agotado completamente."
        elif product.get('stock', 0) <= stock_minimo:
            tipo_alerta = 'Stock bajo'
            descripcion = f"El producto '{product['nombre']}' tiene solo {product['stock']} unidades disponibles (mínimo: {stock_minimo})."
        else:
            # El stock está bien, resolver alertas anteriores si existen
            resolved = self.alert_model.mark_stock_alerts_as_resolved(product['id'])
            if resolved > 0:
                Logger.info(f"Stock normalizado para producto '{product['nombre']}'. {resolved} alertas resueltas.", "ALERT_MANAGER")
            return None

        if tipo_alerta:
            # Verificar si ya existe una alerta similar en las últimas 24 horas
            if not self.alert_model.check_existing_alert(tipo_alerta, product['id'], hours=24):
                # Crear alerta en la base de datos usando el modelo
                alert_id = self.alert_model.create_alert(tipo=tipo_alerta, producto_id=product['id'], descripcion=descripcion)
                
                # Enviar a la UI
                self.ui_queue.put({
                    "title": tipo_alerta,
                    "message": descripcion,
                    "icon": "error" if tipo_alerta == "Producto agotado" else "warning"
                })
                
                return alert_id
            else:
                # Ya existe una alerta similar reciente, no crear duplicado
                return None

        return None

    def generate_inactive_product_alert(self, product):
        """
        Genera una alerta de producto sin movimiento y la guarda en la base de datos.

        Args:
            product (dict): Diccionario con datos del producto (id, nombre, dias_sin_movimiento).

        Returns:
            int: ID de la alerta creada, o None si falla.
        """
        if product.get('dias_sin_movimiento', 0) >= 30:
            tipo_alerta = 'Sin movimiento'
            descripcion = f"El producto '{product['nombre']}' lleva {product['dias_sin_movimiento']} días sin rotación."

            # Verificar si ya existe una alerta similar en las últimas 48 horas
            if not self.alert_model.check_existing_alert(tipo_alerta, product['id'], hours=48):
                # Crear alerta en la base de datos usando el modelo
                alert_id = self.alert_model.create_alert(tipo=tipo_alerta, producto_id=product['id'], descripcion=descripcion)
                
                # Enviar a la UI
                self.ui_queue.put({
                    "title": tipo_alerta,
                    "message": descripcion,
                    "icon": "warning"
                })
                
                return alert_id

        return None

    def generate_movement_alert(self, product, movement_type, quantity, reason):
        """
        Genera una notificación de movimiento de inventario (entrada o salida).
        
        Args:
            product (dict): Diccionario con datos del producto (id, nombre, stock).
            movement_type (str): Tipo de movimiento ('Entrada' o 'Salida').
            quantity (int): Cantidad del movimiento.
            reason (str): Razón del movimiento.
        
        Returns:
            int: ID de la alerta creada, o None si falla.
        """
        # Determinar el tipo de alerta según el movimiento
        if movement_type == 'Entrada':
            tipo_alerta = 'Entrada de inventario'
            icono = '📥'
        else:
            tipo_alerta = 'Salida de inventario'
            icono = '📤'
        
        # Crear descripción detallada
        descripcion = f"{icono} {movement_type} de {quantity} unidades. Stock actual: {product.get('stock', 0)}. Motivo: {reason}"
        
        # Crear alerta en la base de datos
        alert_id = self.alert_model.create_alert(
            tipo=tipo_alerta,
            producto_id=product['id'],
            descripcion=descripcion
        )
        
        # Enviar a la UI
        self.ui_queue.put({
            "title": tipo_alerta,
            "message": descripcion,
            "icon": "info"
        })
        
        return alert_id

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
    
    def get_unread_count(self):
        """
        Obtiene el número de alertas no leídas.
        
        Returns:
            int: Número de alertas no leídas.
        """
        unread = self.alert_model.get_unread_alerts()
        return len(unread) if unread else 0

# Instancia global del gestor de alertas
alert_manager = AlertManager()