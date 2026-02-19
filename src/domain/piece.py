from dataclasses import dataclass
from src.domain.element import Element
from src.domain.team import Team

@dataclass
class Piece:
    """Represents a game piece with an elemental type and team affiliation."""
    element: Element
    team: Team

    @property
    def is_empty(self) -> bool:
        """Checks if the piece is empty (no element)."""
        return self.element == Element.EMPTY
