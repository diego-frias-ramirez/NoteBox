"""
NoteBox - Modelo de Productos
Ubicación: model/product_model.py
"""

import sys
import os

model_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(model_path)

from model.database import Database
from utils.logger import Logger

class ProductModel:
    """Modelo para gestionar productos del inventario."""

    def __init__(self):
        self.db = Database()

# EN model/product_model.py

    def get_total_products(self, search="", category_id=None):
        """
        Obtiene el total de productos (para paginación), con filtros opcionales.
        
        Args:
            search (str): Término de búsqueda para nombre o código.
            category_id (int): ID de categoría para filtrar.
        
        Returns:
            int: Número total de productos que coinciden con los filtros.
        """
        query = "SELECT COUNT(*) as total FROM productos p WHERE p.activo = TRUE"
        params = []

        # Aplicar filtro de búsqueda
        if search:
            query += " AND (p.nombre LIKE %s OR p.codigo LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param]) # Usar search_param dos veces para nombre y código

        # Aplicar filtro de categoría
        if category_id:
            query += " AND p.categoria_id = %s"
            params.append(category_id)

        try:
            result = self.db.execute_query(query, params=params, fetch=True)
            total = result[0]['total'] if result else 0
            Logger.info(f"Total productos obtenidos (con filtros): {total}", "PRODUCT_MODEL")
            return total
        except Exception as e:
            Logger.log_error_exception(e, "PRODUCT_MODEL")
            return 0

    def get_products(self, search="", category_id=None, limit=10, offset=0):
        """
        Obtiene productos activos con filtros y paginación.
        
        Args:
            search (str): Término de búsqueda para nombre/código.
            category_id (int): ID de categoría para filtrar.
            limit (int): Límite de resultados por página.
            offset (int): Offset para paginación.
        
        Returns:
            list: Lista de productos activos.
        """
        query = """
            SELECT 
                p.id, p.codigo, p.nombre, p.descripcion, p.categoria_id,
                p.stock, p.stock_minimo, p.precio, p.estado,
                p.dias_sin_movimiento, p.fecha_creacion, p.fecha_actualizacion,
                p.activo, -- <-- INCLUIMOS EL CAMPO ACTIVO
                c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = TRUE -- <-- FILTRO PRINCIPAL POR ACTIVO
        """
        params = []

        where_conditions = []
        if search:
            where_conditions.append("(p.nombre LIKE %s OR p.codigo LIKE %s)")
            search_param = f"%{search}%"
            params.extend([search_param, search_param])
        
        if category_id:
            where_conditions.append("p.categoria_id = %s")
            params.append(category_id)
        
        if where_conditions:
            query += " AND " + " AND ".join(where_conditions)
        
        query += " ORDER BY p.nombre ASC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        try:
            result = self.db.execute_query(query, params=params, fetch=True)
            Logger.info(f"Productos activos obtenidos: {len(result) if result else 0}", "PRODUCT_MODEL")
            return result if result else []
        except Exception as e:
            Logger.error(f"Error obteniendo productos activos: {e}", "PRODUCT_MODEL")
            return []

    def get_product_by_id(self, product_id):
        """
        Obtiene un producto por su ID (si está activo).
        
        Args:
            product_id (int): ID del producto.
        
        Returns:
            dict: Datos del producto o None.
        """
        query = """
            SELECT 
                p.id, p.codigo, p.nombre, p.descripcion, p.categoria_id,
                p.stock, p.stock_minimo, p.precio, p.estado,
                p.dias_sin_movimiento, p.fecha_creacion, p.fecha_actualizacion,
                p.activo, -- <-- INCLUIMOS EL CAMPO ACTIVO
                c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = %s AND p.activo = TRUE -- <-- FILTRO POR ACTIVO
        """
        try:
            result = self.db.execute_query(query, params=(product_id,), fetch=True)
            Logger.info(f"Producto ID {product_id} {'encontrado' if result else 'no encontrado o inactivo'}", "PRODUCT_MODEL")
            return result[0] if result else None
        except Exception as e:
            Logger.error(f"Error obteniendo producto ID {product_id}: {e}", "PRODUCT_MODEL")
            return None

    def get_all_products_including_inactive(self, search="", category_id=None, limit=10, offset=0):
        """
        Obtiene todos los productos (activos e inactivos).
        Útil para vistas de administración completa.
        
        Args:
            search (str): Término de búsqueda.
            category_id (int): ID de categoría.
            limit (int): Límite.
            offset (int): Offset.
        
        Returns:
            list: Lista de productos.
        """
        query = """
            SELECT 
                p.id, p.codigo, p.nombre, p.descripcion, p.categoria_id,
                p.stock, p.stock_minimo, p.precio, p.estado,
                p.dias_sin_movimiento, p.fecha_creacion, p.fecha_actualizacion,
                p.activo, -- <-- INCLUIMOS EL CAMPO ACTIVO
                c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            -- SIN FILTRO POR ACTIVO
        """
        params = []

        where_conditions = []
        if search:
            where_conditions.append("(p.nombre LIKE %s OR p.codigo LIKE %s)")
            search_param = f"%{search}%"
            params.extend([search_param, search_param])
        
        if category_id:
            where_conditions.append("p.categoria_id = %s")
            params.append(category_id)
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        
        query += " ORDER BY p.activo DESC, p.nombre ASC LIMIT %s OFFSET %s" # <-- Ordenar: activos primero
        params.extend([limit, offset])
        
        try:
            result = self.db.execute_query(query, params=params, fetch=True)
            Logger.info(f"Productos totales (activos e inactivos) obtenidos: {len(result) if result else 0}", "PRODUCT_MODEL")
            return result if result else []
        except Exception as e:
            Logger.error(f"Error obteniendo todos los productos: {e}", "PRODUCT_MODEL")
            return []

    def create_product(self, codigo, nombre, descripcion, categoria_id, stock, stock_minimo, precio, estado="Disponible", activo=True):
        """
        Crea un nuevo producto.
        
        Args:
            codigo (str): Código del producto.
            nombre (str): Nombre del producto.
            descripcion (str): Descripción.
            categoria_id (int): ID de la categoría.
            stock (int): Cantidad en stock.
            stock_minimo (int): Stock mínimo.
            precio (float): Precio del producto.
            estado (str): Estado inicial del producto.
            activo (bool): Si el producto está activo o no.
        
        Returns:
            bool: True si se creó, False si falló.
        """
        query = """
            INSERT INTO productos 
            (codigo, nombre, descripcion, categoria_id, stock, stock_minimo, precio, estado, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (codigo, nombre, descripcion, categoria_id, stock, stock_minimo, precio, estado, activo)
        
        try:
            product_id = self.db.execute_query(query, params=params)
            if product_id:
                Logger.success(f"Producto '{nombre}' creado con ID {product_id}", "PRODUCT_MODEL")
                return True
            return False
        except Exception as e:
            Logger.error(f"Error creando producto '{nombre}': {e}", "PRODUCT_MODEL")
            return False

    def update_product(self, product_id, **kwargs):
        """
        Actualiza un producto existente.
        Soporta actualizar el estado 'activo'.
        
        Args:
            product_id (int): ID del producto.
            **kwargs: Campos a actualizar (codigo, nombre, etc.).
        
        Returns:
            bool: True si se actualizó, False si falló.
        """
        allowed_fields = ['codigo', 'nombre', 'descripcion', 'categoria_id', 'stock', 'stock_minimo', 'precio', 'estado', 'activo'] # <-- 'activo' AHORA ESTÁ PERMITIDO
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = %s")
                params.append(value)
        
        if not updates:
            Logger.warning("No hay campos válidos para actualizar", "PRODUCT_MODEL")
            return False
        
        query = f"UPDATE productos SET {', '.join(updates)} WHERE id = %s AND activo = TRUE" # <-- ASEGURAR QUE SEA ACTIVO PARA PODER ACTUALIZAR
        params.append(product_id)
        
        try:
            rows_affected = self.db.execute_query(query, params=params)
            if rows_affected > 0:
                Logger.success(f"Producto ID {product_id} actualizado", "PRODUCT_MODEL")
                return True
            else:
                Logger.warning(f"No se encontró producto ID {product_id} activo para actualizar", "PRODUCT_MODEL")
                return False
        except Exception as e:
            Logger.error(f"Error actualizando producto ID {product_id}: {e}", "PRODUCT_MODEL")
            return False

    def deactivate_product(self, product_id):
        """
        Desactiva un producto (soft delete).
        
        Args:
            product_id (int): ID del producto.
        
        Returns:
            bool: True si se desactivó, False si falló.
        """
        query = "UPDATE productos SET activo = FALSE WHERE id = %s AND activo = TRUE" # <-- ASEGURAR QUE ESTÉ ACTIVO PARA DESACTIVARLO
        try:
            rows_affected = self.db.execute_query(query, params=(product_id,))
            if rows_affected > 0:
                Logger.success(f"Producto ID {product_id} desactivado", "PRODUCT_MODEL")
                return True
            else:
                Logger.warning(f"No se encontró producto ID {product_id} activo para desactivar", "PRODUCT_MODEL")
                return False
        except Exception as e:
            Logger.error(f"Error desactivando producto ID {product_id}: {e}", "PRODUCT_MODEL")
            return False

    def activate_product(self, product_id):
        """
        Activa un producto previamente desactivado.
        
        Args:
            product_id (int): ID del producto.
        
        Returns:
            bool: True si se activó, False si falló.
        """
        query = "UPDATE productos SET activo = TRUE WHERE id = %s AND activo = FALSE" # <-- ASEGURAR QUE ESTÉ INACTIVO PARA ACTIVARLO
        try:
            rows_affected = self.db.execute_query(query, params=(product_id,))
            if rows_affected > 0:
                Logger.success(f"Producto ID {product_id} activado", "PRODUCT_MODEL")
                return True
            else:
                Logger.warning(f"No se encontró producto ID {product_id} inactivo para activar", "PRODUCT_MODEL")
                return False
        except Exception as e:
            Logger.error(f"Error activando producto ID {product_id}: {e}", "PRODUCT_MODEL")
            return False

    def count_products_by_category(self, category_id):
        """
        Cuenta cuántos productos activos hay en una categoría específica.
        
        Args:
            category_id (int): ID de la categoría.
        
        Returns:
            int: Número de productos activos en la categoría.
        """
        query = "SELECT COUNT(*) as count FROM productos WHERE categoria_id = %s AND activo = TRUE" # <-- FILTRO POR ACTIVO Y CATEGORÍA
        try:
            result = self.db.execute_query(query, params=(category_id,), fetch=True)
            count = result[0]['count'] if result else 0
            return count
        except Exception as e:
            Logger.error(f"Error contando productos por categoría {category_id}: {e}", "PRODUCT_MODEL")
            return 0

    def get_all_products_filtered(self, search="", category_id=None):
        """
        Obtiene TODOS los productos activos con filtros (SIN paginación).
        Útil para exportación de inventario.
        
        Args:
            search (str): Término de búsqueda para nombre/código.
            category_id (int): ID de categoría para filtrar.
        
        Returns:
            list: Lista de todos los productos activos que coinciden con los filtros.
        """
        query = """
            SELECT 
                p.id, p.codigo, p.nombre, p.descripcion, p.categoria_id,
                p.stock, p.stock_minimo, p.precio, p.estado,
                p.dias_sin_movimiento, p.fecha_creacion, p.fecha_actualizacion,
                p.activo,
                c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
        """
        params = []

        # Filtro de búsqueda
        if search:
            query += " AND (p.nombre LIKE %s OR p.codigo LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param])
        
        # Filtro de categoría
        if category_id:
            query += " AND p.categoria_id = %s"
            params.append(category_id)
        
        query += " ORDER BY p.nombre ASC"
        
        try:
            result = self.db.execute_query(query, params=params, fetch=True)
            Logger.info(f"Productos para exportar obtenidos: {len(result) if result else 0}", "PRODUCT_MODEL")
            return result if result else []
        except Exception as e:
            Logger.error(f"Error obteniendo productos para exportar: {e}", "PRODUCT_MODEL")
            return []