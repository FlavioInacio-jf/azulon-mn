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

    def place(self, row: int, col: int, piece: Piece):
        """Places a piece on the board at the specified location."""
        self.grid[row][col] = piece

    def move(self, r1: int, c1: int, r2: int, c2: int):
        """Moves a piece from one location to another on the board."""
        piece = self.grid[r1][c1]
        self.grid[r2][c2] = piece
        self.grid[r1][c1] = None

    def pieces(self):
        """Iterates over board pieces with coordinates."""
        for r in range(self.size):
            for c in range(self.size):
                piece = self.grid[r][c]
                if piece:
                    yield r, c, piece
