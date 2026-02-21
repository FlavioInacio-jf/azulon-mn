from enum import Enum, auto

class Team(Enum):
    """Enumeration of game teams."""
    NONE = auto()
    RED = auto()
    BLUE = auto()

    def opponent(self):
        """Returns the opposing team."""
        return Team.BLUE if self == Team.RED else Team.RED

