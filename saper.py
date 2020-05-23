import random
import time
import sys


class Field(object):

    def __init__(self):
        self.revealed = False
        self.mine = False
        self.value = 0

    def set_mine(self):
        self.mine = True

    def is_mine(self):
        return self.mine
    
    def set_value(self, value):
        self.value = value 

    def get_value(self):
        return self.value

    def set_revealed(self):
        self.revealed = True

    def is_revealed(self):
        return self.revealed


class Board(object):

    def __init__(self, height, width, mines=0):
        self.height = height
        self.width = width
        if not mines:
            self.mines = int((height * width) * 0.15)
        self._create_board()
        self._generate_mines()
        self._set_fields_values()

    def get_field(self, row, col):
        return self.board[row][col]

    def _create_board(self):
        self.board = [[Field() for _ in range(self.width)]
                      for _ in range(self.height)]

    def _generate_mines(self):
        mines_left = self.mines
        random.seed(1121)
        while mines_left > 0:
            gen_row = random.randint(0, self.height-1)
            gen_col = random.randint(0, self.width-1)
            if not self.board[gen_row][gen_col].is_mine():
                self.board[gen_row][gen_col].set_mine()
                mines_left -= 1

    def _set_fields_values(self):
        for row in range(self.height):
            for col in range(self.width):
                value = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0:
                            continue
                        if row + x < 0 or col + y < 0:
                            continue
                        try:
                            if self.board[row + x][col + y].is_mine():
                                value += 1
                        except IndexError:
                            continue
                self.board[row][col].set_value(value)

    def clear_field(self, row, col):
        if self.board[row][col].is_mine():
            return 1
        elif self.board[row][col].is_revealed():
            return 2
        else:
            self.board[row][col].set_revealed()
            if self.board[row][col].get_value() == 0:
                self._reveal(row, col)
            return 0

    def _reveal(self, row, col):
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i < 0 or j < 0:
                    continue
                try:
                    if not self.board[i][j].is_revealed() \
                            and not self.board[i][j].is_mine():
                        if self.board[i][j].get_value() > 0:
                            self.board[i][j].set_revealed()
                        else:
                            self.board[i][j].set_revealed()
                            self._reveal(i, j)
                except IndexError:
                    continue

    def print_board(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col].is_revealed():
                    if self.board[row][col].is_mine():
                        print("*  ", end='')
                    else:
                        print("{}  ".format(self.board[row][col].get_value()), end='')
                else:
                    print("#  ", end='')
            print()

    def print_board2(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col].is_mine():
                    print("*  ", end='')
                else:
                    print("{}  ".format(self.board[row][col].get_value()), end='')
            print()


if __name__ == "__main__":
    board = Board(9, 9)
    board.print_board()
    random.seed(int(time.time()))
    # x = random.randint(0, 8)
    # y = random.randint(0, 8)
    # while board.clear_field(x, y) != 2:
    #     x = random.randint(0, 8)
    #     y = random.randint(0, 8)
    board.clear_field(0, 0)
    board.clear_field(0, 2)
    #board.clear_field(1, 5)
    print()
    board.print_board()
    print()
    board.print_board2()

