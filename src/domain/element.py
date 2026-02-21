from enum import Enum

from src.domain.game_config import GameConfig

class Element(Enum):
    """Enumeration of game elements with associated weights (pontos)."""
    EMPTY = 0
    FIRE = 1
    WATER = 2
    EARTH = 3
    AIR = 4

    @classmethod
    def get_weight(cls, element: "Element", game_config: GameConfig) -> int:
        """Return the weight (pontos) of a given element."""
        weights = {
            cls.EMPTY: game_config.empty_weight,
            cls.FIRE: game_config.fire_weight,
            cls.WATER: game_config.water_weight,
            cls.EARTH: game_config.earth_weight,
            cls.AIR: game_config.air_weight
        }
        return weights.get(element, 0)

    @classmethod
    def get_all(cls) -> list["Element"]:
        """Return all elements excluding EMPTY."""
        return [cls.FIRE, cls.WATER, cls.EARTH, cls.AIR]