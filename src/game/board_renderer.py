"""Manages the game board state and rendering of pieces based on their elemental types."""
import tkinter as tk
from typing import Optional

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

        self._selected_piece: Optional[tuple[int,int]] = None
        self._valid_moves: list[tuple[int,int]] = []

    def selected_piece(self, row: int, col: int):
        """Sets the currently selected piece's position."""
        self._selected_piece = None if row is None or col is None else (row, col)

    def set_valid_moves(self, moves: list[tuple[int,int]]):
        """Sets the list of valid move positions for the currently selected piece."""
        self._valid_moves = moves

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

                square_number = r * board.size + c + 1
                self.draw_square_number(r, c, square_number)

        if self._selected_piece:
            sr, sc = self._selected_piece
            self._canvas.create_rectangle(
                sc*self._square_size,
                sr*self._square_size,
                (sc+1)*self._square_size,
                (sr+1)*self._square_size,
                outline=self._theme.get_board_theme().get(BoardColor.HIGHLIGHT),
                width=3,
                tags="highlight"
            )

        for vr, vc in self._valid_moves:
            cx = vc * self._square_size + self._square_size//2
            cy = vr * self._square_size + self._square_size//2
            radius = self._square_size//6
            self._canvas.create_oval(
                cx-radius, cy-radius,
                cx+radius, cy+radius,
                width=20,
                fill=self._theme.get_board_theme().get(BoardColor.HIGHLIGHT),
                outline=self._theme.get_board_theme().get(BoardColor.HIGHLIGHT),
                tags="highlight"
            )

    def draw_piece(self, row: int, col: int, piece):
        """Draws a piece on the board at the specified location."""
        if piece is None or piece.is_empty:
            return
        self._piece_renderer.draw_piece(row, col, piece)

    def draw_square_number(self, row: int, col: int, number: int):
        """Draws a number on the specified square, used for debugging or move hints."""
        cx = col * self._square_size + self._square_size // 2
        cy = row * self._square_size + self._square_size // 2

        color_light = self._theme.get_board_theme().get(BoardColor.LIGHT)
        color_dark = self._theme.get_board_theme().get(BoardColor.DARK)

        square_color = color_light if (row + col) % 2 == 0 else color_dark
        text_color = "#000000" if square_color == self._theme.get_board_theme().get(BoardColor.HIGHLIGHT) else "#efecec"

        self._canvas.create_text(
            cx, cy,
            text=str(number),
            fill=text_color,
            font=("Arial", self._square_size // 4, "bold"),
            tags="board"
        )

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
            self._piece_renderer.delete(r, c)

    def square_size(self) -> int:
        """Returns the size of each square on the board."""
        return self._square_size