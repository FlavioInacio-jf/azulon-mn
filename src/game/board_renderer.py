"""Manages the game board state and rendering of pieces based on their elemental types."""
import tkinter as tk

from src.domain.board import Board
from src.domain.move import Move
from src.domain.piece import Piece
from src.domain.team import Team
from src.game.piece_renderer import PieceRenderer
from src.theme.board_theme import BoardColor
from src.theme.theme_manager import ThemeManager

class BoardRenderer:
    """Manages the game board state and rendering of pieces based on their elemental types."""
    def __init__(self, canvas: tk.Canvas, square_size: int, theme: ThemeManager):
        self._canvas = canvas
        self._square_size = square_size
        self._theme = theme
        self._piece_renderer = PieceRenderer(canvas, square_size, theme)

    def draw_board(self, board: Board):
        """Draws the game board and pieces based on the current state."""
        self._canvas.delete("board")
        board_theme = self._theme.get_board_theme()

        for r in range(board.size):
            for c in range(board.size):
                color = (
                    board_theme.get(BoardColor.LIGHT) if (r + c) % 2 == 0 else board_theme.get(BoardColor.DARK)
                )

                self._canvas.create_rectangle(
                    c * self._square_size,
                    r * self._square_size,
                    (c + 1) * self._square_size,
                    (r + 1) * self._square_size,
                    fill=color,
                    outline="",
                    tags="board"
                )

    def draw_piece(self, row: int, col: int, piece):
        """Draws a piece on the board at the specified location."""
        if piece is None or piece.is_empty:
            return
        self._piece_renderer.draw_piece(row, col, piece)

    def draw_all_pieces(self, board: Board):
        """Draws all pieces on the board based on the current state."""
        for r in range(board.size):
            for c in range(board.size):
                piece = board.get_piece(r, c)
                self.draw_piece(r, c, piece)

    def move_piece(self, board: Board, move: Move):
        """Animates a piece moving
        from its start position to its end position, and handles captures."""
        piece = board.get_piece(move.start_row, move.start_col)
        if piece.is_empty:
            return

        self._piece_renderer.animate_move(piece, move.start_row, move.start_col,
                                         move.end_row, move.end_col)

        # Remove captured pieces --- IGNORE ---
        for r, c in move.captured:
            board.set_piece(r, c, Piece(piece.element, Team.NONE))
            self._canvas.delete(f"piece_{r}_{c}")

    def square_size(self) -> int:
        """Returns the size of each square on the board."""
        return self._square_size