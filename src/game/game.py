"""Main game class responsible for managing the game state and GUI."""

import tkinter as tk

from src.game.board import Board

class Game:
    """Main game class responsible for managing the game state and GUI."""
    def __init__(self, root: tk.Tk):
        # Main game class responsible for managing the game state and GUI
        self.square_size = 80
        self.board_size = 6

        self.root = root
        self.canvas = self._get_canvas()
        self.board = Board(self.canvas, self.square_size, self.board_size)

        # Initialize the game board with starting pieces and draw it
        self.board.draw()
        self.board.initialize()
        self._setup_window()

    def _setup_window(self):
        """Configures the main application window."""
        geometry_width = self.board_size * self.square_size + 180
        geometry_height = self.board_size * self.square_size + 180

        self.root.geometry(f"{geometry_width}x{geometry_height}")
        self.root.title("AZULON")

    def _get_canvas(self)-> tk.Canvas:
        """Initializes the game board canvas."""
        canvas = tk.Canvas(
            self.root,
            width=self.board_size * self.square_size,
            height=self.board_size * self.square_size
        )
        canvas.pack()
        return canvas
