from database import Database

class UserController:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def crear_usuario(self, username, nombre, correo, password):
        """
        Crea un nuevo usuario
        Retorna: (éxito: bool, mensaje: str)
        """
        if not all([username, nombre, correo, password]):
            return (False, "Todos los campos son obligatorios")
        
        # Verificar si el usuario ya existe
        query_check = "SELECT * FROM usuarios WHERE username = %s OR correo = %s"
        existing = self.db.fetch_one(query_check, (username, correo))
        
        if existing:
            return (False, "El usuario o correo ya existe")
        
        query = """
            INSERT INTO usuarios (username, nombre, correo, password) 
            VALUES (%s, %s, %s, %s)
        """
        
        if self.db.execute_query(query, (username, nombre, correo, password)):
            return (True, "Usuario creado exitosamente")
        else:
            return (False, "Error al crear usuario")
    
    def obtener_usuarios(self):
        """
        Obtiene todos los usuarios
        Retorna: lista de diccionarios con datos de usuarios
        """
        query = "SELECT id_usuario, username, nombre, correo, fecha_registro FROM usuarios"
        return self.db.fetch_all(query)
    
    def obtener_usuario(self, id_usuario):
        """
        Obtiene un usuario por ID
        Retorna: diccionario con datos del usuario o None
        """
        query = "SELECT * FROM usuarios WHERE id_usuario = %s"
        return self.db.fetch_one(query, (id_usuario,))
    
    def modificar_usuario(self, id_usuario, username, nombre, correo, password=None):
        """
        Modifica un usuario existente
        Retorna: (éxito: bool, mensaje: str)
        """
        if not all([id_usuario, username, nombre, correo]):
            return (False, "Todos los campos son obligatorios")
        
        # Verificar si el username o correo ya existen en otro usuario
        query_check = """
            SELECT * FROM usuarios 
            WHERE (username = %s OR correo = %s) AND id_usuario != %s
        """
        existing = self.db.fetch_one(query_check, (username, correo, id_usuario))
        
        if existing:
            return (False, "El usuario o correo ya existe en otro registro")
        
        if password:
            query = """
                UPDATE usuarios 
                SET username = %s, nombre = %s, correo = %s, password = %s
                WHERE id_usuario = %s
            """
            params = (username, nombre, correo, password, id_usuario)
        else:
            query = """
                UPDATE usuarios 
                SET username = %s, nombre = %s, correo = %s
                WHERE id_usuario = %s
            """
            params = (username, nombre, correo, id_usuario)
        
        if self.db.execute_query(query, params):
            return (True, "Usuario modificado exitosamente")
        else:
            return (False, "Error al modificar usuario")
    
    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario
        Retorna: (éxito: bool, mensaje: str)
        """
        if not id_usuario:
            return (False, "ID de usuario no válido")
        
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        
        if self.db.execute_query(query, (id_usuario,)):
            return (True, "Usuario eliminado exitosamente")
        else:
            return (False, "Error al eliminar usuario")
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        self.db.disconnect()