"""
NoteBox - Punto de entrada principal
"""

import threading
import time
import tkinter as tk
from view.splash_view import NoteBoxSplash
from controller.settings_controller import SettingsController

from controller.inventory_controller import InventoryController
from utils.alerts import alert_manager
from utils.logger import Logger


def _backup_worker(poll_interval_seconds=60):
    """Worker que revisa configuración de backups y ejecuta backups automáticos."""
    sc = SettingsController(user_data=None)
    while True:
        try:
            backup_cfg = sc.get_backup_settings()
            auto = backup_cfg.get('auto_backup', False)
            freq_days = int(backup_cfg.get('backup_frequency_days', 7))

            if auto:
                last_ts = sc.get_last_backup_timestamp()
                now = time.time()

                # Si no hay backup previo o pasó más tiempo que la frecuencia, crear uno
                need = False
                if last_ts is None:
                    need = True
                else:
                    elapsed_days = (now - last_ts) / (60 * 60 * 24)
                    if elapsed_days >= freq_days:
                        need = True

                if need:
                    sc.create_backup()

            # Dormir antes de la siguiente comprobación
        except Exception:
            Logger.error("Error en backup worker", "MAIN")
        time.sleep(poll_interval_seconds)


def _alerts_worker(poll_interval_seconds=3600):
    """Worker que revisa productos inactivos y genera alertas."""
    ic = InventoryController()
    while True:
        try:
            # Verificar productos inactivos (por defecto 30 días)
            inactive_products = ic.get_inactive_products(days_without_movement=30)
            
            for product in inactive_products:
                alert_manager.generate_inactive_product_alert(product)
                
            # Dormir antes de la siguiente comprobación (por defecto 1 hora)
        except Exception as e:
            Logger.error(f"Error en alerts worker: {e}", "MAIN")
        time.sleep(poll_interval_seconds)


def _products_notification_worker(poll_interval_seconds=7200):
    """Worker que genera notificaciones automáticas para todos los productos."""
    ic = InventoryController()
    
    # Ejecutar inmediatamente al inicio
    try:
        Logger.info("Generando notificaciones automáticas para todos los productos...", "MAIN")
        
        # Obtener todos los productos de la base de datos
        all_products = ic.product_model.get_all_products_filtered()
        
        if all_products:
            Logger.info(f"Procesando {len(all_products)} productos para notificaciones", "MAIN")
            
            for product in all_products:
                # Generar alerta de stock si es necesario (también resuelve si el stock está bien)
                alert_manager.generate_stock_alert(product)
                
                # Generar alerta de producto inactivo si es necesario
                if product.get('dias_sin_movimiento', 0) >= 30:
                    alert_manager.generate_inactive_product_alert(product)
            
            Logger.success(f"Notificaciones procesadas para {len(all_products)} productos", "MAIN")
        else:
            Logger.info("No hay productos en la base de datos", "MAIN")
            
    except Exception as e:
        Logger.error(f"Error generando notificaciones iniciales: {e}", "MAIN")
    
    # Continuar ejecutando periódicamente
    while True:
        try:
            time.sleep(poll_interval_seconds)
            
            Logger.info("Actualizando notificaciones de productos...", "MAIN")
            
            all_products = ic.product_model.get_all_products_filtered()
            
            if all_products:
                for product in all_products:
                    alert_manager.generate_stock_alert(product)
                    
                    if product.get('dias_sin_movimiento', 0) >= 30:
                        alert_manager.generate_inactive_product_alert(product)
                
                Logger.success(f"Notificaciones actualizadas para {len(all_products)} productos", "MAIN")
                
        except Exception as e:
            Logger.error(f"Error en products notification worker: {e}", "MAIN")


def main():
    """Función principal que inicia la aplicación y los workers."""
    # Iniciar worker de backups en background
    t_backup = threading.Thread(target=_backup_worker, args=(60,), daemon=True)
    t_backup.start()

    # Iniciar worker de alertas en background
    t_alerts = threading.Thread(target=_alerts_worker, args=(3600,), daemon=True)
    t_alerts.start()

    # Iniciar worker de notificaciones de productos en background
    t_products = threading.Thread(target=_products_notification_worker, args=(7200,), daemon=True)
    t_products.start()

    app = NoteBoxSplash()
    app.run()


if __name__ == "__main__":
    main()