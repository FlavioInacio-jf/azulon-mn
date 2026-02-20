from dataclasses import dataclass

@dataclass
class Move:
    """Represents a move in the game, including start and end positions and any captured pieces."""
    start_row: int
    start_col: int
    end_row: int
    end_col: int
    captured: list[tuple[int, int]]