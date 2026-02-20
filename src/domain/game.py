from typing import Optional, Dict, List
from src.domain.board import Board
from src.domain.move import Move
from src.domain.team import Team

class Game:
    """Manages the overall game state, including the board, turns, and scoring."""
    def __init__(self, board: Board):
        self._board = board
        self._current_turn: Team = Team.RED
        self._scores: Dict[Team, int] = {Team.RED: 0, Team.BLUE: 0}

    def initialize(self) -> None:
        """Initializes the game by setting up the board and resetting scores."""
        self._board.initialize()
        self._scores = {Team.RED: 0, Team.BLUE: 0}

    @property
    def board(self) -> Board:
        """Returns the current game board."""
        return self._board

    @property
    def current_turn(self) -> Team:
        """Returns the current player's turn."""
        return self._current_turn

    @property
    def scores(self) -> Dict[Team, int]:
        """Returns the current scores for each team."""
        return self._scores

    def switch_turn(self) -> None:
        """Switches the current player's turn."""
        self._current_turn = Team.RED if self._current_turn == Team.BLUE else Team.BLUE

    def apply_move(self, move: Move) -> None:
        """Applies a move to the game state, including piece movement and captures."""
        piece = self._board.get_piece(move.start_row, move.start_col)
        if piece.is_empty:
            return

        self._board.place_piece(move.end_row, move.end_col, piece)
        self._board.remove_piece(move.start_row, move.start_col)

        for r, c in move.captured:
            captured_piece = self._board.get_piece(r, c)
            self._scores[piece.team] += captured_piece.weight
            self._board.remove_piece(r, c)

        self.switch_turn()

    def get_valid_moves(self, row: int, col: int) -> List[Move]:
        """Returns a list of valid moves for the piece at (row, col)."""
        piece = self._board.get_piece(row, col)
        if piece.is_empty or piece.team is None:
            return []

        valid_moves: List[Move] = []

        # Determine movement directions based on team
        directions = [(-1, -1), (-1, 1)] if piece.team == Team.RED else [(1, -1), (1, 1)]

        # Valid moves (moving to an adjacent empty square)
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc


            is_valid_simple_move = (
                self._board.in_bounds(new_row, new_col) and
                self._board.get_piece(new_row, new_col).is_empty
            )
            if is_valid_simple_move:
                valid_moves.append(Move(row, col, new_row, new_col, []))

        # Capture moves (jumping over an opponent's piece)
        for dr, dc in directions:
            mid_row, mid_col = row + dr, col + dc
            end_row, end_col = row + 2*dr, col + 2*dc
            if self._board.in_bounds(end_row, end_col):
                mid_piece = self._board.get_piece(mid_row, mid_col)
                end_piece = self._board.get_piece(end_row, end_col)

                can_capture = (
                    not mid_piece.is_empty and
                    mid_piece.team != piece.team and
                    end_piece.is_empty
                )

                if can_capture:
                    valid_moves.append(Move(row, col, end_row, end_col, [(mid_row, mid_col)]))

        return valid_moves

    def calculate_winner(self) -> Optional[Team]:
        """Determines the winner based on current scores."""
        if self._scores[Team.RED] > self._scores[Team.BLUE]:
            return Team.RED
        elif self._scores[Team.BLUE] > self._scores[Team.RED]:
            return Team.BLUE
        return None  # empate