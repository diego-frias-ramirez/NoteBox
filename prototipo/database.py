import pymysql
from pymysql.cursors import DictCursor

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '' 
        self.database = 'POO_Proyecto_parcial2'
        self.connection = None
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=DictCursor
            )
            return True
        except pymysql.Error as e:
            print(f"Error conectando a la base de datos: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta INSERT, UPDATE o DELETE"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return True
        except pymysql.Error as e:
            print(f"Error ejecutando query: {e}")
            self.connection.rollback()
            return False
    
    def fetch_all(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna todos los resultados"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error obteniendo datos: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna un solo resultado"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except pymysql.Error as e:
            print(f"Error obteniendo dato: {e}")
            return None