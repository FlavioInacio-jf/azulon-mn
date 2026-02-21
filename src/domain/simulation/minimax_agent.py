
from src.domain.game import Game
from src.domain.simulation.minimax import minimax
from src.domain.team import Team


class MinimaxAgent:
    """Implements a minimax agent that uses the minimax algorithm to choose the best move."""
    def __init__(self, depth: int):
        self.depth = depth

    def choose_move(self, game: Game, team: Team):
        """Chooses the best move for the given game state and team using the minimax algorithm."""
        _, move = minimax(game, self.depth, True, team)
        return move