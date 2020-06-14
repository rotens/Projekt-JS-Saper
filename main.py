import tkinter as tk

import board
import game_window
import minesweeper


def main():
    # Inicjalizacja biblioteki Tkinter
    root = tk.Tk()
    # Zablokowanie możliwości zmiany rozmiaru okna
    root.resizable(width=False, height=False)
    # Tworzenie obiektu klasy GameWindow
    # Do konstruktora przekazywany jest główny widget
    gw = game_window.GameWindow(master=root)
    # Tworzenie obiektu klasy Board
    game_board = board.Board()
    # Tworzenie obiektu klasu Minesweeper
    # Do konstruktora przekazywany jest obiekt klasy GameWindow oraz obiekt klasy Board
    ms = minesweeper.Minesweeper(game_board, gw)
    # Rozpoczęcie gry
    ms.init_game()
    root.mainloop()


if __name__ == "__main__":
    main()

