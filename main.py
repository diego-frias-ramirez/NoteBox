"""
NoteBox - Punto de entrada principal
"""

import tkinter as tk
from view.splash_view import NoteBoxSplash

def main():
    """Función principal que inicia la aplicación."""
    app = NoteBoxSplash()
    app.run()

if __name__ == "__main__":
    main()