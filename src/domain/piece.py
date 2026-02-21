from dataclasses import dataclass
import random
from typing import Optional
from src.domain.element import Element
from src.domain.game_config import GameConfig
from src.domain.team import Team

@dataclass
class Piece:
    """Represents a game piece with an elemental type and team affiliation."""
    element: Element
    team: Optional[Team]

    @property
    def is_empty(self) -> bool:
        """Checks if the piece is empty (no element)."""
        return self.element == Element.EMPTY

    def weight(self, game_config: GameConfig) -> int:
        """Returns the weight of the piece based on its elemental type."""
        return Element.get_weight(self.element, game_config)

    @classmethod
    def create_team_set(cls, team: Team) -> list['Piece']:
        """Creates a set of pieces for a given team, including base and extra pieces."""
        BASE_ELEMENTS = Element.get_all()

        base_pieces = [Piece(el, team) for el in BASE_ELEMENTS]

        # Generate 2 extra pieces with random elements for the team
        extra_elements = random.choices(BASE_ELEMENTS, k=2)
        extra_pieces = [Piece(el, team) for el in extra_elements]
        all_pieces = extra_pieces + base_pieces

        return all_pieces