"""Manages the game board state and rendering of pieces based on their elemental types."""
import tkinter as tk

from src.domain.board import Board
from src.game.piece_renderer import PieceRenderer
from src.theme.board_theme import BoardColor
from src.theme.theme_manager import ThemeManager

class BoardRenderer:
    """Manages the game board state and rendering of pieces based on their elemental types."""
    def __init__(self, canvas: tk.Canvas, square_size: int, theme: ThemeManager):
        self._canvas = canvas
        self._square_size = square_size
        self.theme = theme
        self.piece_renderer = PieceRenderer(canvas, square_size, theme)

    def draw(self, board: Board):
        """Draws the game board and pieces based on the current state."""
        self._canvas.delete("all")

        board_theme = self.theme.get_board_theme()

        for r in range(board.size):
            for c in range(board.size):

                square_color = (
                    board_theme.get(BoardColor.LIGHT) if
                    (r + c) % 2 == 0
                    else board_theme.get(BoardColor.DARK)
                )

                self._canvas.create_rectangle(
                    c * self._square_size,
                    r * self._square_size,
                    (c + 1) * self._square_size,
                    (r + 1) * self._square_size,
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

    def move_piece(self, board: Board, move):
        """Animates a piece moving from its starting position to its destination."""
        piece = board.get_piece(move.start_row, move.start_col)
        if piece.is_empty:
            return

        # Animate the piece moving to the new location
        self.piece_renderer.move_piece(
            piece,
            move.start_row,
            move.start_col,
            move.end_row,
            move.end_col
        )

        # Remove captured pieces from the board and canvas
        for r, c in move.captured:
            board.set_piece(r, c, None)
            self._canvas.delete(f"piece_{r}_{c}")

        # Update the board state with the moved piece
        board.set_piece(move.end_row, move.end_col, piece)
        board.set_piece(move.start_row, move.start_col, None)

    def square_size(self) -> int:
        """Returns the size of each square on the board."""
        return self._square_size