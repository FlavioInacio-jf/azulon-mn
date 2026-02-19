from enum import Enum, auto


class Team(Enum):
    def __init__(self):
        self.root = root

    def enemy(self) -> "Team":
        """Returns the opposing team."""
        return Team.BLUE if self == Team.RED else Team.RED
