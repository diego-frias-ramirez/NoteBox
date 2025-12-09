"""
NoteBox - Sistema de Gestión de Inventario
Módulo de conexión a la base de datos MySQL usando PyMySQL
"""

import pymysql
import json
import os
from utils.logger import Logger

class Database:
    """Clase para gestionar la conexión a la base de datos MySQL."""

    _connection = None
    _config = None

    @classmethod
    def load_config(cls):
        """Carga la configuración de la base de datos desde db_config.json."""
        if cls._config is None:
            try:
                # Obtener la ruta absoluta del directorio actual (donde está database.py)
                current_dir = os.path.dirname(os.path.abspath(__file__))
                
                # Construir la ruta absoluta al archivo db_config.json
                db_config_path = os.path.join(current_dir, '..', 'config', 'db_config.json')
                
                with open(db_config_path, 'r', encoding='utf-8') as f:
                    cls._config = json.load(f)
                    
                # Seleccionar el entorno actual
                current_env = cls._config.get('current_environment', 'development')
                cls._config = cls._config[current_env]
                
            except FileNotFoundError:
                error_msg = "Archivo db_config.json no encontrado"
                Logger.error(error_msg, "DATABASE")
                raise Exception(error_msg)
            except json.JSONDecodeError:
                error_msg = "Error al leer db_config.json"
                Logger.error(error_msg, "DATABASE")
                raise Exception(error_msg)
            except KeyError:
                error_msg = "Entorno actual no definido en db_config.json"
                Logger.error(error_msg, "DATABASE")
                raise Exception(error_msg)
        
        return cls._config

    @classmethod
    def get_connection(cls):
        """Obtiene o crea una conexión a la base de datos."""
        try:
            config = cls.load_config()
            
            # Verificar si la conexión existe y está abierta
            if cls._connection is None or not cls._connection.open:
                cls._connection = pymysql.connect(
                    host=config['database']['host'],
                    user=config['database']['user'],
                    password=config['database']['password'],
                    database=config['database']['database'],
                    port=config['database']['port'],
                    charset=config['database'].get('charset', 'utf8mb4'),
                    autocommit=config['database'].get('autocommit', True),
                    cursorclass=pymysql.cursors.DictCursor,
                    connect_timeout=config['database'].get('connect_timeout', 10)
                )
                Logger.success("Conexión a base de datos establecida", "DATABASE")
            else:
                 # Si ya existe, verificar que esté viva
                 try:
                     cls._connection.ping(reconnect=True)
                 except pymysql.Error:
                     # Si falla el ping, intentar reconectar
                     Logger.warning("Conexión perdida, reconectando...", "DATABASE")
                     cls._connection = pymysql.connect(
                        host=config['database']['host'],
                        user=config['database']['user'],
                        password=config['database']['password'],
                        database=config['database']['database'],
                        port=config['database']['port'],
                        charset=config['database'].get('charset', 'utf8mb4'),
                        autocommit=config['database'].get('autocommit', True),
                        cursorclass=pymysql.cursors.DictCursor,
                        connect_timeout=config['database'].get('connect_timeout', 10)
                     )
            
            return cls._connection
            
        except pymysql.Error as e:
            error_msg = f"Error al conectar a la base de datos: {e}"
            Logger.error(error_msg, "DATABASE")
            raise Exception(error_msg)

    @classmethod
    def close_connection(cls):
        """Cierra la conexión a la base de datos."""
        if cls._connection and cls._connection.open:
            cls._connection.close()
            cls._connection = None
            Logger.info("Conexión a base de datos cerrada", "DATABASE")

    @classmethod
    def test_connection(cls):
        """Prueba la conexión a la base de datos."""
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
            error_msg = f"Test de conexión fallido: {e}"
            Logger.error(error_msg, "DATABASE")
            return False

    @classmethod
    def create_database(cls):
        """Crea la base de datos si no existe."""
        try:
            config = cls.load_config()
            
            # Conectar sin especificar base de datos
            conn = pymysql.connect(
                host=config['database']['host'],
                user=config['database']['user'],
                password=config['database']['password'],
                port=config['database']['port'],
                charset=config['database'].get('charset', 'utf8mb4'),
                connect_timeout=config['database'].get('connect_timeout', 10)
            )
            
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                Logger.success(f"Base de datos '{config['database']['database']}' verificada/creada", "DATABASE")
            
            conn.close()
            return True
            
        except pymysql.Error as e:
            error_msg = f"Error al crear base de datos: {e}"
            Logger.error(error_msg, "DATABASE")
            return False

    @classmethod
    def execute_query(cls, query, params=None, fetch=False):
        """
        Ejecuta una consulta SQL.
        
        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple/list/dict, optional): Parámetros para la consulta.
            fetch (bool): Si es True, retorna los resultados.
        
        Returns:
            list/dict/int: Resultados de la consulta, número de filas afectadas o ID del último registro insertado.
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
            error_msg = f"Error ejecutando query: {e}\nQuery: {query}"
            Logger.error(error_msg, "DATABASE")
            raise Exception(error_msg)

    @classmethod
    def execute_many(cls, query, params_list):
        """
        Ejecuta una consulta múltiples veces con diferentes parámetros.
        
        Args:
            query (str): Consulta SQL a ejecutar.
            params_list (list of tuples): Lista de tuplas con parámetros.
        
        Returns:
            int: Número de filas afectadas.
        """
        try:
            conn = cls.get_connection()
            if not conn:
                return 0
            
            with conn.cursor() as cursor:
                cursor.executemany(query, params_list)
                return cursor.rowcount
                
        except pymysql.Error as e:
            error_msg = f"Error ejecutando executemany: {e}\nQuery: {query}"
            Logger.error(error_msg, "DATABASE")
            raise Exception(error_msg)

    @classmethod
    def init_database(cls):
        """Inicializa la base de datos con las tablas necesarias."""
        try:
            # Primero crear la base de datos
            cls.create_database()
            
            # Conectar a la base de datos
            conn = cls.get_connection()
            if not conn:
                return False
            
            # Construir la ruta absoluta al archivo db_schema.sql
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sql_script_path = os.path.join(current_dir, 'database', 'db_schema.sql')
            
            # Leer y ejecutar el script SQL
            with open(sql_script_path, 'r', encoding='utf-8') as f:
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
            error_msg = "Archivo db_schema.sql no encontrado"
            Logger.error(error_msg, "DATABASE")
            return False
                
        except Exception as e:
            Logger.error_exception(e, "DATABASE")
            return False

# Inicializar la conexión al cargar el módulo
try:
    Database.get_connection()
except Exception as e:
    Logger.error(f"Error al inicializar la base de datos: {e}", "DATABASE")