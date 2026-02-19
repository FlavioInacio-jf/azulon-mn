"""Manages the game board state and rendering of pieces based on their elemental types."""
import tkinter as tk

from src.domain.element import Element
from src.game.piece import Piece

class Board:
    """Manages the game board state and rendering of pieces based on their elemental types."""
    COLORS = {
        "light": "#e6d3a3",   # parchment
        "dark": "#8b6f47",    # stone
        "highlight": "#f4e4a1"  # gold aura
    }

    def __init__(self, canvas: tk.Canvas, square_size: int, board_size: int):
        # Main game class responsible for managing the game state and GUI
        self.canvas = canvas
        self.square_size = square_size
        self.board_size = board_size

        self.board: list[list[Element]] = [[Element.EMPTY] * board_size for _ in range(board_size)]
        self.selected: tuple[int, int] | None = None
        self.turn: Element = Element.FIRE

        self.piece = Piece(canvas, square_size)

        self.canvas.bind("<Button-1>", self.on_click)

    def draw(self):
        """Draws the game board and pieces on the canvas."""
        self.canvas.delete("all")

        for r in range(self.board_size):
            for c in range(self.board_size):
                color = "bisque" if (r + c) % 2 == 0 else "gray"

                self.canvas.create_rectangle(
                    c * self.square_size,
                    r * self.square_size,
                    (c + 1) * self.square_size,
                    (r + 1) * self.square_size,
                    fill=color
                )

                # draw piece via renderer
                self.piece.draw(r, c, self.board[r][c])

    def initialize(self):
        """Initializes the game board with starting pieces."""
        for r in range(self.board_size):
            for c in range(self.board_size):
                if (r + c) % 2 != 0:
                    if r < 2:
                        self.board[r][c] = Element.WATER
                    elif r > 3:
                        self.board[r][c] = Element.FIRE

        self.draw()

    def on_click(self, event):
        """Handles click events on the canvas to select and move pieces."""
        col = event.x // self.square_size
        row = event.y // self.square_size

        if row >= self.board_size or col >= self.board_size:
            return

        if self.selected:
            r_old, c_old = self.selected

            if self.board[row][col] == Element.EMPTY:
                self.board[row][col] = self.board[r_old][c_old]
                self.board[r_old][c_old] = Element.EMPTY

            self.selected = None
            self.draw()
        else:
            if self.board[row][col] != Element.EMPTY:
                self.selected = (row, col)
