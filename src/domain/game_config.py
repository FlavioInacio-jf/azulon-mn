class GameConfig:
    """
    Game configuration loaded from environment variables.
    """

    def __init__(
        self,
        water_weight: float,
        earth_weight: float,
        fire_weight: float,
        air_weight: float,
        empty_weight: float,
        minimax_depth: int,
    ) -> None:
        self.water_weight = water_weight
        self.earth_weight = earth_weight
        self.fire_weight = fire_weight
        self.air_weight = air_weight
        self.empty_weight = empty_weight
        self.minimax_depth = minimax_depth