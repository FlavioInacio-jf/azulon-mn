import random
from src.domain.piece import Piece
from src.domain.element import Element
from src.domain.team import Team

class PieceFactory:
    """Factory class to create game pieces based on elemental types and team affiliation."""
    BASE_ELEMENTS = Element.get_all()

    @classmethod
    def create_team_set(cls, team: Team) -> list[Piece]:
        """Creates a set of pieces for a given team,
        including base elements and random duplicates."""
        random_elements = random.choices(cls.BASE_ELEMENTS, k=2)
        elements = cls.BASE_ELEMENTS + random_elements
        return [Piece(el, team) for el in elements]