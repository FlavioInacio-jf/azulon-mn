import math
from typing import Optional

from src.domain.game import Game
from src.domain.move import Move
from src.domain.simulation.game_cloner import GameCloner
from src.domain.team import Team

def evaluate(game: Game, team: Team):
    """Evaluation function to score the game state from the perspective of the given team."""
    return game.get_weighted_score(team) - game.get_weighted_score(team.opponent())


def minimax(game: Game, depth: int, maximizing: bool, team: Team) -> tuple[float,  Optional[Move]]:
    """Minimax algorithm to determine the best move for a given game state."""
    gamer_cloner = GameCloner()

    if depth == 0 or game.is_game_over():
        return evaluate(game, team), None

    current_team = team if maximizing else team.opponent()
    moves = game.get_all_moves(current_team)

    if not moves:
        return evaluate(game, team), None

    best_move = None

    if maximizing:
        max_eval = -math.inf

        for move in moves:
            new_game = gamer_cloner.clone(game)
            new_game.apply_move(move)

            eval_score, _ = minimax(new_game, depth-1, False, team)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

        return max_eval, best_move

    else:
        min_eval = math.inf

        for move in moves:
            new_game = gamer_cloner.clone(game)
            new_game.apply_move(move)

            eval_score, _ = minimax(new_game, depth-1, True, team)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

        return min_eval, best_move