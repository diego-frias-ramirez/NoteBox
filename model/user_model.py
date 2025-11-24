"""
NoteBox - Modelo de Usuarios
"""

from model.database import Database
from utils.logger import Logger
from datetime import datetime

class UserModel:
    """Modelo para manejar usuarios del sistema"""
    
    @staticmethod
    def authenticate(username, password):
        """
        Autentica un usuario con sus credenciales
        
        Args:
            username: Nombre de usuario
            password: Contraseña (en texto plano por ahora)
        
        Returns:
            dict: Datos del usuario si es válido, None si no
        """
        query = """
            SELECT id, usuario, nombre, email, rol, estado, ultimo_acceso
            FROM usuarios
            WHERE usuario = %s AND contrasena = %s
        """
        
        try:
            result = Database.execute_query(query, (username, password), fetch=True)
            
            if result:
                Logger.log_database_operation(
                    "SELECT", "usuarios", True, 
                    f"Autenticación usuario: {username}"
                )
                return result[0]
            else:
                Logger.log_database_operation(
                    "SELECT", "usuarios", False,
                    f"Credenciales inválidas para: {username}"
                )
                return None
                
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return None
    
    @staticmethod
    def get_all():
        """Obtiene todos los usuarios"""
        query = """
            SELECT id, usuario, nombre, email, rol, estado, 
                   ultimo_acceso, fecha_creacion
            FROM usuarios
            ORDER BY nombre ASC
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            Logger.log_database_operation(
                "SELECT", "usuarios", True,
                f"{len(result) if result else 0} usuarios"
            )
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return []
    
    @staticmethod
    def get_by_id(user_id):
        """Obtiene un usuario por su ID"""
        query = """
            SELECT id, usuario, nombre, email, rol, estado,
                   ultimo_acceso, fecha_creacion
            FROM usuarios
            WHERE id = %s
        """
        
        try:
            result = Database.execute_query(query, (user_id,), fetch=True)
            if result:
                return result[0]
            return None
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return None
    
    @staticmethod
    def update_last_access(user_id):
        """Actualiza la fecha de último acceso del usuario"""
        query = """
            UPDATE usuarios
            SET ultimo_acceso = %s
            WHERE id = %s
        """
        
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = Database.execute_query(query, (now, user_id))
            
            if result:
                Logger.log_database_operation(
                    "UPDATE", "usuarios", True,
                    f"Último acceso actualizado - ID: {user_id}"
                )
                return True
            return False
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return False
    
    @staticmethod
    def get_active_users():
        """Obtiene solo los usuarios activos"""
        query = """
            SELECT id, usuario, nombre, email, rol
            FROM usuarios
            WHERE estado = 'Activo'
            ORDER BY nombre ASC
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return []
    
    @staticmethod
    def count_by_role():
        """Cuenta usuarios por rol"""
        query = """
            SELECT 
                rol,
                COUNT(*) as total,
                SUM(CASE WHEN estado = 'Activo' THEN 1 ELSE 0 END) as activos
            FROM usuarios
            GROUP BY rol
        """
        
        try:
            result = Database.execute_query(query, fetch=True)
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return []

    # EN model/user_model.py

    def get_users(self, search="", role=None, limit=5, offset=0):
        """
        Obtiene usuarios con paginación y filtros.
        """
        query = """
            SELECT id, usuario as username, nombre, email, rol, estado, ultimo_acceso
            FROM usuarios
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (nombre LIKE %s OR usuario LIKE %s OR email LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])

        if role:
            query += " AND rol = %s"
            params.append(role)

        query += " ORDER BY nombre ASC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        try:
            result = self.db.execute_query(query, params=params, fetch=True)
            Logger.info(f"Usuarios obtenidos: {len(result) if result else 0}", "USER_MODEL")
            return result if result else []
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return []

    def get_total_users(self, search="", role=None):
        """
        Obtiene el total de usuarios (para paginación).
        """
        query = "SELECT COUNT(*) as total FROM usuarios WHERE 1=1"
        params = []

        if search:
            query += " AND (nombre LIKE %s OR usuario LIKE %s OR email LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])

        if role:
            query += " AND rol = %s"
            params.append(role)

        try:
            result = self.db.execute_query(query, params=params, fetch=True)
            total = result[0]['total'] if result else 0
            Logger.info(f"Total de usuarios: {total}", "USER_MODEL")
            return total
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return 0

    def get_users_count_by_role(self, role):
        """
        Obtiene el número de usuarios por rol.
        """
        query = "SELECT COUNT(*) as count FROM usuarios WHERE rol = %s"
        try:
            result = self.db.execute_query(query, params=(role,), fetch=True)
            count = result[0]['count'] if result else 0
            Logger.info(f"Usuarios con rol '{role}': {count}", "USER_MODEL")
            return count
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return 0

    def create_user(self, nombre, username, email, password, rol):
        """
        Crea un nuevo usuario.
        """
        # Hashear la contraseña (usa una librería segura en producción)
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        query = """
            INSERT INTO usuarios (usuario, contrasena, nombre, email, rol)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (username, hashed_password, nombre, email, rol)

        try:
            user_id = self.db.execute_query(query, params=params)
            if user_id:
                Logger.success(f"Usuario '{nombre}' creado con ID {user_id}", "USER_MODEL")
                return True
            return False
        except Exception as e:
            Logger.error_exception(e, "USER_MODEL")
            return False