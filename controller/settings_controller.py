"""
NoteBox - Controlador del Módulo de Configuraciones
Ubicación: controller/settings_controller.py
"""

import json
import os
from datetime import datetime
from model.database import Database
from utils.logger import Logger
from utils.helpers import Helpers

class SettingsController:
    """Controlador para gestionar configuraciones del sistema."""
    
    def __init__(self, user_data):
        self.user_data = user_data
        self.config_dir = "config"
        self.app_settings_file = os.path.join(self.config_dir, "app_settings.json")
        self.db_config_file = os.path.join(self.config_dir, "db_config.json")

    def get_system_info(self):
        """Obtiene información general del sistema."""
        try:
            # Información de la base de datos
            query = "SELECT VERSION() as version"
            result = Database.execute_query(query, fetch=True)
            db_version = result[0]['version'] if result else "Desconocida"
            
            # Información de configuración
            app_config = self.load_app_settings()
            
            # Estadísticas de uso
            stats = self.get_usage_stats()
            
            return {
                'app_name': app_config.get('application', {}).get('name', 'NoteBox'),
                'app_version': app_config.get('application', {}).get('version', 'v1.0.0'),
                'company': app_config.get('application', {}).get('company_name', 'Papelería Valeria'),
                'db_version': db_version,
                'total_products': stats.get('total_products', 0),
                'total_users': stats.get('total_users', 0),
                'total_movements': stats.get('total_movements', 0),
                'last_backup': self.get_last_backup_date()
            }
        except Exception as e:
            Logger.error(f"Error obteniendo información del sistema: {e}", "SETTINGS_CONTROLLER")
            return {}

    def get_usage_stats(self):
        """Obtiene estadísticas de uso del sistema."""
        try:
            # Total de productos
            query_products = "SELECT COUNT(*) as total FROM productos WHERE activo = TRUE"
            products = Database.execute_query(query_products, fetch=True)
            
            # Total de usuarios
            query_users = "SELECT COUNT(*) as total FROM usuarios WHERE estado = 'Activo'"
            users = Database.execute_query(query_users, fetch=True)
            
            # Total de movimientos
            query_movements = "SELECT COUNT(*) as total FROM movimientos"
            movements = Database.execute_query(query_movements, fetch=True)
            
            return {
                'total_products': products[0]['total'] if products else 0,
                'total_users': users[0]['total'] if users else 0,
                'total_movements': movements[0]['total'] if movements else 0
            }
        except Exception as e:
            Logger.error(f"Error obteniendo estadísticas: {e}", "SETTINGS_CONTROLLER")
            return {}

    def get_last_backup_date(self):
        """Obtiene la fecha del último backup."""
        try:
            backups_dir = "exports/backups"
            if not os.path.exists(backups_dir):
                return "Nunca"
            
            files = [f for f in os.listdir(backups_dir) if f.endswith('.json') or f.endswith('.sql')]
            if not files:
                return "Nunca"
            
            latest = max(files, key=lambda x: os.path.getmtime(os.path.join(backups_dir, x)))
            timestamp = os.path.getmtime(os.path.join(backups_dir, latest))
            return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")
        except Exception as e:
            Logger.error(f"Error obteniendo fecha de backup: {e}", "SETTINGS_CONTROLLER")
            return "Error"

    def get_last_backup_timestamp(self):
        """Devuelve el timestamp (float) del último backup o None si no existe."""
        try:
            backups_dir = "exports/backups"
            if not os.path.exists(backups_dir):
                return None
            files = [f for f in os.listdir(backups_dir) if f.endswith('.json') or f.endswith('.sql')]
            if not files:
                return None
            latest = max(files, key=lambda x: os.path.getmtime(os.path.join(backups_dir, x)))
            timestamp = os.path.getmtime(os.path.join(backups_dir, latest))
            return timestamp
        except Exception as e:
            Logger.error(f"Error obteniendo timestamp de backup: {e}", "SETTINGS_CONTROLLER")
            return None

    def load_app_settings(self):
        """Carga la configuración de la aplicación."""
        try:
            if os.path.exists(self.app_settings_file):
                with open(self.app_settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            Logger.error(f"Error cargando configuración: {e}", "SETTINGS_CONTROLLER")
            return {}

    def save_app_settings(self, settings):
        """Guarda la configuración de la aplicación."""
        try:
            with open(self.app_settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            Logger.success("Configuración guardada correctamente", "SETTINGS_CONTROLLER")
            return True, "Configuración guardada correctamente"
        except Exception as e:
            Logger.error(f"Error guardando configuración: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def get_company_settings(self):
        """Obtiene configuración de la empresa."""
        try:
            query = """
                SELECT 
                    nombre_negocio, tipo_negocio, moneda, direccion,
                    telefono, email_contacto, color_primario, color_secundario
                FROM configuracion
                LIMIT 1
            """
            result = Database.execute_query(query, fetch=True)
            return result[0] if result else {}
        except Exception as e:
            Logger.error(f"Error obteniendo configuración de empresa: {e}", "SETTINGS_CONTROLLER")
            return {}

    def update_company_settings(self, data):
        """Actualiza configuración de la empresa."""
        try:
            query = """
                UPDATE configuracion
                SET nombre_negocio = %s,
                    tipo_negocio = %s,
                    direccion = %s,
                    telefono = %s,
                    email_contacto = %s
                WHERE id = 1
            """
            params = (
                data.get('nombre_negocio'),
                data.get('tipo_negocio'),
                data.get('direccion'),
                data.get('telefono'),
                data.get('email_contacto')
            )
            
            result = Database.execute_query(query, params)
            
            if result:
                Logger.success("Configuración de empresa actualizada", "SETTINGS_CONTROLLER")
                return True, "Configuración actualizada correctamente"
            return False, "No se pudo actualizar la configuración"
        except Exception as e:
            Logger.error(f"Error actualizando configuración: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def get_alert_settings(self):
        """Obtiene configuración de alertas."""
        try:
            app_config = self.load_app_settings()
            return app_config.get('alerts', {
                'stock_bajo_threshold': 10,
                'dias_sin_movimiento': 30,
                'enable_stock_alerts': True,
                'enable_inactive_product_alerts': True
            })
        except Exception as e:
            Logger.error(f"Error obteniendo configuración de alertas: {e}", "SETTINGS_CONTROLLER")
            return {}

    def update_alert_settings(self, data):
        """Actualiza configuración de alertas."""
        try:
            app_config = self.load_app_settings()
            
            if 'alerts' not in app_config:
                app_config['alerts'] = {}
            
            app_config['alerts']['stock_bajo_threshold'] = int(data.get('stock_bajo_threshold', 10))
            app_config['alerts']['dias_sin_movimiento'] = int(data.get('dias_sin_movimiento', 30))
            app_config['alerts']['enable_stock_alerts'] = data.get('enable_stock_alerts', True)
            app_config['alerts']['enable_inactive_product_alerts'] = data.get('enable_inactive_product_alerts', True)
            
            return self.save_app_settings(app_config)
        except Exception as e:
            Logger.error(f"Error actualizando alertas: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def get_backup_settings(self):
        """Obtiene configuración de backups."""
        try:
            app_config = self.load_app_settings()
            return app_config.get('backup', {
                'auto_backup': True,
                'backup_frequency_days': 7,
                'retention_days': 30
            })
        except Exception as e:
            Logger.error(f"Error obteniendo configuración de backup: {e}", "SETTINGS_CONTROLLER")
            return {}

    def update_backup_settings(self, data):
        """Actualiza configuración de backups."""
        try:
            app_config = self.load_app_settings()
            
            if 'backup' not in app_config:
                app_config['backup'] = {}
            
            app_config['backup']['auto_backup'] = data.get('auto_backup', True)
            app_config['backup']['backup_frequency_days'] = int(data.get('backup_frequency_days', 7))
            app_config['backup']['retention_days'] = int(data.get('retention_days', 30))
            
            return self.save_app_settings(app_config)
        except Exception as e:
            Logger.error(f"Error actualizando backup: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def update_ui_colors(self, colors):
        """Actualiza colores en la sección `ui.colors` de app_settings.json."""
        try:
            app_config = self.load_app_settings()
            if 'ui' not in app_config:
                app_config['ui'] = {}
            if 'colors' not in app_config['ui']:
                app_config['ui']['colors'] = {}

            app_config['ui']['colors']['primary'] = colors.get('primary', '#00B4D8')
            app_config['ui']['colors']['secondary'] = colors.get('secondary', '#10B981')
            app_config['ui']['colors']['sidebar'] = colors.get('sidebar', '#1E293B')

            success, msg = self.save_app_settings(app_config)
            return success, msg
        except Exception as e:
            Logger.error(f"Error actualizando colores UI: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def create_backup(self, filepath=None):
        """Crea un backup manual de la base de datos."""
        try:
            import subprocess
            import shutil

            # Cargar configuración de BD
            db_config = self.load_db_config()
            if not db_config:
                return False, "No se pudo cargar la configuración de BD"

            # Determinar entorno (use 'current_environment' si está presente)
            env_name = db_config.get('current_environment', 'development')
            env = db_config.get(env_name, db_config.get('development', {}))
            db_info = env.get('database', {})

            host = db_info.get('host', 'localhost')
            user = db_info.get('user', 'root')
            password = db_info.get('password', '')
            database = db_info.get('database', 'notebox_db')

            if filepath:
                backup_file = filepath
                # Ensure dir exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                backups_dir = os.path.dirname(filepath) # Used for retention cleanup later
            else:
                # Carpeta de backups (intentar usar paths de config si existen)
                backups_path_cfg = env.get('paths', {}).get('backups') or db_config.get('development', {}).get('paths', {}).get('backups')
                if backups_path_cfg:
                    # Resolver ruta relativa respecto al directorio de trabajo actual
                    backups_dir = os.path.normpath(os.path.join(os.getcwd(), backups_path_cfg))
                else:
                    backups_dir = os.path.join(os.getcwd(), 'exports', 'backups')

                os.makedirs(backups_dir, exist_ok=True)

                # Nombre del archivo de backup
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(backups_dir, f"backup_notebox_{timestamp}.sql")

            # Verificar que mysqldump esté disponible
            mysqldump_path = shutil.which('mysqldump')
            if not mysqldump_path:
                # Intentar fallback: exportar usando conexión Python (sin mysqldump)
                try:
                    # Asegurar conexión fresca
                    conn = Database.get_connection()
                    
                    with conn.cursor() as cursor:
                        cursor.execute("SHOW TABLES")
                        rows = cursor.fetchall()
                        tables = []
                        for r in rows:
                             if r and list(r.values()):
                                 tables.append(list(r.values())[0])
                        
                        if not tables:
                             Logger.warning("Backup fallback: No se encontraron tablas", "SETTINGS_CONTROLLER")
                             
                        with open(backup_file, 'w', encoding='utf-8') as f:
                            for table in tables:
                                try:
                                    cursor.execute(f"SHOW CREATE TABLE `{table}`")
                                    create_row = cursor.fetchone()
                                    if not create_row: continue
                                    
                                    # obtener la columna CREATE TABLE
                                    create_stmt = None
                                    for v in create_row.values():
                                        if isinstance(v, str) and v.strip().upper().startswith('CREATE'):
                                            create_stmt = v
                                            break
                                    if not create_stmt: continue

                                    f.write(f"-- Table: {table}\n")
                                    f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
                                    f.write(create_stmt + ";\n\n")

                                    cursor.execute(f"SELECT * FROM `{table}`")
                                    rows = cursor.fetchall()
                                    if rows:
                                        cols = list(rows[0].keys())
                                        for r in rows:
                                            vals = []
                                            for c in cols:
                                                v = r.get(c)
                                                if v is None:
                                                    vals.append('NULL')
                                                elif isinstance(v, (int, float)):
                                                    vals.append(str(v))
                                                else:
                                                    escaped = str(v).replace("'", "''").replace("\\", "\\\\").replace("\n", "\\n")
                                                    vals.append(f"'{escaped}'")
                                            cols_escaped = ', '.join([f'`{c}`' for c in cols])
                                            f.write(f"INSERT INTO `{table}` ({cols_escaped}) VALUES ({', '.join(vals)});\n")
                                    f.write('\n')
                                except Exception as e:
                                    Logger.error(f"Error backup tabla {table}: {e}", "SETTINGS_CONTROLLER")
                                    continue

                    Logger.success(f"Backup creado (fallback SQL): {backup_file}", "SETTINGS_CONTROLLER")
                    return True, backup_file
                except Exception as e:
                    msg = f"mysqldump no disponible y fallback falló: {e}"
                    Logger.error(msg, "SETTINGS_CONTROLLER")
                    return False, msg

            # Construir comando como lista y redirigir stdout al archivo
            cmd = [mysqldump_path, '-h', host, '-u', user]
            if password:
                # concatenar -pPASSWORD (mysqldump exige directamente sin espacio)
                cmd.append(f'-p{password}')
            cmd.append(database)

            try:
                with open(backup_file, 'wb') as out_f:
                    proc = subprocess.run(cmd, stdout=out_f, stderr=subprocess.PIPE)

                if proc.returncode == 0 and os.path.exists(backup_file):
                    Logger.success(f"Backup creado: {backup_file}", "SETTINGS_CONTROLLER")

                    # Limpiar backups antiguos según retención
                    try:
                        app_cfg = self.load_app_settings()
                        retention = int(app_cfg.get('backup', {}).get('retention_days', 30))
                        cutoff = datetime.now().timestamp() - (retention * 24 * 60 * 60)
                        for f in os.listdir(backups_dir):
                            fp = os.path.join(backups_dir, f)
                            if os.path.isfile(fp) and os.path.getmtime(fp) < cutoff:
                                try:
                                    os.remove(fp)
                                except Exception:
                                    pass
                    except Exception:
                        pass

                    return True, backup_file
                else:
                    stderr = proc.stderr.decode('utf-8', errors='replace') if proc and hasattr(proc, 'stderr') else ''
                    msg = f"Error al crear el backup. mysqldump rc={getattr(proc, 'returncode', 'N/A')} stderr={stderr}"
                    Logger.error(msg, "SETTINGS_CONTROLLER")
                    return False, msg

            except Exception as e:
                Logger.error(f"Excepción ejecutando mysqldump: {e}", "SETTINGS_CONTROLLER")
                return False, str(e)

        except Exception as e:
            Logger.error(f"Error creando backup: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def load_db_config(self):
        """Carga la configuración de la base de datos."""
        try:
            if os.path.exists(self.db_config_file):
                with open(self.db_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            Logger.error(f"Error cargando config de BD: {e}", "SETTINGS_CONTROLLER")
            return {}

    def test_database_connection(self):
        """Prueba la conexión a la base de datos."""
        try:
            if Database.test_connection():
                return True, "Conexión exitosa"
            return False, "No se pudo conectar"
        except Exception as e:
            Logger.error(f"Error probando conexión: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def get_security_settings(self):
        """Obtiene configuración de seguridad."""
        try:
            app_config = self.load_app_settings()
            return app_config.get('security', {
                'max_login_attempts': 3,
                'lockout_duration_minutes': 15
            })
        except Exception as e:
            Logger.error(f"Error obteniendo config de seguridad: {e}", "SETTINGS_CONTROLLER")
            return {}

    def update_security_settings(self, data):
        """Actualiza configuración de seguridad."""
        try:
            app_config = self.load_app_settings()
            
            if 'security' not in app_config:
                app_config['security'] = {}
            
            app_config['security']['max_login_attempts'] = int(data.get('max_login_attempts', 3))
            app_config['security']['lockout_duration_minutes'] = int(data.get('lockout_duration_minutes', 15))
            
            return self.save_app_settings(app_config)
        except Exception as e:
            Logger.error(f"Error actualizando seguridad: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def clear_old_logs(self, days=30):
        """Limpia logs antiguos."""
        try:
            Logger.clear_old_logs(days)
            return True, f"Logs de más de {days} días eliminados"
        except Exception as e:
            Logger.error(f"Error limpiando logs: {e}", "SETTINGS_CONTROLLER")
            return False, str(e)

    def get_storage_info(self):
        """Obtiene información de almacenamiento."""
        try:
            import shutil
            
            # Espacio en disco
            total, used, free = shutil.disk_usage("/")
            
            # Tamaño de la BD (aproximado por archivos)
            db_size = 0
            logs_size = 0
            backups_size = 0
            
            # Calcular tamaño de logs
            logs_dir = "logs"
            if os.path.exists(logs_dir):
                for f in os.listdir(logs_dir):
                    fp = os.path.join(logs_dir, f)
                    if os.path.isfile(fp):
                        logs_size += os.path.getsize(fp)
            
            # Calcular tamaño de backups
            backups_dir = "exports/backups"
            if os.path.exists(backups_dir):
                for f in os.listdir(backups_dir):
                    fp = os.path.join(backups_dir, f)
                    if os.path.isfile(fp):
                        backups_size += os.path.getsize(fp)
            
            return {
                'disk_total': total // (1024**3),  # GB
                'disk_used': used // (1024**3),
                'disk_free': free // (1024**3),
                'logs_size': logs_size // (1024**2),  # MB
                'backups_size': backups_size // (1024**2)
            }
        except Exception as e:
            Logger.error(f"Error obteniendo info de almacenamiento: {e}", "SETTINGS_CONTROLLER")
            return {}