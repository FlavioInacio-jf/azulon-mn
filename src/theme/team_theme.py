from src.domain.team import Team


TEAM_THEME = {
    Team.RED: "#e74c3c",
    Team.BLUE: "#3498db",
    Team.NONE: "#aaaaaa"
}

class TeamTheme:
    """Provides color themes for teams."""

    def get(self, team: Team) -> str:
        """Returns the color associated with a given team."""
        return TEAM_THEME[team]
