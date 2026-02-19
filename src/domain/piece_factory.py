import random

from src.domain.element import Element
from src.domain.team import Team
from src.domain.piece import Piece


class PieceFactory:
    """Generates elemental piece sets for a team."""

    BASE_ELEMENTS = [
        Element.FIRE,
        Element.WATER,
        Element.EARTH,
        Element.AIR
    ]

    @classmethod
    def create_team_set(cls, team: Team) -> list[Piece]:
        """Creates a set of pieces for a given team, including base and random elements."""
        random_elements = random.choices(cls.BASE_ELEMENTS, k=2)
        elements = cls.BASE_ELEMENTS + random_elements
        return [Piece(el, team) for el in elements]
