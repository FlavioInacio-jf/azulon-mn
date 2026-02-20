from src.domain.element import Element
from src.domain.piece import Piece
from src.domain.piece_factory import PieceFactory
from src.domain.team import Team


class Board:
    """Represents the logical game board state."""
    def __init__(self, size: int = 6):
        self.size = size
        self.grid: list[list[Piece | None]] = [
            [None] * size for _ in range(size)
        ]

    def initialize(self):
        """Populate board with starting pieces."""

        red = PieceFactory.create_team_set(Team.RED)
        blue = PieceFactory.create_team_set(Team.BLUE)

        pos_blue = [(0,1),(0,3),(0,5),(1,0),(1,2),(1,4)]
        pos_red  = [(4,1),(4,3),(4,5),(5,0),(5,2),(5,4)]

        for (r, c), piece in zip(pos_blue, blue):
            self.grid[r][c] = piece

        for (r, c), piece in zip(pos_red, red):
            self.grid[r][c] = piece

    def place_piece(self, row: int, col: int, piece: Piece):
        """Places a piece on the board at the specified location."""
        self.grid[row][col] = piece

    def remove_piece(self, row: int, col: int):
        """Removes a piece from the board, setting it to empty."""
        self.grid[row][col] = Piece(Element.EMPTY, None)

    def get_piece(self, row: int, col: int) -> Piece:
        """Returns the piece at the specified location."""
        return self.grid[row][col]

    def get_size(self) -> int:
        """Returns the size of the board."""
        return self.size

    def in_bounds(self, row: int, col: int) -> bool:
        """Checks if the given position is within the bounds of the board."""
        return 0 <= row < self.size and 0 <= col < self.size
