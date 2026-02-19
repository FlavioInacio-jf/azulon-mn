from src.theme.board_theme import BoardTheme
from src.theme.piece_theme import PIECE_THEME
from src.theme.team_theme import TeamTheme


class ThemeManager:
    """Centralizes access to board and team color themes."""
    board_theme = BoardTheme()
    team_theme = TeamTheme()
    piece_theme = PIECE_THEME

    def get_team_theme(self) -> TeamTheme:
        """Returns the color associated with a given team."""
        return self.team_theme

    def get_board_theme(self) -> BoardTheme:
        """Returns the board theme."""
        return self.board_theme

    def get_piece_theme(self) -> PIECE_THEME:
        """Returns the piece theme."""
        return self.piece_theme