"""
Módulo de Constantes
Contiene todas las constantes, colores y configuraciones del simulador
"""

# --- CONSTANTES DE MEMORIA ---
MEMORIA_DEFAULT = 1024
BLOQUE_MEMORIA = 1

# --- COLORES FUTURISTAS Y TECNOLÓGICOS - TEMA OSCURO ---
COLOR_FONDO_PRINCIPAL = "#0a0e27"  # Azul oscuro profundo
COLOR_FONDO_SECUNDARIO = "#141b2d"  # Azul oscuro medio
COLOR_FONDO_CANVAS = "#1a1f3a"  # Azul oscuro para canvas
COLOR_LIBRE = "#1e2749"  # Azul muy oscuro para memoria libre
COLOR_OCUPADO = "#4a5568"  # Gris azulado para procesos normales
COLOR_EJECUCION = "#ffd700"  # Dorado brillante para proceso en ejecución
COLOR_EJECUCION_BRILLO = "#ffed4e"  # Dorado más claro para brillo
COLOR_PRIMARIO = "#00d4ff"  # Cyan brillante
COLOR_SECUNDARIO = "#ff6b35"  # Naranja vibrante
COLOR_DORADO = "#ffd700"  # Dorado
COLOR_FONDO_OSCURO = "#0d1117"  # Casi negro
COLOR_TEXTO_CLARO = "#e4e6eb"  # Blanco suave
COLOR_TEXTO_DORADO = "#ffd700"  # Texto dorado
COLOR_BORDE = "#2d3748"  # Borde gris oscuro
COLOR_BORDE_DORADO = "#ffd700"  # Borde dorado
COLOR_FONDO_MODERNO = "#141b2d"  # Fondo oscuro para ventanas
COLOR_HOVER = "#2a3441"  # Color hover


def get_color_proceso(pid):
    """
    Retorna un color único para cada proceso basado en su PID
    Paleta de colores futuristas y tecnológicos
    """
    colores = [
        "#00d4ff",  # Cyan brillante
        "#ff6b35",  # Naranja vibrante
        "#9d4edd",  # Púrpura neón
        "#06ffa5",  # Verde neón
        "#ff006e",  # Rosa neón
        "#8338ec",  # Púrpura eléctrico
        "#3a86ff",  # Azul eléctrico
        "#ffbe0b",  # Amarillo dorado
        "#fb5607",  # Naranja intenso
        "#ff006e",  # Magenta
        "#06ffa5",  # Verde esmeralda
        "#8338ec",  # Violeta
        "#3a86ff",  # Azul cielo
        "#ffbe0b",  # Oro
        "#fb5607"   # Coral
    ]
    return colores[(pid - 1) % len(colores)]

