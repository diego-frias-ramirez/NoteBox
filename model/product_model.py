"""
NoteBox - Modelo de Productos
"""

from model.database import Database
from utils.logger import Logger
from utils.validators import Validators

class ProductModel:
    """Modelo para manejar productos del inventario"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los productos activos con información de categoría"""
        query = """
            SELECT * FROM productos_completos
            WHERE activo = TRUE
            ORDER BY nombre ASC
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            Logger.log_database_operation("SELECT", "productos", True, f"{len(result) if result else 0} registros")
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return []
    
    @staticmethod
    def get_by_id(producto_id):
        """Obtiene un producto por su ID"""
        query = """
            SELECT * FROM productos_completos
            WHERE id = %s
        """
        
        try:
            result = Database.execute_query(query, (producto_id,), fetch=True)
            if result:
                Logger.log_database_operation("SELECT", "productos", True)
                return result[0]
            return None
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return None
    
    @staticmethod
    def get_by_category(categoria_id):
        """Obtiene todos los productos de una categoría"""
        query = """
            SELECT * FROM productos_completos
            WHERE categoria_id = %s AND activo = TRUE
            ORDER BY nombre ASC
        """
        
        try:
            result = Database.execute_query(query, (categoria_id,), fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return []
    
    @staticmethod
    def search(search_term):
        """Busca productos por nombre o código"""
        query = """
            SELECT * FROM productos_completos
            WHERE activo = TRUE 
            AND (nombre LIKE %s OR codigo LIKE %s)
            ORDER BY nombre ASC
        """
        
        search_pattern = f"%{search_term}%"
        
        try:
            result = Database.execute_query(query, (search_pattern, search_pattern), fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return []
    
    @staticmethod
    def create(data):
        """Crea un nuevo producto"""
        # Validar datos
        is_valid, msg = Validators.validate_product_data(data)
        if not is_valid:
            Logger.warning(f"Validación fallida: {msg}", "PRODUCT_MODEL")
            return False, msg
        
        query = """
            INSERT INTO productos 
            (codigo, nombre, descripcion, categoria_id, precio, stock, 
             stock_minimo, unidad_medida, proveedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            data.get('codigo', ''),
            data['nombre'],
            data.get('descripcion', ''),
            data['categoria_id'],
            data['precio'],
            data.get('stock', 0),
            data.get('stock_minimo', 10),
            data.get('unidad_medida', 'pieza'),
            data.get('proveedor', '')
        )
        
        try:
            result = Database.execute_query(query, params)
            if result:
                Logger.log_database_operation("INSERT", "productos", True, f"ID: {result}")
                return True, result
            return False, "No se pudo crear el producto"
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return False, str(e)
    
    @staticmethod
    def update(producto_id, data):
        """Actualiza un producto existente"""
        # Validar datos
        is_valid, msg = Validators.validate_product_data(data)
        if not is_valid:
            Logger.warning(f"Validación fallida: {msg}", "PRODUCT_MODEL")
            return False, msg
        
        query = """
            UPDATE productos
            SET codigo = %s, nombre = %s, descripcion = %s, categoria_id = %s,
                precio = %s, stock = %s, stock_minimo = %s, 
                unidad_medida = %s, proveedor = %s
            WHERE id = %s
        """
        
        params = (
            data.get('codigo', ''),
            data['nombre'],
            data.get('descripcion', ''),
            data['categoria_id'],
            data['precio'],
            data.get('stock', 0),
            data.get('stock_minimo', 10),
            data.get('unidad_medida', 'pieza'),
            data.get('proveedor', ''),
            producto_id
        )
        
        try:
            result = Database.execute_query(query, params)
            if result:
                Logger.log_database_operation("UPDATE", "productos", True, f"ID: {producto_id}")
                return True, "Producto actualizado correctamente"
            return False, "No se pudo actualizar el producto"
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return False, str(e)
    
    @staticmethod
    def delete(producto_id):
        """Elimina (desactiva) un producto"""
        query = """
            UPDATE productos
            SET activo = FALSE
            WHERE id = %s
        """
        
        try:
            result = Database.execute_query(query, (producto_id,))
            if result:
                Logger.log_database_operation("UPDATE", "productos", True, f"Desactivar ID: {producto_id}")
                return True, "Producto eliminado correctamente"
            return False, "No se pudo eliminar el producto"
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return False, str(e)
    
    @staticmethod
    def update_stock(producto_id, nueva_cantidad):
        """Actualiza el stock de un producto"""
        query = """
            UPDATE productos
            SET stock = %s
            WHERE id = %s
        """
        
        try:
            result = Database.execute_query(query, (nueva_cantidad, producto_id))
            if result:
                Logger.log_database_operation("UPDATE", "productos", True, f"Stock actualizado ID: {producto_id}")
                return True, "Stock actualizado correctamente"
            return False, "No se pudo actualizar el stock"
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return False, str(e)
    
    @staticmethod
    def get_low_stock():
        """Obtiene productos con stock bajo"""
        query = """
            SELECT * FROM alertas_stock_bajo
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return []
    
    @staticmethod
    def get_statistics():
        """Obtiene estadísticas del inventario"""
        query = """
            CALL obtener_resumen_inventario()
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            if result:
                return result[0]
            return None
        except Exception as e:
            Logger.error_exception(e, "PRODUCT_MODEL")
            return None