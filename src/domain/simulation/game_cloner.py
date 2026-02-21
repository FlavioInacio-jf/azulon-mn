import copy

from src.domain.game import Game


class GameCloner:
    """Utility class to create deep copies of Game instances for use in simulations."""
    def clone(self, game: Game):
        """Creates a deep copy of the given Game instance."""
        new_game = game.__class__(game.board.clone())
        new_game.set_current_turn(game.current_turn())
        new_game.set_scores(copy.deepcopy(game.scores()))
        new_game.set_selected_piece(*game.selected_piece() if game.selected_piece() else (None, None))
        return new_game