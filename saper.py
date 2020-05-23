import random
import time


class Field(object):

    def __init__(self):
        self.revealed = False
        self.mine = False
        self.value = 0
        self.flag = False

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

    def set_flag(self):
        self.flag = True

    def is_flagged(self):
        return self.flag


class Board(object):

    def __init__(self, height, width, mines=0):
        self.height = height
        self.width = width
        if not mines:
            self.mines = int((height * width) * 0.15)
        self._create_board()
        self._generate_mines()
        self._flagged_mines = 0
        self._flagged_fields = 0
        self._unrevealed_fields = height * width - self.mines

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
                self._increment_fields_values(gen_row, gen_col)
                mines_left -= 1

    def _increment_fields_values(self, row, col):
        for x in range(row-1, row+2):
            for y in range(col-1, col+2):
                if x < 0 or y < 0:
                    continue
                try:
                    cur_val = self.board[x][y].get_value()
                    self.board[x][y].set_value(cur_val+1)
                except IndexError:
                    continue

    def clear_field(self, row, col):
        if self.board[row][col].is_mine():
            return 1
        elif self.board[row][col].is_revealed():
            return 2
        else:
            self.board[row][col].set_revealed()
            self._unrevealed_fields -= 1
            if self.board[row][col].get_value() == 0:
                self._reveal(row, col)
            return 0

    def _reveal(self, row, col):
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i < 0 or j < 0:
                    continue
                try:
                    if not self.board[i][j].is_revealed():
                        self.board[i][j].set_revealed()
                        self._unrevealed_fields -= 1
                        if self.board[i][j].get_value() == 0:
                            self._reveal(i, j)
                except IndexError:
                    continue

    def get_field(self, row, col):
        return self.board[row][col]

    def flag_field(self, row, col):
        if self._flagged_fields == self.mines:
            return 1
        if self.board[row][col].is_mine():
            self._flagged_mines += 1
        self.board[row][col].set_flag()
        self._flagged_fields += 1
        return 0

    def check_state(self):
        if self._unrevealed_fields == 0:
            return 1
        if self._flagged_mines == self.mines:
            return 1
        return 0

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
    random.seed(int(time.time()))
    # x = random.randint(0, 8)
    # y = random.randint(0, 8)
    # while board.clear_field(x, y) != 2:
    #     x = random.randint(0, 8)
    #     y = random.randint(0, 8)
    board.clear_field(0, 0)
    board.clear_field(0, 2)
    board.clear_field(0, 8)
    #board.clear_field(1, 5)
    print()
    board.print_board()
    print()
    board.print_board2()

