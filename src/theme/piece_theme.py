from enum import Enum

class PIECE_THEME(str, Enum):
    """Enumeration of piece theme colors."""
    LIGHT_BG = "#2c2c2c"
    DARK_BG = "#121212"
    FIRE = "#e74c3c"
    WATER = "#00bfff"
    EARTH = "#2ecc71"
    AIR = "#f1c40f"
    HIGHLIGHT = "#ffffff"