"""
NoteBox - Sistema de Gestión de Inventario
Definición de temas visuales
"""

from assets.styles.colors import Colors
from assets.styles.fonts import Fonts
from utils.logger import Logger

class ThemeManager:
    """Clase para gestionar los temas del sistema."""
    
    # Temas disponibles
    THEMES = {
        "light": {
            "name": "Tema Claro",
            "colors": {
                "primary": Colors.PRIMARY,
                "secondary": Colors.SECONDARY,
                "sidebar": Colors.SIDEBAR_BG,
                "background": Colors.BACKGROUND,
                "card_background": Colors.CARD_BG,
                "text_primary": Colors.TEXT_PRIMARY,
                "text_secondary": Colors.TEXT_SECONDARY,
                "border": Colors.BORDER,
                "hover": Colors.HOVER,
                "active": Colors.ACTIVE,
                "disabled": Colors.DISABLED,
                "accent": Colors.ACCENT,
                "success": Colors.SUCCESS,
                "warning": Colors.WARNING,
                "info": Colors.INFO,
                "stock_alto": Colors.STOCK_ALTO,
                "stock_medio": Colors.STOCK_MEDIO,
                "stock_bajo": Colors.STOCK_BAJO
            },
            "fonts": {
                "family": Fonts.FAMILY,
                "size_normal": Fonts.SIZE_NORMAL,
                "weight_normal": Fonts.WEIGHT_NORMAL,
                "weight_bold": Fonts.WEIGHT_BOLD
            }
        },
        "dark": {
            "name": "Tema Oscuro",
            "colors": {
                "primary": Colors.PRIMARY_DARK,
                "secondary": Colors.SECONDARY,
                "sidebar": Colors.PRIMARY_DARK,
                "background": "#1E1E1E",
                "card_background": "#2D2D2D",
                "text_primary": Colors.TEXT_LIGHT,
                "text_secondary": "#B0B0B0",
                "border": Colors.BORDER_DARK,
                "hover": "#2C3E50",
                "active": Colors.SECONDARY,
                "disabled": Colors.BORDER_LIGHT,
                "accent": Colors.ACCENT,
                "success": Colors.SUCCESS,
                "warning": Colors.WARNING,
                "info": Colors.INFO,
                "stock_alto": Colors.STOCK_ALTO,
                "stock_medio": Colors.STOCK_MEDIO,
                "stock_bajo": Colors.STOCK_BAJO
            },
            "fonts": {
                "family": Fonts.FAMILY,
                "size_normal": Fonts.SIZE_NORMAL,
                "weight_normal": Fonts.WEIGHT_NORMAL,
                "weight_bold": Fonts.WEIGHT_BOLD
            }
        }
    }
    
    # Tema actual
    current_theme = "light"
    
    @classmethod
    def get_current_theme(cls):
        """Obtiene el tema actual."""
        return cls.THEMES[cls.current_theme]
    
    @classmethod
    def set_theme(cls, theme_name):
        """Establece el tema actual."""
        if theme_name in cls.THEMES:
            cls.current_theme = theme_name
        else:
            Logger.warning(f"Tema '{theme_name}' no encontrado. Usando 'light' por defecto.", "THEME_MANAGER")
            cls.current_theme = "light"
    
    @classmethod
    def get_color(cls, color_key):
        """Obtiene un color específico del tema actual."""
        theme = cls.get_current_theme()
        return theme["colors"].get(color_key, Colors.PRIMARY)
    
    @classmethod
    def get_font(cls, size_key=None, weight="normal"):
        """Obtiene una configuración de fuente del tema actual."""
        theme = cls.get_current_theme()
        if size_key is None:
            size = theme["fonts"]["size_normal"]
        else:
            size = theme["fonts"][size_key] if size_key in theme["fonts"] else theme["fonts"]["size_normal"]
        return (theme["fonts"]["family"], size, weight)