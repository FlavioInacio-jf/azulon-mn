from typing import Optional, Dict, List
from src.domain.board import Board
from src.domain.move import Move
from src.domain.team import Team

class Game:
    """Manages the overall game state, including the board, current turn, and scores."""
    def __init__(self, board: Board):
        """Manages the overall game state, including the board, current turn, and scores."""
        self._board = board
        self._current_turn: Team = Team.RED
        self._scores: Dict[Team, int] = {Team.RED: 0, Team.BLUE: 0}
        self.selected_row: Optional[int] = None
        self.selected_col: Optional[int] = None

    def initialize(self) -> None:
        """Initializes the game state, setting up the board and resetting scores."""
        self._board.initialize()
        self._scores = {Team.RED: 0, Team.BLUE: 0}
        self.selected_row = None
        self.selected_col = None
        self._current_turn = Team.RED

    @property
    def board(self) -> Board:
        """Returns the current state of the game board."""
        return self._board

    @property
    def current_turn(self) -> Team:
        """Returns the team whose turn it currently is."""
        return self._current_turn

    @property
    def scores(self) -> Dict[Team, int]:
        """Returns the current scores for both teams."""
        return self._scores

    def switch_turn(self) -> None:
        """Switches the current player's turn."""
        self._current_turn = Team.RED if self._current_turn == Team.BLUE else Team.BLUE

    def select_piece(self, row: int, col: int) -> bool:
        """Selects a piece at the given location if it belongs to the current player. Returns True if selection is successful."""
        piece = self._board.get_piece(row, col)
        if piece.is_empty or piece.team != self._current_turn:
            return False
        self.selected_row = row
        self.selected_col = col
        return True

    def move_selected_piece(self, dest_row: int, dest_col: int) -> Optional[Move]:
        """Attempts to move the selected piece to the specified destination. Returns the Move if successful, or None if invalid."""
        if self.selected_row is None or self.selected_col is None:
            return None

        valid_moves = self.get_valid_moves(self.selected_row, self.selected_col)
        move = next((m for m in valid_moves if m.end_row == dest_row and m.end_col == dest_col), None)
        if move:
            self.apply_move(move)
            if move.captured and self.has_additional_capture(move.end_row, move.end_col):
                self.selected_row, self.selected_col = move.end_row, move.end_col
            else:
                self.selected_row = None
                self.selected_col = None
                self.switch_turn()
            return move

        self.selected_row = None
        self.selected_col = None
        return None

    def apply_move(self, move: Move) -> None:
        """Applies the given move to the board, updating piece positions and scores."""
        piece = self._board.get_piece(move.start_row, move.start_col)
        if piece.is_empty:
            return

        self._board.set_piece(move.end_row, move.end_col, piece)
        self._board.remove_piece(move.start_row, move.start_col)

        for r, c in move.captured:
            captured_piece = self._board.get_piece(r, c)
            self._scores[piece.team] += captured_piece.weight
            self._board.remove_piece(r, c)

    def get_valid_moves(self, row: int, col: int) -> List[Move]:
        """Returns a list of valid moves for the piece at the given location."""
        piece = self._board.get_piece(row, col)
        if piece.is_empty or piece.team is None:
            return []

        moves: List[Move] = []
        directions = [(-1, -1), (-1, 1)] if piece.team == Team.RED else [(1, -1), (1, 1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if self._board.in_bounds(nr, nc) and self._board.get_piece(nr, nc).is_empty:
                moves.append(Move(row, col, nr, nc, []))

        moves.extend(self._get_capture_moves(row, col))

        return moves

    def _get_capture_moves(self, row: int, col: int, visited=None) -> List[Move]:
        """Recursively finds all valid capture moves for the piece at the given location."""
        if visited is None:
            visited = set()

        piece = self._board.get_piece(row, col)
        moves: List[Move] = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            mid_row, mid_col = row + dr, col + dc
            end_row, end_col = row + 2*dr, col + 2*dc

            if not self._board.in_bounds(end_row, end_col):
                continue

            mid_piece = self._board.get_piece(mid_row, mid_col)
            end_piece = self._board.get_piece(end_row, end_col)

            if mid_piece.is_empty or mid_piece.team == piece.team or not end_piece.is_empty:
                continue

            if (mid_row, mid_col, end_row, end_col) in visited:
                continue

            new_visited = visited | {(mid_row, mid_col, end_row, end_col)}
            move = Move(row, col, end_row, end_col, [(mid_row, mid_col)])

            subsequent = self._get_capture_moves(end_row, end_col, new_visited)
            if subsequent:
                for sub in subsequent:
                    moves.append(Move(row, col, sub.end_row, sub.end_col, move.captured + sub.captured))
            else:
                moves.append(move)

        return moves

    def has_additional_capture(self, row: int, col: int) -> bool:
        """Checks if the piece at the given location has any valid capture moves."""
        return any(m.captured for m in self.get_valid_moves(row, col))