"""
NoteBox - Modelo de Categorías
"""

from model.database import Database
from utils.logger import Logger
from utils.validators import Validators

class CategoryModel:
    """Modelo para manejar categorías de productos"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las categorías activas"""
        query = """
            SELECT id, nombre, descripcion, activo, 
                   fecha_creacion, fecha_actualizacion
            FROM categorias
            WHERE activo = TRUE
            ORDER BY nombre ASC
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            Logger.log_database_operation("SELECT", "categorias", True, f"{len(result) if result else 0} registros")
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "CATEGORY_MODEL")
            return []
    
    @staticmethod
    def get_by_id(categoria_id):
        """Obtiene una categoría por su ID"""
        query = """
            SELECT id, nombre, descripcion, activo,
                   fecha_creacion, fecha_actualizacion
            FROM categorias
            WHERE id = %s
        """
        
        try:
            result = Database.execute_query(query, (categoria_id,), fetch=True)
            if result:
                Logger.log_database_operation("SELECT", "categorias", True)
                return result[0]
            return None
        except Exception as e:
            Logger.error_exception(e, "CATEGORY_MODEL")
            return None
    
    @staticmethod
    def create(nombre, descripcion=""):
        """Crea una nueva categoría"""
        # Validar nombre
        is_valid, msg = Validators.validate_category_name(nombre)
        if not is_valid:
            Logger.warning(f"Validación fallida: {msg}", "CATEGORY_MODEL")
            return False, msg
        
        query = """
            INSERT INTO categorias (nombre, descripcion)
            VALUES (%s, %s)
        """
        
        try:
            result = Database.execute_query(query, (nombre, descripcion))
            if result:
                Logger.log_database_operation("INSERT", "categorias", True, f"ID: {result}")
                return True, result
            return False, "No se pudo crear la categoría"
        except Exception as e:
            Logger.error_exception(e, "CATEGORY_MODEL")
            return False, str(e)
    
    @staticmethod
    def update(categoria_id, nombre, descripcion=""):
        """Actualiza una categoría existente"""
        # Validar nombre
        is_valid, msg = Validators.validate_category_name(nombre)
        if not is_valid:
            Logger.warning(f"Validación fallida: {msg}", "CATEGORY_MODEL")
            return False, msg
        
        query = """
            UPDATE categorias
            SET nombre = %s, descripcion = %s
            WHERE id = %s
        """
        
        try:
            result = Database.execute_query(query, (nombre, descripcion, categoria_id))
            if result:
                Logger.log_database_operation("UPDATE", "categorias", True, f"ID: {categoria_id}")
                return True, "Categoría actualizada correctamente"
            return False, "No se pudo actualizar la categoría"
        except Exception as e:
            Logger.error_exception(e, "CATEGORY_MODEL")
            return False, str(e)
    
    @staticmethod
    def delete(categoria_id):
        """Elimina (desactiva) una categoría"""
        query = """
            UPDATE categorias
            SET activo = FALSE
            WHERE id = %s
        """
        
        try:
            result = Database.execute_query(query, (categoria_id,))
            if result:
                Logger.log_database_operation("UPDATE", "categorias", True, f"Desactivar ID: {categoria_id}")
                return True, "Categoría eliminada correctamente"
            return False, "No se pudo eliminar la categoría"
        except Exception as e:
            Logger.error_exception(e, "CATEGORY_MODEL")
            return False, str(e)
    
    @staticmethod
    def count_products(categoria_id):
        """Cuenta cuántos productos tiene una categoría"""
        query = """
            SELECT COUNT(*) as total
            FROM productos
            WHERE categoria_id = %s AND activo = TRUE
        """
        
        try:
            result = Database.execute_query(query, (categoria_id,), fetch=True)
            if result:
                return result[0]['total']
            return 0
        except Exception as e:
            Logger.error_exception(e, "CATEGORY_MODEL")
            return 0