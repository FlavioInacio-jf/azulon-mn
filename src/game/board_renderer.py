"""Manages the game board state and rendering of pieces based on their elemental types."""
import tkinter as tk

from src.domain.board import Board
from src.game.piece_renderer import PieceRenderer

class BoardRenderer:
    """Manages the game board state and rendering of pieces based on their elemental types."""
    COLORS = {
        "light": "#e6d3a3",   # parchment
        "dark": "#8b6f47",    # stone
        "highlight": "#f4e4a1"  # gold aura
    }

    def __init__(self, canvas: tk.Canvas, square_size: int):
        self.canvas = canvas
        self.square_size = square_size
        self.piece_renderer = PieceRenderer(canvas, square_size)

    def draw(self, board: Board):
        """Draws the game board and pieces based on the current state of the board."""
        self.canvas.delete("all")

        for r in range(board.size):
            for c in range(board.size):
                color = (
                    self.COLORS["light"]
                    if (r + c) % 2 == 0
                    else self.COLORS["dark"]
                )

                self.canvas.create_rectangle(
                    c * self.square_size,
                    r * self.square_size,
                    (c + 1) * self.square_size,
                    (r + 1) * self.square_size,
                    fill=color
                )

                piece = board.grid[r][c]
                if piece:
                    self.piece_renderer.draw(r, c, piece.element)
