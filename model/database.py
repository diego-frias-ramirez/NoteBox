"""
NoteBox - Configuración y conexión a la base de datos
"""

import pymysql
import json
from utils.logger import Logger

class Database:
    """Clase para manejar la conexión a la base de datos"""
    
    _connection = None
    _config = None
    
    @classmethod
    def load_config(cls):
        """Carga la configuración de la base de datos"""
        if cls._config is None:
            try:
                with open('config/db_config.json', 'r', encoding='utf-8') as f:
                    cls._config = json.load(f)
            except FileNotFoundError:
                Logger.error("Archivo db_config.json no encontrado", "DATABASE")
                raise
            except json.JSONDecodeError:
                Logger.error("Error al leer db_config.json", "DATABASE")
                raise
        return cls._config
    
    @classmethod
    def get_connection(cls):
        """Obtiene o crea una conexión a la base de datos"""
        try:
            if cls._connection is None or not cls._connection.open:
                config = cls.load_config()
                
                cls._connection = pymysql.connect(
                    host=config['host'],
                    user=config['user'],
                    password=config['password'],
                    database=config['database'],
                    port=config['port'],
                    charset=config.get('charset', 'utf8mb4'),
                    autocommit=config.get('autocommit', True),
                    cursorclass=pymysql.cursors.DictCursor
                )
                
                Logger.success("Conexión a base de datos establecida", "DATABASE")
            
            return cls._connection
            
        except pymysql.Error as e:
            Logger.error(f"Error al conectar a la base de datos: {e}", "DATABASE")
            return None
    
    @classmethod
    def close_connection(cls):
        """Cierra la conexión a la base de datos"""
        if cls._connection and cls._connection.open:
            cls._connection.close()
            cls._connection = None
            Logger.info("Conexión a base de datos cerrada", "DATABASE")
    
    @classmethod
    def test_connection(cls):
        """Prueba la conexión a la base de datos"""
        try:
            conn = cls.get_connection()
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT VERSION()")
                    version = cursor.fetchone()
                    Logger.success(f"MySQL versión: {version['VERSION()']}", "DATABASE")
                return True
            return False
        except pymysql.Error as e:
            Logger.error(f"Test de conexión fallido: {e}", "DATABASE")
            return False
    
    @classmethod
    def create_database(cls):
        """Crea la base de datos si no existe"""
        try:
            config = cls.load_config()
            
            # Conectar sin especificar base de datos
            conn = pymysql.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                port=config['port'],
                charset=config.get('charset', 'utf8mb4')
            )
            
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                Logger.success(f"Base de datos '{config['database']}' verificada/creada", "DATABASE")
            
            conn.close()
            return True
            
        except pymysql.Error as e:
            Logger.error(f"Error al crear base de datos: {e}", "DATABASE")
            return False
    
    @classmethod
    def execute_query(cls, query, params=None, fetch=False):
        """
        Ejecuta una consulta SQL
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (opcional)
            fetch: Si True, retorna los resultados
        
        Returns:
            Si fetch=True: lista de resultados
            Si fetch=False: número de filas afectadas o ID del último registro insertado
        """
        try:
            conn = cls.get_connection()
            if not conn:
                return None
            
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                
                if fetch:
                    return cursor.fetchall()
                else:
                    # Para INSERT, retornar el ID insertado
                    if query.strip().upper().startswith('INSERT'):
                        return cursor.lastrowid
                    # Para UPDATE/DELETE, retornar filas afectadas
                    return cursor.rowcount
                    
        except pymysql.Error as e:
            Logger.error(f"Error ejecutando query: {e}", "DATABASE")
            Logger.debug(f"Query: {query}", "DATABASE")
            return None
    
    @classmethod
    def execute_many(cls, query, params_list):
        """
        Ejecuta una consulta múltiples veces con diferentes parámetros
        
        Args:
            query: Consulta SQL a ejecutar
            params_list: Lista de tuplas con parámetros
        
        Returns:
            Número de filas afectadas
        """
        try:
            conn = cls.get_connection()
            if not conn:
                return 0
            
            with conn.cursor() as cursor:
                cursor.executemany(query, params_list)
                return cursor.rowcount
                
        except pymysql.Error as e:
            Logger.error(f"Error ejecutando executemany: {e}", "DATABASE")
            return 0
    
    @classmethod
    def init_database(cls):
        """Inicializa la base de datos con las tablas necesarias"""
        try:
            # Primero crear la base de datos
            cls.create_database()
            
            # Conectar a la base de datos
            conn = cls.get_connection()
            if not conn:
                return False
            
            # Leer y ejecutar el script SQL
            try:
                with open('database/db_schema.sql', 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                    
                # Separar y ejecutar cada statement
                statements = sql_script.split(';')
                
                with conn.cursor() as cursor:
                    for statement in statements:
                        statement = statement.strip()
                        if statement and not statement.startswith('--'):
                            try:
                                cursor.execute(statement)
                            except pymysql.Error as e:
                                # Ignorar errores de objetos que ya existen
                                if 'already exists' not in str(e):
                                    Logger.warning(f"Advertencia al ejecutar statement: {e}", "DATABASE")
                
                Logger.success("Base de datos inicializada correctamente", "DATABASE")
                return True
                
            except FileNotFoundError:
                Logger.error("Archivo db_schema.sql no encontrado", "DATABASE")
                return False
                
        except Exception as e:
            Logger.error_exception(e, "DATABASE")
            return False