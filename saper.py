import random
import time
import tkinter as tk


ROWS_MAX = 15
COLUMNS_MAX = 15
ROWS_MIN = 2
COLUMNS_MIN = 2
MINES_MIN = 0

FIELD_WIDTH = 2
FIELD_HEIGHT = 1


class BoardParametersError(Exception):
    pass


class Field(object):

    def __init__(self):
        self.revealed = False
        self.mine = False
        self.value = 0
        self.flag = False


class Board(object):

    def __init__(self):
        self.fields = []
        self.modified_fields = []
        self.rows = 0
        self.cols = 0
        self.mines = 0
        self._flagged_mines = 0
        self._flagged_fields = 0
        self._unrevealed_fields = 0

    def create_board(self, rows, cols, mines):
        if rows < ROWS_MIN or rows > ROWS_MAX:
            raise BoardParametersError()
        if cols < COLUMNS_MIN or cols > COLUMNS_MAX:
            raise BoardParametersError()
        if mines < MINES_MIN or mines > rows*cols:
            raise BoardParametersError()
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.fields = [[Field() for _ in range(self.cols)]
                       for _ in range(self.rows)]
        self._generate_mines()

    def _generate_mines(self):
        mines_left = self.mines
        random.seed(1121)
        while mines_left > 0:
            gen_row = random.randint(0, self.rows-1)
            gen_col = random.randint(0, self.cols-1)
            if not self.fields[gen_row][gen_col].mine:
                self.fields[gen_row][gen_col].mine = True
                self._increment_fields_values(gen_row, gen_col)
                mines_left -= 1

    def _increment_fields_values(self, row, col):
        for x in range(row-1, row+2):
            for y in range(col-1, col+2):
                if x < 0 or y < 0:
                    continue
                try:
                    self.fields[x][y].value += 1
                except IndexError:
                    continue

    def _get_mines_cords(self):
        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                if field.mine:
                    self.modified_fields.append((i, j))

    def clear_field(self, row, col):
        if self.fields[row][col].mine:
            self.fields[row][col].revealed = True
            self.modified_fields = []
            self._get_mines_cords()
            return 1
        elif self.fields[row][col].revealed:
            return 2
        else:
            self.fields[row][col].revealed = True
            self._unrevealed_fields -= 1
            self.modified_fields = [(row, col)]
            if self.fields[row][col].value == 0:
                self._reveal(row, col)
            return 0

    def _reveal(self, row, col):
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i < 0 or j < 0:
                    continue
                try:
                    if not self.fields[i][j].revealed:
                        self.fields[i][j].revealed = True
                        self._unrevealed_fields -= 1
                        self.modified_fields.append((i, j))

                        if self.fields[i][j].value == 0:
                            self._reveal(i, j)

                except IndexError:
                    continue

    def flag_field(self, row, col):
        if self._flagged_fields == self.mines:
            return 1
        if self.fields[row][col].mine:
            self._flagged_mines += 1
        self.fields[row][col].flag = True
        self._flagged_fields += 1
        return 0

    def check_state(self):
        if self._unrevealed_fields == 0:
            return 1
        if self._flagged_mines == self.mines:
            return 1
        return 0

    # def print_board(self):
    #     for row in range(self.rows):
    #         for col in range(self.cols):
    #             if self.fields[row][col].revealed:
    #                 if self.fields[row][col].mine:
    #                     print("*  ", end='')
    #                 else:
    #                     print("{}  ".format(self.fields[row][col].value), end='')
    #             else:
    #                 print("#  ", end='')
    #         print()

    # def print_board2(self):
    #     for row in range(self.rows):
    #         for col in range(self.cols):
    #             if self.fields[row][col].mine:
    #                 print("*  ", end='')
    #             else:
    #                 print("{}  ".format(self.fields[row][col].value), end='')
    #         print()


class DrawBoard(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.fields = []
        self.pack()

    def draw_board(self, board):
        self.fields = [[tk.Button(self, height=1, width=2) for _ in row]
                       for row in board.fields]

        for i, row in enumerate(self.fields):
            for j, el in enumerate(row):
                el.grid(row=i, column=j)

    def update_fields(self, board):
        for cords in board.modified_fields:
            row = cords[0]
            col = cords[1]
            if not board.fields[row][col].mine:
                self.fields[row][col].config(text=board.fields[row][col].value,
                                             relief="sunken")
            else:
                self.fields[row][col]['text'] = "*"
                self.fields[row][col]['fg'] = "red"
                self.fields[row][col]['relief'] = "sunken"

    def draw_mines(self, board, row, col):
        self.fields[row][col]['text'] = "*"
        self.fields[row][col]['fg'] = "red"
        self.fields[row][col]['relief'] = "sunken"

        for cords in board.modified_fields:
            row = cords[0]
            col = cords[1]
            self.fields[row][col]['text'] = "*"
            self.fields[row][col]['relief'] = "sunken"


class Controller(object):
    def __init__(self, board, db):
        self.board = board
        self.db = db
        self.create_events()

    def create_events(self):
        for i, row in enumerate(self.db.fields):
            for j, el in enumerate(row):
                el.config(command=lambda x=i, y=j: self.on_click(x, y))

    def on_click(self, row, col):
        if self.board.clear_field(row, col) == 1:
            self.db.draw_mines(self.board, row, col)
        else:
            self.db.update_fields(self.board)


if __name__ == "__main__":
    board = Board()
    board.create_board(15, 15, 30)
   #random.seed(int(time.time()))
    # x = random.randint(0, 8)
    # y = random.randint(0, 8)
    # while board.clear_field(x, y) != 2:
    #     x = random.randint(0, 8)
    #     y = random.randint(0, 8)
    #board.clear_field(0, 0)
    #board.print_board2()
    #game_input = Controller()
    root = tk.Tk()
    db = DrawBoard(master=root)
    db.draw_board(board)
    con = Controller(board, db)
    db.mainloop()


