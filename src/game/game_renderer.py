import tkinter as tk

from src.domain.team import Team
from src.game.board_renderer import BoardRenderer
from src.domain.game import Game
from src.theme.theme_manager import ThemeManager

class GameRenderer:
    """Manages the main game window, rendering the board and handling user interactions."""

    def __init__(self, root: tk.Tk, game: Game, square_size: int = 80):
        self._root = root
        self._game = game
        self._square_size = square_size
        self._theme = ThemeManager()

        self._canvas = tk.Canvas(
            root,
            width=game.board.get_size() * square_size,
            height=game.board.get_size() * square_size
        )
        self._canvas.pack()

        self.board_renderer = BoardRenderer(self._canvas, square_size, self._theme)
        self._canvas.bind("<Button-1>", self.on_click)

    def initialize(self):
        """Initializes the game state and redraws the board."""
        self._game.initialize()
        self._setup_window()
        self._redraw_all()

    def _setup_window(self):
        """Configures the main window size and title."""
        size = self._game.board.size * self._square_size + 180
        self._root.geometry(f"{size}x{size}")
        self._root.title("AZULON")

    def on_click(self, event):
        """Handles user clicks to select and move pieces."""
        col = event.x // self._square_size
        row = event.y // self._square_size

        if not self._game.board.in_bounds(row, col):
            return

        # Clear selection if clicking the same piece again
        if self._game.is_same_selected_piece(row, col):
            self._game.clear_selection()
            self.board_renderer.set_valid_moves([])
            self.board_renderer.selected_piece(None, None)

            self._redraw_all()
            return

        if self._game.selected_piece() is None:
            selected = self._game.select_piece(row, col)
            if selected:
                self.board_renderer.selected_piece(row, col)
                moves = self._game.get_valid_moves(row, col)
                self.board_renderer.set_valid_moves([(m.end_row, m.end_col) for m in moves])
        else:
            move = self._game.move_selected_piece(row, col)
            if move:
                self.board_renderer.move_piece(self._game.board, move)

                # Reset selection and valid moves after an attempt to move
                self.board_renderer.set_valid_moves([])
                self.board_renderer.selected_piece(None, None)

        self._redraw_all()

    def draw_scores(self):
        """Draws the current scores for both teams on the canvas."""
        self._canvas.delete("score")

        scores = self._game.scores()
        red_score = scores.get(Team.RED, 0)
        blue_score = scores.get(Team.BLUE, 0)

        board_px = self._square_size * self._game.board.get_size()
        padding = 0

        self._canvas.create_text(
            padding,
            padding,
            anchor="nw",
            text=f"BLUE: {blue_score}",
            fill=self._theme.get_team_theme().get(Team.BLUE),
            font=("Arial", 16, "bold"),
            tags="score"
        )

        self._canvas.create_text(
            board_px - padding,
            board_px - padding,
            anchor="se",
            text=f"RED: {red_score}",
            fill=self._theme.get_team_theme().get(Team.RED),
            font=("Arial", 16, "bold"),
            tags="score"
        )

    def _show_game_over(self, winner: Team):
        """Displays a game over message indicating the winning team."""
        self._canvas.create_rectangle(
            0, 0,
            self._square_size * self._game.board.size,
            self._square_size * self._game.board.size,
            fill="black",
            stipple="gray50",
            tags="gameover"
        )

        self._canvas.create_text(
            self._square_size * self._game.board.size // 2,
            self._square_size * self._game.board.size // 2,
            text=f"{winner.name} WINS",
            fill="white",
            font=("Arial", 32, "bold"),
            tags="gameover"
        )

    def _redraw_all(self):
        """Helper to refresh the UI."""
        self.board_renderer.draw_board(self._game.board)
        self.board_renderer.draw_all_pieces(self._game.board)
        self.draw_scores()

        winner = self._game.get_winner()
        if winner:
            self._show_game_over(winner)