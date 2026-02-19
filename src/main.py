"""Main entry point for the Checkers game GUI."""

import tkinter as tk
from src.game.game import Game

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
