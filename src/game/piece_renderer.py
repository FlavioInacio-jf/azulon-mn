import tkinter as tk

from src.domain.element import Element
from src.domain.team import Team
from src.game.svg_loader import SvgLoader
from src.theme.theme_manager import ThemeManager


class PieceRenderer:
    """Draws elemental pieces on the game board based on their type and color."""

    def __init__(self, canvas: tk.Canvas, square_size: int, theme: ThemeManager):
        self.assets_path = "assets/svg"
        self.canvas = canvas
        self.square_size = square_size
        self.theme = theme

        self.svg = SvgLoader()
        # Keep references to images so Tkinter does not garbage collect
        self._images: dict[str, tk.PhotoImage] = {}

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
            outline=self.theme.get_team_theme().get(team),
            width=1,
            tags=element_id
        )

        size = int(self.square_size * 0.8)

        path = self._get_svg_path(element)
        img = self.svg.load(path, size)
        self.canvas.create_image(x, y, image=img)

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

    def _get_svg_path(self, element)-> str:
        """Returns the file path for the SVG corresponding to the given element."""
        mapping = {
            Element.FIRE: "fire.svg",
            Element.WATER: "water.svg",
            Element.EARTH: "earth.svg",
            Element.AIR: "air.svg",
        }

        return f"{self.assets_path}/{mapping.get(element, 'default.svg')}"

    def move_piece(self, piece, start_row: int, start_col: int, end_row: int, end_col: int, steps: int = 10, delay: float = 0.02):
        """Animates a piece moving from its starting position to its destination."""
        element = piece.element
        team = piece.team

        start_x = start_col * self.square_size + self.square_size // 2
        start_y = start_row * self.square_size + self.square_size // 2
        end_x = end_col * self.square_size + self.square_size // 2
        end_y = end_row * self.square_size + self.square_size // 2

        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps

        element_id = f"piece_move"
        radius = self.square_size // 2 - 15
        self.canvas.delete(element_id)
        oval = self.canvas.create_oval(
            start_x - radius, start_y - radius,
            start_x + radius, start_y + radius,
            fill=self.theme.get_team_theme().get(team),
            outline=self.theme.get_team_theme().get(team),
            width=1,
            tags=element_id
        )

        # Carrega SVG
        size = int(self.square_size * 0.8)
        path = self._get_svg_path(element)
        img = self.svg.load(path, size)
        img_id = self.canvas.create_image(start_x, start_y, image=img, tags=element_id)
        self._images[element_id] = img

        # Animação
        for _ in range(steps):
            self.canvas.move(element_id, dx, dy)
            self.canvas.update()
            self.canvas.after(int(delay*1000))  # usa after no lugar de time.sleep

        # Remove antigo e redesenha na posição final
        self.canvas.delete(element_id)
        self.draw(end_row, end_col, element, team)