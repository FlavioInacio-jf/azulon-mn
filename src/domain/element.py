from enum import Enum

class Element(Enum):
    """Enumeration of game elements with associated weights (pontos)."""
    EMPTY = 0
    FIRE = 1
    WATER = 2
    EARTH = 3
    AIR = 4

    @classmethod
    def get_weight(cls, element: "Element") -> int:
        """Return the weight (pontos) of a given element."""
        weights = {
            cls.EMPTY: 0,
            cls.FIRE: 3,
            cls.WATER: 2,
            cls.EARTH: 1,
            cls.AIR: 1
        }
        return weights.get(element, 0)

    @classmethod
    def get_all(cls) -> list["Element"]:
        """Return all elements excluding EMPTY."""
        return [cls.FIRE, cls.WATER, cls.EARTH, cls.AIR]