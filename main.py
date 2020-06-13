import tkinter as tk

import Board
import GameWindow
import Minesweeper


def main():
    root = tk.Tk()
    root.resizable(width=False, height=False)
    gw = GameWindow.GameWindow(master=root)
    board = Board.Board()
    ms = Minesweeper.Minesweeper(board, gw)
    ms.init_game()
    gw.mainloop()


if __name__ == "__main__":
    main()

