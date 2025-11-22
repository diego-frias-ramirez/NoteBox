# controller/notifications_controller.py

import mysql.connector
from datetime import datetime, timedelta

class NotificationsController:
    def __init__(self, db_config):
        self.db_config = db_config
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        return mysql.connector.connect(**self.db_config)
    
    def get_notifications_summary(self):
        """Obtener resumen de notificaciones"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Contar notificaciones por tipo
            query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN leida = 0 THEN 1 ELSE 0 END) as no_leidas,
                SUM(CASE WHEN tipo = 'Stock bajo' AND leida = 0 THEN 1 ELSE 0 END) as advertencias,
                SUM(CASE WHEN tipo = 'Producto agotado' AND leida = 0 THEN 1 ELSE 0 END) as criticas
            FROM alertas
            WHERE fecha_alerta >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            """
            cursor.execute(query)
            summary = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return {
                'total': summary['total'] or 0,
                'no_leidas': summary['no_leidas'] or 0,
                'advertencias': summary['advertencias'] or 0,
                'criticas': summary['criticas'] or 0
            }
            
        except Exception as e:
            print(f"Error obteniendo resumen de notificaciones: {e}")
            return {'total': 0, 'no_leidas': 0, 'advertencias': 0, 'criticas': 0}
    
    def get_all_notifications(self, filter_type="all"):
        """Obtener todas las notificaciones con filtro"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            base_query = """
            SELECT 
                a.id,
                a.tipo,
                a.descripcion,
                a.fecha_alerta,
                a.leida,
                p.nombre as producto_nombre,
                p.codigo as producto_codigo,
                u.nombre as usuario_nombre
            FROM alertas a
            LEFT JOIN productos p ON a.producto_id = p.id
            LEFT JOIN usuarios u ON a.usuario_id = u.id
            WHERE a.fecha_alerta >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            """
            
            # Aplicar filtros
            if filter_type == "no_leidas":
                query = base_query + " AND a.leida = 0"
            elif filter_type == "advertencias":
                query = base_query + " AND a.tipo = 'Stock bajo' AND a.leida = 0"
            elif filter_type == "criticas":
                query = base_query + " AND a.tipo = 'Producto agotado' AND a.leida = 0"
            else:
                query = base_query
                
            query += " ORDER BY a.fecha_alerta DESC"
            
            cursor.execute(query)
            notifications = cursor.fetchall()
            
            # Formatear notificaciones para la vista
            formatted_notifications = []
            for notif in notifications:
                formatted_notif = self._format_notification(notif)
                formatted_notifications.append(formatted_notif)
            
            cursor.close()
            conn.close()
            
            return formatted_notifications
            
        except Exception as e:
            print(f"Error obteniendo notificaciones: {e}")
            return []
    
    def _format_notification(self, notification):
        """Formatear notificación para la vista"""
        tipo = notification['tipo']
        leida = notification['leida']
        
        # Mapear tipos a formato de vista
        type_mapping = {
            'Stock bajo': ('warning', '⚠️', 'Stock bajo detectado'),
            'Producto agotado': ('critical', '📦', 'Producto agotado'),
            'Sin movimiento': ('info', '📉', 'Producto sin movimiento'),
            'Backup': ('success', '✓', 'Backup completado'),
            'Actualizacion': ('info', 'ℹ️', 'Actualización disponible'),
            'Recordatorio': ('warning', '⏰', 'Recordatorio')
        }
        
        notif_type, icon, title = type_mapping.get(tipo, ('info', 'ℹ️', 'Notificación'))
        
        # Formatear descripción
        descripcion = notification['descripcion']
        if notification['producto_nombre']:
            descripcion = f"El producto '{notification['producto_nombre']}' {descripcion}"
        
        # Formatear tiempo relativo
        fecha_alerta = notification['fecha_alerta']
        time_diff = self._get_relative_time(fecha_alerta)
        
        # Colores según tipo
        color_mapping = {
            'warning': ('#fff4e6', '#ffc107'),
            'critical': ('#ffe5e5', '#ef233c'),
            'info': ('#e8f4f8', '#00b4d8'),
            'success': ('#d4edda', '#10b981')
        }
        
        bg_color, border_color = color_mapping.get(notif_type, ('#e8f4f8', '#00b4d8'))
        
        return (
            notif_type, icon, title, descripcion, time_diff, 
            bg_color, border_color, notification['id'], leida
        )
    
    def _get_relative_time(self, fecha):
        """Obtener tiempo relativo en formato legible"""
        now = datetime.now()
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        
        diff = now - fecha
        
        if diff.days > 0:
            if diff.days == 1:
                return "Hace 1 día"
            else:
                return f"Hace {diff.days} días"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"Hace {hours} hora{'s' if hours > 1 else ''}"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"Hace {minutes} minuto{'s' if minutes > 1 else ''}"
        else:
            return "Hace unos momentos"
    
    def mark_as_read(self, notification_id):
        """Marcar notificación como leída"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "UPDATE alertas SET leida = 1 WHERE id = %s"
            cursor.execute(query, (notification_id,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error marcando notificación como leída: {e}")
            return False
    
    def mark_all_as_read(self):
        """Marcar todas las notificaciones como leídas"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "UPDATE alertas SET leida = 1 WHERE leida = 0"
            cursor.execute(query)
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error marcando todas como leídas: {e}")
            return False
    
    def delete_notification(self, notification_id):
        """Eliminar notificación"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM alertas WHERE id = %s"
            cursor.execute(query, (notification_id,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error eliminando notificación: {e}")
            return False
    
    def clear_all_notifications(self):
        """Eliminar todas las notificaciones"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM alertas WHERE fecha_alerta < DATE_SUB(NOW(), INTERVAL 7 DAY)"
            cursor.execute(query)
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error limpiando notificaciones: {e}")
            return False
    
    def get_notification_settings(self):
        """Obtener configuración de notificaciones"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM configuracion LIMIT 1"
            cursor.execute(query)
            config = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            # Por ahora retornamos valores por defecto
            # En una implementación real, esto vendría de la tabla de configuración
            return {
                'stock_alerts': True,
                'no_movement': True,
                'backup_confirm': True
            }
            
        except Exception as e:
            print(f"Error obteniendo configuración: {e}")
            return {
                'stock_alerts': True,
                'no_movement': True,
                'backup_confirm': True
            }
    
    def update_notification_settings(self, settings):
        """Actualizar configuración de notificaciones"""
        try:
            # En una implementación real, esto actualizaría la tabla de configuración
            print(f"Configuración actualizada: {settings}")
            return True
        except Exception as e:
            print(f"Error actualizando configuración: {e}")
            return False
    
    def generate_sample_notifications(self):
        """Generar notificaciones de ejemplo para testing"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener algunos productos para las notificaciones
            cursor.execute("SELECT id, nombre FROM productos LIMIT 5")
            productos = cursor.fetchall()
            
            # Limpiar notificaciones existentes
            cursor.execute("DELETE FROM alertas")
            
            # Insertar notificaciones de ejemplo
            sample_notifications = [
                ('Stock bajo', productos[0][0] if productos else None, 
                 f'tiene solo {8} unidades disponibles.', 0, 1),
                ('Producto agotado', productos[1][0] if len(productos) > 1 else None,
                 'se ha agotado completamente.', 0, 1),
                ('Sin movimiento', productos[2][0] if len(productos) > 2 else None,
                 'lleva 45 días sin rotación.', 0, 1),
                ('Backup', None, 'El respaldo automático se realizó exitosamente.', 1, 1),
                ('Stock bajo', productos[3][0] if len(productos) > 3 else None,
                 f'tiene solo {12} unidades disponibles.', 0, 1),
                ('Actualizacion', None, 'Hay una nueva versión del sistema disponible (v1.0.1).', 0, 1),
                ('Recordatorio', None, 'Es recomendable realizar un inventario físico mensual.', 0, 1)
            ]
            
            # Insertar con fechas escalonadas
            for i, (tipo, producto_id, descripcion, leida, usuario_id) in enumerate(sample_notifications):
                fecha = f"DATE_SUB(NOW(), INTERVAL {i * 2} HOUR)"
                query = f"""
                INSERT INTO alertas (tipo, producto_id, descripcion, fecha_alerta, leida, usuario_id)
                VALUES (%s, %s, %s, {fecha}, %s, %s)
                """
                cursor.execute(query, (tipo, producto_id, descripcion, leida, usuario_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("Notificaciones de ejemplo generadas exitosamente")
            return True
            
        except Exception as e:
            print(f"Error generando notificaciones de ejemplo: {e}")
            return False