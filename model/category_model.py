"""
NoteBox - Modelo de Categorías
Ubicación: model/category_model.py
"""

import sys
import os

# Asegurar que el módulo 'model' esté en el path para imports relativos
model_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(model_path)

from model.database import Database
from utils.logger import Logger

class CategoryModel:
    """Modelo para gestionar categorías de productos."""

    def __init__(self):
        self.db = Database()

    def get_all_categories(self):
        """
        Obtiene todas las categorías activas.
        
        Returns:
            list: Lista de diccionarios con datos de categorías o lista vacía.
        """
        query = """
            SELECT id, nombre, descripcion, activo, fecha_creacion
            FROM categorias
            WHERE activo = TRUE -- <-- FILTRO POR ACTIVO
            ORDER BY nombre ASC
        """
        try:
            result = self.db.execute_query(query, fetch=True)
            Logger.info(f"Obtenidas {len(result) if result else 0} categorías activas", "CATEGORY_MODEL")
            return result if result else []
        except Exception as e:
            Logger.error(f"Error obteniendo categorías activas: {e}", "CATEGORY_MODEL")
            return []

    def get_category_by_id(self, category_id):
        """
        Obtiene una categoría por su ID (si está activa).
        
        Args:
            category_id (int): ID de la categoría.
        
        Returns:
            dict: Datos de la categoría o None si no se encuentra o no está activa.
        """
        query = """
            SELECT id, nombre, descripcion, activo, fecha_creacion
            FROM categorias
            WHERE id = %s AND activo = TRUE -- <-- FILTRO POR ACTIVO
        """
        try:
            result = self.db.execute_query(query, params=(category_id,), fetch=True)
            Logger.info(f"Categoría ID {category_id} {'encontrada' if result else 'no encontrada o inactiva'}", "CATEGORY_MODEL")
            return result[0] if result else None
        except Exception as e:
            Logger.error(f"Error obteniendo categoría ID {category_id}: {e}", "CATEGORY_MODEL")
            return None

    def get_all_categories_including_inactive(self):
        """
        Obtiene todas las categorías (activas e inactivas).
        Útil para vistas de administración completa.
        
        Returns:
            list: Lista de diccionarios con datos de categorías.
        """
        query = """
            SELECT id, nombre, descripcion, activo, fecha_creacion
            FROM categorias
            ORDER BY activo DESC, nombre ASC -- <-- Ordenar: activas primero
        """
        try:
            result = self.db.execute_query(query, fetch=True)
            Logger.info(f"Obtenidas {len(result) if result else 0} categorías totales (activas e inactivas)", "CATEGORY_MODEL")
            return result if result else []
        except Exception as e:
            Logger.error(f"Error obteniendo todas las categorías: {e}", "CATEGORY_MODEL")
            return []

    def create_category(self, name, description=""):
        """
        Crea una nueva categoría (por defecto activa).
        
        Args:
            name (str): Nombre de la categoría.
            description (str): Descripción opcional.
        
        Returns:
            bool: True si se creó, False si falló.
        """
        query = """
            INSERT INTO categorias (nombre, descripcion, activo)
            VALUES (%s, %s, TRUE) -- <-- CREAR SIEMPRE COMO ACTIVA POR DEFECTO
        """
        try:
            category_id = self.db.execute_query(query, params=(name, description))
            if category_id:
                Logger.success(f"Categoría '{name}' creada con ID {category_id}", "CATEGORY_MODEL")
                return True
            return False
        except Exception as e:
            Logger.error(f"Error creando categoría '{name}': {e}", "CATEGORY_MODEL")
            return False

    def update_category(self, category_id, name, description="", active=True):
        """
        Actualiza una categoría existente.
        
        Args:
            category_id (int): ID de la categoría.
            name (str): Nuevo nombre.
            description (str): Nueva descripción.
            active (bool): Nuevo estado de activo/inactivo.
        
        Returns:
            bool: True si se actualizó, False si falló.
        """
        query = """
            UPDATE categorias
            SET nombre = %s, descripcion = %s, activo = %s -- <-- ACTUALIZAR ESTADO ACTIVO
            WHERE id = %s
        """
        try:
            rows_affected = self.db.execute_query(query, params=(name, description, active, category_id))
            if rows_affected > 0:
                Logger.success(f"Categoría ID {category_id} actualizada", "CATEGORY_MODEL")
                return True
            else:
                Logger.warning(f"No se encontró categoría ID {category_id} para actualizar", "CATEGORY_MODEL")
                return False
        except Exception as e:
            Logger.error(f"Error actualizando categoría ID {category_id}: {e}", "CATEGORY_MODEL")
            return False

    def delete_category(self, category_id):
        """
        Elimina (desactiva) una categoría. (Soft Delete)
        
        Args:
            category_id (int): ID de la categoría.
        
        Returns:
            bool: True si se desactivó, False si falló.
        """
        # OPCIÓN RECOMENDADA: Soft Delete (cambiar activo a FALSE)
        query = """
            UPDATE categorias
            SET activo = FALSE -- <-- DESACTIVAR EN VEZ DE ELIMINAR
            WHERE id = %s
        """
        # OPCIÓN 2: Eliminación Física (NO RECOMENDADA si hay productos asociados)
        # query = "DELETE FROM categorias WHERE id = %s"
        
        try:
            rows_affected = self.db.execute_query(query, params=(category_id,))
            if rows_affected > 0:
                Logger.success(f"Categoría ID {category_id} desactivada", "CATEGORY_MODEL")
                return True
            else:
                Logger.warning(f"No se encontró categoría ID {category_id} para desactivar", "CATEGORY_MODEL")
                return False
        except Exception as e:
            Logger.error(f"Error desactivando categoría ID {category_id}: {e}", "CATEGORY_MODEL")
            return False

    def count_active_categories(self):
        """
        Cuenta cuántas categorías activas hay.
        
        Returns:
            int: Número de categorías activas.
        """
        query = "SELECT COUNT(*) as count FROM categorias WHERE activo = TRUE"
        try:
            result = self.db.execute_query(query, fetch=True)
            count = result[0]['count'] if result else 0
            Logger.info(f"Categorías activas contadas: {count}", "CATEGORY_MODEL")
            return count
        except Exception as e:
            Logger.error(f"Error contando categorías activas: {e}", "CATEGORY_MODEL")
            return 0

if __name__ == "__main__":
    # Prueba rápida
    cm = CategoryModel()
    cats = cm.get_all_categories()
    from utils.logger import Logger
    Logger.info(f"Categorías activas: {len(cats)}", "CATEGORY_MODEL")
    for c in cats:
        Logger.info(f"- {c['id']}: {c['nombre']} - Activo: {c['activo']}", "CATEGORY_MODEL")