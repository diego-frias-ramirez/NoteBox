"""
NoteBox - Sistema de Gestión de Inventario
Configuración de fuentes y tamaños
"""

class Fonts:
    """Clase con configuraciones de fuentes para la interfaz del sistema."""
    
    # Familia de fuentes
    FAMILY = "Segoe UI"
    FAMILY_FALLBACK = "Arial"
    FAMILY_MONO = "Consolas"
    
    # Tamaños de fuente
    SIZE_SMALL = 9
    SIZE_NORMAL = 10
    SIZE_MEDIUM = 11
    SIZE_LARGE = 12
    SIZE_XLARGE = 14
    SIZE_TITLE = 16
    SIZE_HEADING = 18
    SIZE_DISPLAY = 24
    
    # Pesos de fuente
    WEIGHT_NORMAL = "normal"
    WEIGHT_BOLD = "bold"
    
    # Configuraciones predefinidas
    @staticmethod
    def get_font(size=10, weight="normal"):
        """Retorna una tupla de configuración de fuente"""
        return (Fonts.FAMILY, size, weight)
    
    # Fuentes específicas para componentes
    SIDEBAR_TITLE = (FAMILY, SIZE_DISPLAY, WEIGHT_BOLD)
    SIDEBAR_ITEM = (FAMILY, SIZE_MEDIUM, WEIGHT_NORMAL)
    
    BUTTON_NORMAL = (FAMILY, SIZE_NORMAL, WEIGHT_NORMAL)
    BUTTON_LARGE = (FAMILY, SIZE_MEDIUM, WEIGHT_BOLD)
    
    LABEL_NORMAL = (FAMILY, SIZE_NORMAL, WEIGHT_NORMAL)
    LABEL_BOLD = (FAMILY, SIZE_NORMAL, WEIGHT_BOLD)
    LABEL_TITLE = (FAMILY, SIZE_LARGE, WEIGHT_BOLD)
    
    ENTRY_NORMAL = (FAMILY, SIZE_NORMAL, WEIGHT_NORMAL)
    
    TABLE_HEADER = (FAMILY, SIZE_NORMAL, WEIGHT_BOLD)
    TABLE_CELL = (FAMILY, SIZE_NORMAL, WEIGHT_NORMAL)
    
    TITLE_LARGE = (FAMILY, SIZE_HEADING, WEIGHT_BOLD)
    SUBTITLE = (FAMILY, SIZE_LARGE, WEIGHT_NORMAL)