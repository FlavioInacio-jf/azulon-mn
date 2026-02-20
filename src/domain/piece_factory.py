import random
from src.domain.piece import Piece
from src.domain.element import Element
from src.domain.team import Team

class PieceFactory:
    """Factory class to create game pieces based on elemental types and team affiliation."""
    BASE_ELEMENTS = Element.get_all()

    @classmethod
    def create_team_set(cls, team: Team) -> list[Piece]:
        """Creates a set of pieces for a given team, including base and extra pieces."""
        base_pieces = [Piece(el, team) for el in cls.BASE_ELEMENTS]

        # Generate 2 extra pieces with random elements for the team
        extra_elements = random.choices(cls.BASE_ELEMENTS, k=2)
        extra_pieces = [Piece(el, team) for el in extra_elements]
        all_pieces = extra_pieces + base_pieces

        return all_pieces