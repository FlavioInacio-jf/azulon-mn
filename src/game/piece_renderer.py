import tkinter as tk

from src.domain.piece import Piece
from src.game.svg_loader import SvgLoader
from src.theme.theme_manager import ThemeManager


class PieceRenderer:
    """Draws elemental pieces on the game board based on their type and color."""

    def __init__(self, canvas: tk.Canvas, square_size: int, theme: ThemeManager):
        self.canvas = canvas
        self.square_size = square_size
        self.theme = theme
        self.svg_loader = SvgLoader()
        self._images: dict[str, tk.PhotoImage] = {}

    def draw_piece(self, row: int, col: int, piece: Piece):
        """Draws a piece on the canvas based on its element type."""
        element_id = self._get_element_id(row, col)
        self.canvas.delete(element_id)

        x = col * self.square_size + self.square_size // 2
        y = row * self.square_size + self.square_size // 2
        radius = self.square_size // 2 - 15

        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=self.theme.get_team_theme().get(piece.team),
            outline=self.theme.get_team_theme().get(piece.team),
            tags=element_id
        )

        size = int(self.square_size * 0.8)
        path = f"assets/svg/{piece.element.name.lower()}.svg"
        img = self.svg_loader.load(path, size)
        self.canvas.create_image(x, y, image=img, tags=element_id)
        self._images[element_id] = img

    def animate_move(self, piece, start_row, start_col, end_row, end_col, steps=10, delay=20):
        """Anima a peça do ponto inicial ao final."""
        element_id = f"piece_{start_row}_{start_col}"
        start_x = start_col * self.square_size + self.square_size // 2
        start_y = start_row * self.square_size + self.square_size // 2
        end_x = end_col * self.square_size + self.square_size // 2
        end_y = end_row * self.square_size + self.square_size // 2

        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps

        for _ in range(steps):
            self.canvas.move(element_id, dx, dy)
            self.canvas.update()
            self.canvas.after(delay)

        # Garantir posição final exata
        self.draw_piece(end_row, end_col, piece)
        self.canvas.delete(element_id)

    def _get_element_id(self, row: int, col: int) -> str:
        """Generates a unique canvas tag for a piece based on its board position."""
        return f"piece_{row}_{col}"
