"""Main entry point for the Checkers game GUI."""

import tkinter as tk

from src.config.config import ConfigLoader
from src.domain.board import Board
from src.domain.game import Game
from src.domain.game_config import GameConfig
from src.domain.move_generator import MoveGenerator
from src.game.game_renderer import GameRenderer

if __name__ == "__main__":
    cfg = ConfigLoader(load_dotenv_file=True)
    cfg.load_env_file()

    root = tk.Tk()

    # Load game configuration from environment variables
    water_weight = cfg.get_env_var("WATER_WEIGHT", 0.25)
    earth_weight = cfg.get_env_var("EARTH_WEIGHT", 0.25)
    fire_weight = cfg.get_env_var("FIRE_WEIGHT", 0.25)
    air_weight = cfg.get_env_var("AIR_WEIGHT", 0.25)
    minimax_depth = cfg.get_env_var("MINIMAX_DEPTH", 3)
    empty_weight = cfg.get_env_var("EMPTY_WEIGHT", 0.0)

    game_config = GameConfig(
        water_weight=float(water_weight),
        earth_weight=float(earth_weight),
        fire_weight=float(fire_weight),
        air_weight=float(air_weight),
        empty_weight=float(empty_weight),
        minimax_depth=int(minimax_depth)
    )

    SQUARE_SIZE = 80 # Size of each square on the board

    # Initialize the game state
    board = Board(6) # Initialize a 6x6 board
    game = Game(board, MoveGenerator(board), game_config=game_config) # Create the game instance with the board, move generator, and game configuration
    game.initialize() # Set up the initial game state

    # Create the game renderer and start the main loop
    game_renderer = GameRenderer(
        root=root,
        game=game,
        square_size=SQUARE_SIZE)
    game_renderer.initialize()

    root.mainloop()
