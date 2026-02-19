import tkinter as tk

from src.domain.element import Element
from src.domain.team import Team
from src.theme.theme_manager import ThemeManager


class PieceRenderer:
    """Draws elemental pieces on the game board based on their type and color."""

    def __init__(self, canvas: tk.Canvas, square_size: int, theme: ThemeManager):
        self.canvas = canvas
        self.square_size = square_size
        self.theme = theme

    def draw(self, row: int, col: int, element: Element, team: Team):
        """Draws a piece on the canvas based on its element type."""
        element_id = f"piece_{row}_{col}"
        self.canvas.delete(element_id)

        x = col * self.square_size + self.square_size // 2
        y = row * self.square_size + self.square_size // 2
        radius = self.square_size // 2 - 15

        self.canvas.create_oval(
            x - radius - 5, y - radius - 5,
            x + radius + 5, y + radius + 5,
            fill=self.theme.get_team_theme().get(team),
            stipple="gray50",
            outline="white",
            width=1,
            tags=element_id
        )

        if element == Element.FIRE:
            self._draw_fire(x, y, radius)
        elif element == Element.WATER:
            self._draw_water(x, y, radius)
        elif element == Element.EARTH:
            self._draw_earth(x, y, radius)
        elif element == Element.AIR:
            self._draw_air(x, y, radius)

    def _draw_fire(self, x: int, y: int, radius: int):
        """Draws a flame-shaped piece for the fire element."""
        points = [
            x, y - radius,
            x + radius * 0.6, y + radius * 0.4,
            x, y + radius * 0.8,
            x - radius * 0.6, y + radius * 0.4
        ]

        self.canvas.create_polygon(
            points,
            fill="white",
            outline=self.theme.get_piece_theme().FIRE
        )

    def _draw_water(self, x: int, y: int, radius: int):
        """Draws a wave-shaped piece for the water element."""
        self.canvas.create_arc(
            x - radius, y - radius,
            x + radius, y + radius,
            start=0,
            extent=180,
            outline=self.theme.get_piece_theme().WATER,
            width=2,
            style="arc"
        )

        self.canvas.create_line(x - radius, y, x + radius, y, fill="white")

    def _draw_earth(self, x: int, y: int, radius: int):
        """Draws a square-shaped piece for the earth element."""
        self.canvas.create_rectangle(
            x - radius * 0.6,
            y - radius * 0.6,
            x + radius * 0.6,
            y + radius * 0.6,
            fill="white",
            outline=self.theme.get_piece_theme().EARTH
        )

    def _draw_air(self, x: int, y: int, radius: int):
        """Draws a swirl-shaped piece for the air element."""
        self.canvas.create_oval(
            x - radius * 0.5,
            y - radius * 0.5,
            x + radius * 0.5,
            y + radius * 0.5,
            outline=self.theme.get_piece_theme().AIR,
            width=2
        )
