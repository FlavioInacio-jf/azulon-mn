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
        self._selected_row: Optional[int] = None
        self._selected_col: Optional[int] = None

    def initialize(self) -> None:
        """Initializes the game state, setting up the board and resetting scores."""
        self._board.initialize()
        self._scores = {Team.RED: 0, Team.BLUE: 0}
        self._selected_row = None
        self._selected_col = None
        self._current_turn = Team.RED

    @property
    def board(self) -> Board:
        """Returns the current state of the game board."""
        return self._board

    def selected_piece(self) -> Optional[tuple[int, int]]:
        """Returns the position of the currently selected piece, or None if no piece is selected."""
        if self._selected_row is not None and self._selected_col is not None:
            return (self._selected_row, self._selected_col)
        return None

    def is_same_selected_piece(self, row: int, col: int) -> bool:
        """Checks if the given position is the same as the currently selected piece."""
        return self.selected_piece() == (row, col)

    def clear_selection(self) -> None:
        """Clears the currently selected piece."""
        self._selected_row = None
        self._selected_col = None

    def current_turn(self) -> Team:
        """Returns the team whose turn it currently is."""
        return self._current_turn

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
        self._selected_row = row
        self._selected_col = col
        return True

    def move_selected_piece(self, dest_row: int, dest_col: int) -> Optional[Move]:
        """Attempts to move the selected piece to the specified destination. Returns the Move if successful, or None if invalid."""
        if self._selected_row is None or self._selected_col is None:
            return None

        valid_moves = self.get_valid_moves(self._selected_row, self._selected_col)
        move = next((m for m in valid_moves if m.end_row == dest_row and m.end_col == dest_col), None)
        if move:
            self._apply_move(move)
            if move.captured and self._has_additional_capture(move.end_row, move.end_col):
                self._selected_row, self._selected_col = move.end_row, move.end_col
            else:
                self._selected_row = None
                self._selected_col = None

                self.switch_turn()
            return move

        self._selected_row = None
        self._selected_col = None
        return None


    def is_game_over(self) -> bool:
        """Checks if the game is over, which occurs when one team has no pieces left."""
        if self._has_team_no_pieces():
            return True

        if not self.has_any_valid_move(self._current_turn):
            return True

        return False

    def get_valid_moves(self, row: int, col: int) -> List[Move]:
        """Returns valid moves for a piece (simple moves + single captures)."""
        piece = self._board.get_piece(row, col)
        if piece.is_empty or piece.team is None:
            return []

        moves: List[Move] = []

        directions = [(-1, -1), (-1, 1)] if piece.team == Team.RED else [(1, -1), (1, 1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if self._board.in_bounds(nr, nc) and self._board.get_piece(nr, nc).is_empty:
                moves.append(Move(row, col, nr, nc, []))

        capture_moves = self._get_capture_moves(row, col)

        if capture_moves:
            return capture_moves

        moves.extend(capture_moves)
        return moves

    def get_winner(self) -> Optional[Team]:
        """Determines the winner of the game based on scores if one team has no pieces left."""
        if not self._has_team_no_pieces():
            return None

        red_score = self._scores.get(Team.RED, 0)
        blue_score = self._scores.get(Team.BLUE, 0)

        if red_score > blue_score:
            return Team.RED
        if blue_score > red_score:
            return Team.BLUE

        return None

    def _apply_move(self, move: Move) -> None:
        """Applies the given move to the board, updating piece positions and scores."""
        piece = self._board.get_piece(move.start_row, move.start_col)
        if piece.is_empty:
            return

        self._board.remove_piece(move.start_row, move.start_col)

        for r, c in move.captured:
            captured_piece = self._board.get_piece(r, c)
            self._scores[piece.team] += captured_piece.weight
            self._board.remove_piece(r, c)

        self._board.set_piece(move.end_row, move.end_col, piece)

    def _get_capture_moves(self, row: int, col: int) -> List[Move]:
        """Returns only single-step capture moves (no recursion)."""
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

            if mid_piece.is_empty:
                continue

            if mid_piece.team == piece.team:
                continue

            if not end_piece.is_empty:
                continue

            moves.append(Move(row, col, end_row, end_col, [(mid_row, mid_col)]))

        return moves

    def _has_additional_capture(self, row: int, col: int) -> bool:
        """Checks if the piece at the given location has any valid capture moves."""
        return any(m.captured for m in self.get_valid_moves(row, col))

    def has_any_valid_move(self, team: Team) -> bool:
        """Checks if a team has at least one valid move."""
        for r in range(self._board.size):
            for c in range(self._board.size):
                piece = self._board.get_piece(r, c)

                if piece.is_empty or piece.team != team:
                    continue

                if len(self.get_valid_moves(r, c)) > 0:
                    return True

        return False

    def _has_team_no_pieces(self) -> bool:
        """Checks if either team has no pieces left on the board."""
        red = 0
        blue = 0

        for r in range(self._board.size):
            for c in range(self._board.size):
                piece = self._board.get_piece(r, c)
                if piece.is_empty:
                    continue

                if piece.team == Team.RED:
                    red += 1
                else:
                    blue += 1

        return red == 0 or blue == 0



