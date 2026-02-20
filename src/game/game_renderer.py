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
        self.board_renderer.draw_board(self.game.board)
        self.board_renderer.draw_all_pieces(self.game.board)

    def _setup_window(self):
        """Configures the main window size and title."""
        size = self.game.board.size * self.square_size + 180
        self.root.geometry(f"{size}x{size}")
        self.root.title("AZULON")

    def on_click(self, event):
        """Handles user clicks to select and move pieces."""
        col = event.x // self.square_size
        row = event.y // self.square_size

        print(f"Clicked on row {row}, col {col}")

        if not self.game.board.in_bounds(row, col):
            return

        if self.game.selected_row is None:
            selected = self.game.select_piece(row, col)
            if selected:
                self.board_renderer.selected_piece(row, col)
                moves = self.game.get_valid_moves(row, col)
                self.board_renderer.set_valid_moves([(m.end_row, m.end_col) for m in moves])
        else:
            move = self.game.move_selected_piece(row, col)
            if move:
                self.board_renderer.move_piece(self.game.board, move)

                # Reset selection and valid moves after an attempt to move
                self.board_renderer.set_valid_moves([])
                self.board_renderer.selected_piece(None, None)

        self.board_renderer.draw_board(self.game.board)
        self.board_renderer.draw_all_pieces(self.game.board)

