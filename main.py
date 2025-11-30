"""
NoteBox - Punto de entrada principal
"""

import threading
import time
import tkinter as tk
from view.splash_view import NoteBoxSplash
from controller.settings_controller import SettingsController
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


def main():
    """Función principal que inicia la aplicación y el worker de backups."""
    # Iniciar worker de backups en background
    t = threading.Thread(target=_backup_worker, args=(60,), daemon=True)
    t.start()

    app = NoteBoxSplash()
    app.run()


if __name__ == "__main__":
    main()