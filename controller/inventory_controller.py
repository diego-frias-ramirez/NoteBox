"""
NoteBox - Controlador del Módulo de Inventario
Responsabilidad: Gestionar la lógica del inventario, conectar vista y modelo.
Ubicación: controller/inventory_controller.py
"""

import os
import sys

# Asegurar que el módulo 'controller' esté en el path para imports relativos
controller_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(controller_path)

from model.product_model import ProductModel
from model.category_model import CategoryModel
from model.report_model import ReportModel
from utils.logger import Logger
from utils.validators import Validators
from utils.alerts import alert_manager
from datetime import datetime

class InventoryController:
    """Controlador para gestionar la lógica del módulo de inventario."""

    def __init__(self):
        self.product_model = ProductModel()
        self.category_model = CategoryModel()
        self.report_model = ReportModel()
        self.current_user = None # Se puede inicializar aquí o recibirlo en cada método
        self.current_page = 1
        self.products_per_page = 7
        self.search_query = ""
        self.filter_category_id = None
        self.filter_order = "nombre"  # Por defecto ordenar por nombre

    def set_current_user(self, user_data):
        """Establece el usuario actual para auditoría."""
        self.current_user = user_data

    def get_inventory_summary(self):
        """Obtiene el resumen general del inventario."""
        try:
            summary = self.report_model.get_inventory_summary()
            Logger.info("Resumen de inventario obtenido correctamente", "INVENTORY_CONTROLLER")
            return summary
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return {}

    def get_products(self, page=None, search="", category_id=None, order_by=None):
        """
        Obtiene productos con paginación y filtros.
        
        Args:
            page (int): Número de página (opcional, usa self.current_page si no se pasa).
            search (str): Término de búsqueda.
            category_id (int): ID de categoría para filtrar.
            order_by (str): Campo para ordenar ('nombre', 'fecha_creacion_asc', 'fecha_creacion_desc').
        
        Returns:
            tuple: (lista de productos, total de productos).
        """
        try:
            current_page = page if page is not None else self.current_page
            offset = (current_page - 1) * self.products_per_page

            # Si se pasa search o category_id, usarlos temporalmente
            final_search = search if search else self.search_query
            final_category_id = category_id if category_id is not None else self.filter_category_id
            final_order_by = order_by if order_by is not None else self.filter_order

            products = self.product_model.get_products(
                search=final_search,
                category_id=final_category_id,
                limit=self.products_per_page,
                offset=offset,
                order_by=final_order_by
            )
            total = self.product_model.get_total_products(
                search=final_search,
                category_id=final_category_id
            )
            
            Logger.info(f"Productos obtenidos: {len(products)}, Total: {total}", "INVENTORY_CONTROLLER")
            return products, total
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return [], 0

    def get_product_by_id(self, product_id):
        """Obtiene un producto por su ID."""
        try:
            product = self.product_model.get_product_by_id(product_id)
            if product:
                Logger.info(f"Producto ID {product_id} obtenido", "INVENTORY_CONTROLLER")
            else:
                Logger.warning(f"Producto ID {product_id} no encontrado", "INVENTORY_CONTROLLER")
            return product
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return None

    def get_categories(self):
        """Obtiene todas las categorías activas."""
        try:
            categories = self.category_model.get_all_categories()
            Logger.info(f"Categorías obtenidas: {len(categories)}", "INVENTORY_CONTROLLER")
            # Convertir lista a diccionario para acceso rápido por ID si es necesario
            return {cat['id']: cat for cat in categories}
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return {}

    def create_product(self, data):
        """
        Crea un nuevo producto.
        
        Args:
            data (dict): Datos del producto {nombre, codigo, categoria_id, stock, precio, etc.}
        
        Returns:
            tuple: (bool: éxito, str: mensaje o dict: producto creado).
        """
        # Validar datos de entrada
        is_valid, msg = Validators.validate_product_data(data)
        if not is_valid:
            Logger.warning(f"Validación fallida en creación: {msg}", "INVENTORY_CONTROLLER")
            return False, msg
        
        try:
            product_id = self.product_model.create_product(**data)
            if product_id:
                Logger.success(f"Producto '{data['nombre']}' creado con ID {product_id}", "INVENTORY_CONTROLLER")
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action("CREAR_PRODUCTO", self.current_user['nombre'], details=f"ID: {product_id}, Nombre: {data['nombre']}")
                # Devolver el producto recién creado para actualizar la vista
                created_product = self.get_product_by_id(product_id)
                
                # Verificar alertas de stock
                if created_product:
                    alert_manager.generate_stock_alert(created_product)
                    
                return True, created_product
            else:
                error_msg = "No se pudo crear el producto en la base de datos"
                Logger.error(error_msg, "INVENTORY_CONTROLLER")
                return False, error_msg
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return False, str(e)

    def update_product(self, product_id, data):
        """
        Actualiza un producto existente.
        
        Args:
            product_id (int): ID del producto.
            data (dict): Datos a actualizar.
        
        Returns:
            tuple: (bool: éxito, str: mensaje).
        """
        # Validar datos de entrada
        is_valid, msg = Validators.validate_product_data(data)
        if not is_valid:
            Logger.warning(f"Validación fallida en actualización: {msg}", "INVENTORY_CONTROLLER")
            return False, msg
        
        try:
            success = self.product_model.update_product(product_id, **data)
            if success:
                Logger.success(f"Producto ID {product_id} actualizado", "INVENTORY_CONTROLLER")
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action("ACTUALIZAR_PRODUCTO", self.current_user['nombre'], details=f"ID: {product_id}")
                
                # Devolver el producto actualizado para actualizar la vista
                updated_product = self.get_product_by_id(product_id)
                
                # Verificar alertas de stock
                if updated_product:
                    alert_manager.generate_stock_alert(updated_product)
                    
                return True, updated_product
            else:
                return False, "No se pudo actualizar el producto"
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return False, str(e)

    def delete_product(self, product_id):
        """
        Elimina (desactiva) un producto.
        
        Args:
            product_id (int): ID del producto.
        
        Returns:
            tuple: (bool: éxito, str: mensaje).
        """
        try:
            success = self.product_model.deactivate_product(product_id) # Asumiendo que tienes este método
            if success:
                Logger.success(f"Producto ID {product_id} eliminado (desactivado)", "INVENTORY_CONTROLLER")
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action("ELIMINAR_PRODUCTO", self.current_user['nombre'], details=f"ID: {product_id}")
                return True, "Producto eliminado correctamente"
            else:
                error_msg = f"No se pudo eliminar el producto ID {product_id}"
                Logger.error(error_msg, "INVENTORY_CONTROLLER")
                return False, error_msg
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return False, str(e)

    def register_movement(self, product_id, quantity, movement_type, reason, user_id):
        """
        Registra un movimiento de inventario (entrada o salida).
        
        Args:
            product_id (int): ID del producto.
            quantity (int): Cantidad movida.
            movement_type (str): 'Entrada' o 'Salida'.
            reason (str): Motivo del movimiento.
            user_id (int): ID del usuario que registra.
        
        Returns:
            tuple: (bool: éxito, str: mensaje).
        """
        try:
            # Validar tipo de movimiento
            if movement_type not in ['Entrada', 'Salida']:
                return False, "Tipo de movimiento inválido. Use 'Entrada' o 'Salida'"
            
            # Obtener producto para validación de stock
            product = self.get_product_by_id(product_id)
            if not product:
                return False, "Producto no encontrado"
            # Para salidas, validar stock suficiente
            if movement_type == 'Salida' and (product['stock'] - quantity) < 0:
                return False, f"Stock insuficiente. Disponible: {product['stock']}, Solicitado: {quantity}"
            
            # Registrar movimiento
            movement_id = self.product_model.register_movement(
                product_id=product_id,
                quantity=quantity,
                movement_type=movement_type,
                reason=reason,
                user_id=user_id
            )
            
            if movement_id:
                Logger.success(f"Movimiento registrado: {movement_type} de {quantity} unidades del producto ID {product_id}", "INVENTORY_CONTROLLER")
                
                # Registrar acción
                if self.current_user:
                    Logger.log_user_action(
                        "REGISTRAR_MOVIMIENTO", 
                        self.current_user['nombre'], 
                        details=f"Tipo: {movement_type}, Producto: {product['nombre']}, Cantidad: {quantity}"
                    )
                
                # Verificar alertas de stock después del movimiento
                updated_product = self.get_product_by_id(product_id)
                if updated_product:
                    # Generar notificación de movimiento
                    alert_manager.generate_movement_alert(
                        product=updated_product,
                        movement_type=movement_type,
                        quantity=quantity,
                        reason=reason
                    )
                    # Verificar alertas de stock bajo/agotado
                    alert_manager.generate_stock_alert(updated_product)
                    
                return True, f"Movimiento de {movement_type.lower()} registrado correctamente"

            else:
                return False, "No se pudo registrar el movimiento"
                
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return False, str(e)

    def get_low_stock_products(self, threshold=None):
        """Obtiene productos con stock bajo."""
        try:
            # Si no se pasa un umbral, usar el del modelo o uno por defecto
            if threshold is None:
                threshold = self.report_model.get_low_stock_threshold() # Asumiendo que tienes este método en ReportModel
                if threshold is None:
                    threshold = 10 # Valor por defecto si no se puede obtener de la configuración
            
            products = self.report_model.get_low_stock_products(threshold)
            Logger.info(f"Productos con stock bajo obtenidos: {len(products)}", "INVENTORY_CONTROLLER")
            return products
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return []

    def get_inactive_products(self, days_without_movement=30):
        """Obtiene productos sin movimiento por X días."""
        try:
            products = self.report_model.get_inactive_products(days_without_movement)
            Logger.info(f"Productos sin movimiento obtenidos: {len(products)}", "INVENTORY_CONTROLLER")
            return products
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return []

    def search_products(self, query):
        """Busca productos por nombre o código."""
        try:
            products = self.product_model.search_products(query)
            Logger.info(f"Resultados de búsqueda para '{query}': {len(products)} productos", "INVENTORY_CONTROLLER")
            return products
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return []

    def get_products_by_category(self, category_id):
        """Obtiene productos filtrados por categoría."""
        try:
            products, total = self.get_products(category_id=category_id)
            Logger.info(f"Productos por categoría ID {category_id}: {len(products)}", "INVENTORY_CONTROLLER")
            return products
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return []

    def export_inventory(self, format="csv", category_id=None, search_query=""):
        """
        Exporta el inventario a un archivo.
        
        Args:
            format (str): Formato de exportación ('csv', 'pdf', 'excel').
            category_id (int): Filtrar por categoría (opcional).
            search_query (str): Filtrar por búsqueda (opcional).
        
        Returns:
            tuple: (bool: éxito, str: ruta del archivo o mensaje de error).
        """
        try:
            # Obtener *todos* los productos que coincidan con los filtros (sin paginación)
            # Usar un límite alto o None si el modelo lo permite
            all_products = self.product_model.get_all_products_filtered(
                search=search_query,
                category_id=category_id
            ) # Asumiendo que tienes este método

            if not all_products:
                return False, "No hay productos para exportar con los filtros actuales"

            # Obtener nombres de categorías
            categories_dict = self.get_categories()
            
            # Formatear datos
            formatted_data = []
            for p in all_products:
                cat_name = categories_dict.get(p['categoria_id'], {}).get('nombre', 'Sin Categoría')
                formatted_data.append({
                    'ID': p['id'],
                    'Código': p['codigo'],
                    'Nombre': p['nombre'],
                    'Categoría': cat_name,
                    'Stock': p['stock'],
                    'Precio': p['precio'],
                    'Estado': p['estado'],
                    'Fecha Creación': p['fecha_creacion'].strftime('%d/%m/%Y') if isinstance(p['fecha_creacion'], datetime) else p['fecha_creacion']
                })
            
            # Generar archivo
            import pandas as pd
            df = pd.DataFrame(formatted_data)
            
            from utils.helpers import Helpers
            filename = Helpers.generate_export_filename("inventario", format)
            export_dir = Helpers.get_exports_dir("reports")
            filepath = os.path.join(export_dir, filename)
            
            if format.lower() == "csv":
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
            elif format.lower() == "excel":
                df.to_excel(filepath, index=False, engine='openpyxl')
            elif format.lower() == "pdf":
                # Para PDF, puedes usar reportlab o convertir desde Excel/Csv
                # Por simplicidad, generamos un CSV y luego lo convertimos si es necesario
                # o usamos una librería como fpdf2
                temp_csv = filepath.replace(".pdf", ".csv")
                df.to_csv(temp_csv, index=False, encoding='utf-8-sig')
                # Lógica para convertir CSV a PDF (requiere más código)
                # Por ahora, devolvemos el CSV
                return True, temp_csv
            else:
                return False, f"Formato de exportación '{format}' no soportado"
            
            Logger.success(f"Inventario exportado a: {filepath}", "INVENTORY_CONTROLLER")
            return True, filepath
            
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return False, f"Error al exportar: {str(e)}"

    def get_inventory_alerts(self):
        """Obtiene todas las alertas de inventario (stock bajo, sin movimiento, etc.)."""
        try:
            low_stock = self.get_low_stock_products()
            inactive = self.get_inactive_products()
            
            alerts = {
                "stock_bajo": low_stock,
                "sin_movimiento": inactive,
                "total_alertas": len(low_stock) + len(inactive)
            }
            
            Logger.info(f"Alertas de inventario generadas: {alerts['total_alertas']} en total", "INVENTORY_CONTROLLER")
            return alerts
        except Exception as e:
            Logger.log_error_exception(e, "INVENTORY_CONTROLLER")
            return {"stock_bajo": [], "sin_movimiento": [], "total_alertas": 0}

    # --- Métodos para manejo de paginación y filtros ---
    def set_search_query(self, query):
        """Establece la consulta de búsqueda."""
        self.search_query = query
        self.current_page = 1 # Reiniciar a la primera página al buscar

    def set_filter_category(self, category_id):
        """Establece el filtro de categoría."""
        self.filter_category_id = category_id
        self.current_page = 1 # Reiniciar a la primera página al filtrar

    def set_filter_order(self, order_by):
        """Establece el filtro de orden."""
        self.filter_order = order_by
        self.current_page = 1 # Reiniciar a la primera página al cambiar el orden

    def get_filter_order(self):
        """Obtiene el orden actual."""
        return self.filter_order

    def set_current_page(self, page):
        """Establece la página actual."""
        self.current_page = page

    def get_current_page(self):
        """Obtiene la página actual."""
        return self.current_page

    def get_products_per_page(self):
        """Obtiene el número de productos por página."""
        return self.products_per_page

if __name__ == "__main__":
    # Prueba rápida del controlador
    controller = InventoryController()
    
    # Cargar resumen
    summary = controller.get_inventory_summary()
    print("Resumen de inventario:", summary)
    
    # Cargar productos (primera página)
    products, total = controller.get_products()
    print(f"Productos obtenidos (pág 1): {len(products)} de {total}")
    
    # Cargar categorías
    categories = controller.get_categories()
    print(f"Categorías cargadas: {len(categories)}")
    
    # Cargar alertas
    alerts = controller.get_inventory_alerts()
    print(f"Alertas de inventario: {alerts['total_alertas']}")