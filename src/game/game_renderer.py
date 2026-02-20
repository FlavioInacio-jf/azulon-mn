import tkinter as tk

from src.game.board_renderer import BoardRenderer
from src.domain.game import Game
from src.theme.theme_manager import ThemeManager

class GameRenderer:
    """Manages the main game window, rendering the board and handling user interactions."""

    def __init__(self, root: tk.Tk, game: Game, square_size: int = 80):
        self.root = root
        self.game = game
        self.square_size = square_size
        self.theme = ThemeManager()

        self.canvas = tk.Canvas(
            root,
            width=game.board.get_size() * square_size,
            height=game.board.get_size() * square_size
        )
        self.canvas.pack()

        self.board_renderer = BoardRenderer(self.canvas, square_size, self.theme)
        self.canvas.bind("<Button-1>", self.on_click)

    def initialize(self):
        """Initializes the game state and redraws the board."""
        self.game.initialize()
        self._setup_window()
        self._draw()

    def _setup_window(self):
        """Configures the main window size and title."""
        size = self.game.board.size * self.square_size + 180
        self.root.geometry(f"{size}x{size}")
        self.root.title("AZULON")

    def _draw(self):
        """Draws the current game state on the canvas."""
        self.board_renderer.draw(self.game.board)

    def on_click(self, event):
        """Handles click events on the canvas, translating them to game logic."""
        col = event.x // self.square_size
        row = event.y // self.square_size

        self.game.click(row, col)
        self._draw()
