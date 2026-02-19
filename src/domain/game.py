from src.domain.board import Board

class Game:
    """Manages the overall game state, including the board, selected pieces, and turn management."""
    def __init__(self, board: Board = None):
        self.board = board
        self.selected: tuple[int, int] | None = None
        self.turn = None

    def initialize(self):
        """Sets up the initial game state, populating the board with pieces."""
        self.board.initialize()

    def click(self, row: int, col: int):
        """Handles a click on the board, selecting or moving pieces as needed."""
        if self.selected:
            r_old, c_old = self.selected
            self.board.move(r_old, c_old, row, col)
            self.selected = None
        else:
            self.selected = (row, col)
