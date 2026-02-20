"""Manages the game board state and rendering of pieces based on their elemental types."""
import tkinter as tk

from src.domain.board import Board
from src.game.piece_renderer import PieceRenderer
from src.theme.board_theme import BoardColor
from src.theme.theme_manager import ThemeManager

class BoardRenderer:
    """Manages the game board state and rendering of pieces based on their elemental types."""
    def __init__(self, canvas: tk.Canvas, square_size: int, theme: ThemeManager):
        self.canvas = canvas
        self.square_size = square_size
        self.theme = theme
        self.piece_renderer = PieceRenderer(canvas, square_size, theme)

    def draw(self, board: Board):
        """Draws the game board and pieces based on the current state."""
        self.canvas.delete("all")

        board_theme = self.theme.get_board_theme()

        for r in range(board.size):
            for c in range(board.size):

                square_color = (
                    board_theme.get(BoardColor.LIGHT) if
                    (r + c) % 2 == 0
                    else board_theme.get(BoardColor.DARK)
                )

                self.canvas.create_rectangle(
                    c * self.square_size,
                    r * self.square_size,
                    (c + 1) * self.square_size,
                    (r + 1) * self.square_size,
                    fill=square_color,
                    outline=""
                )


                piece = board.grid[r][c]
                if piece:
                    self.piece_renderer.draw(
                        r,
                        c,
                        piece.element,
                        piece.team
                    )
