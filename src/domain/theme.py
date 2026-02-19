from enum import Enum

class Color(Enum):
    """Enumeration of theme colors."""
    LIGHT_BG = "light_bg"
    DARK_BG = "dark_bg"
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    HIGHLIGHT = "highlight"


COLORS = {
    Color.LIGHT_BG: "#2c2c2c",
    Color.DARK_BG: "#121212",
    Color.FIRE: "#e74c3c",
    Color.WATER: "#00bfff",
    Color.EARTH: "#2ecc71",
    Color.AIR: "#f1c40f",
    Color.HIGHLIGHT: "#ffffff",
}
