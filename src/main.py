"""Main entry point for the Checkers game GUI."""

import tkinter as tk

from src.domain.board import Board
from src.domain.game import Game
from src.game.game_renderer import GameRenderer

if __name__ == "__main__":
    root = tk.Tk()

    board = Board(6) # Initialize a 6x6 board
    game = Game(board)
    game.initialize() # Set up the initial game state

    GameRenderer(root, game)
    root.mainloop()
