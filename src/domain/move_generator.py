from typing import List
from src.domain.board import Board
from src.domain.move import Move
from src.domain.team import Team


class MoveGenerator:
    """Encapsulates all movement rules of the game."""

    def __init__(self, board: Board):
        """Manages the overall game state, including the board, current turn, and scores."""
        self._board = board

    def get_valid_moves(self, row: int, col: int) -> List[Move]:
        """Returns valid moves for a piece (simple moves + single captures)."""
        piece = self._board.get_piece(row, col)
        if piece.is_empty or piece.team is None:
            return []

        moves: List[Move] = []

        directions = [(-1, -1), (-1, 1)] if piece.team == Team.RED else [(1, -1), (1, 1)]

        # simple moves
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if self._board.in_bounds(nr, nc) and self._board.get_piece(nr, nc).is_empty:
                moves.append(Move(row, col, nr, nc, []))

        capture_moves = self._get_capture_moves(row, col)

        if capture_moves:
            return capture_moves

        return moves

    def get_all_moves(self, team: Team) -> List[Move]:
        """Returns all valid moves for the given team."""
        moves: List[Move] = []

        for r in range(self._board.size):
            for c in range(self._board.size):
                piece = self._board.get_piece(r, c)

                if piece.is_empty or piece.team != team:
                    continue

                moves.extend(self.get_valid_moves(r, c))

        return moves

    def _get_capture_moves(self, row: int, col: int) -> List[Move]:
        """Returns valid capture moves for a piece, which involve jumping over an opponent's piece."""
        piece = self._board.get_piece(row, col)
        moves: List[Move] = []

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            mid_row, mid_col = row + dr, col + dc
            end_row, end_col = row + 2 * dr, col + 2 * dc

            if not self._board.in_bounds(end_row, end_col):
                continue

            mid_piece = self._board.get_piece(mid_row, mid_col)
            end_piece = self._board.get_piece(end_row, end_col)

            if mid_piece.is_empty:
                continue

            if mid_piece.team == piece.team:
                continue

            if not end_piece.is_empty:
                continue

            moves.append(Move(row, col, end_row, end_col, [(mid_row, mid_col)]))

        return moves