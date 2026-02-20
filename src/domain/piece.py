from dataclasses import dataclass
from typing import Optional
from src.domain.element import Element
from src.domain.team import Team

ELEMENT_WEIGHTS = {
    Element.FIRE: 3,
    Element.WATER: 2,
    Element.EARTH: 1,
    Element.AIR: 1,
    Element.EMPTY: 0
}

@dataclass
class Piece:
    """Represents a game piece with an elemental type and team affiliation."""
    element: Element
    team: Optional[Team]

    @property
    def is_empty(self) -> bool:
        """Checks if the piece is empty (no element)."""
        return self.element == Element.EMPTY

    @property
    def weight(self) -> int:
        """Returns the weight of the piece based on its elemental type."""
        return ELEMENT_WEIGHTS.get(self.element, 0)