from database import Database

class AuthController:
    def __init__(self):
        self.db = Database()
        self.db.connect()
    
    def login(self, username, password):
        """
        Valida las credenciales del usuario
        Retorna: (éxito: bool, mensaje: str, user_data: dict)
        """
        if not username or not password:
            return (False, "Por favor ingresa usuario y contraseña", None)
        
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        user = self.db.fetch_one(query, (username, password))
        
        if user:
            return (True, "Login exitoso", user)
        else:
            return (False, "Usuario o contraseña incorrectos", None)
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        self.db.disconnect()