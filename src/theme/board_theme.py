from enum import Enum

class BoardColor(Enum):
    """Enumeration of board theme colors."""
    LIGHT = "light"
    DARK = "dark"
    HIGHLIGHT = "highlight"

class BoardTheme:
    """Defines the color scheme for the game board."""

    palette = {
        BoardColor.LIGHT: "#e6d3a3",
        BoardColor.DARK: "#8b6f47",
        BoardColor.HIGHLIGHT: "#d4c68f",
    }

    def get(self, color: BoardColor) -> str:
        """Returns the hex color code for a given BoardColor."""
        return self.palette[color]