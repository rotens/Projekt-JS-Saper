import tkinter as tk


FIELD_WIDTH = 2
FIELD_HEIGHT = 1
PAD_Y = 5

# Kolory
BASE03 = "#002b36"
BASE02 = "#073642"
BASE01 = "#586e75"
BASE00 = "#657b83"
BASE0 = "#839496"
BASE1 = "#93a1a1"
BASE2 = "#eee8d5"
BASE3 = "#fdf6e3"
YELLOW = "#b58900"
ORANGE = "#cb4b16"
RED = "#dc322f"
MAGENTA = "#d33682"
VIOLET = "#6c71c4"
BLUE = "#268bd2"
CYAN = "#2aa198"
GREEN = "#859900"
WHITE = "#FFFFFF"


class GameWindow(tk.Frame):
    values_colors = {
        1: BLUE,
        2: GREEN,
        3: RED,
        4: VIOLET,
        5: CYAN,
        6: YELLOW,
        7: MAGENTA,
        8: BASE1
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.fields = []
        self.top_frame = tk.Frame(master=self)
        self.board_frame = tk.Frame(master=self)
        self.bottom_frame = tk.Frame(master=self)
        self.top_frame.pack()
        self.board_frame.pack()
        self.bottom_frame.pack()
        self.pack()

    def init_window(self):
        self["bg"] = BASE02
        self._draw_top_frame()
        self._initial_board()
        self._draw_bottom_frame()

    def draw_message(self, message, color="black"):
        if color == "red":
            color = RED
        elif color == "green":
            color = GREEN
        self.lb_message["fg"] = color
        self.lb_message["text"] = message

    def draw_flag_counter(self, board):
        self.lb_flags_number["text"] = board.flagged_fields

    def draw_mines_number(self, board):
        self.lb_mines_number["text"] = board.mines

    def draw_board(self, board):
        self.fields = [[tk.Button(master=self.board_frame) for _ in row]
                       for row in board.fields]

        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                field["bg"] = BASE00
                field["height"] = FIELD_HEIGHT
                field["width"] = FIELD_WIDTH
                field.grid(row=i, column=j)

    def draw_mines(self, board, row, col):
        for i, j in board.mines_cords:
            self.fields[i][j]["text"] = "*"
            self.fields[i][j]["disabledforeground"] = WHITE
            self.fields[i][j]["bg"] = BASE02
            self.fields[i][j]["relief"] = tk.SUNKEN
            self.fields[i][j]["state"] = tk.DISABLED

        self.fields[row][col]["disabledforeground"] = RED

    def update_fields(self, board):
        for row, col in board.modified_fields:
            if not board.fields[row][col].mine:
                self.fields[row][col]["relief"] = tk.SUNKEN
                self.fields[row][col]["state"] = tk.DISABLED
                self.fields[row][col]["bg"] = BASE02
                self.fields[row][col].unbind("<Button-3>")
                if board.get_value(row, col) != 0:
                    self.fields[row][col]["text"] = board.get_value(row, col)
                    color = GameWindow.values_colors[board.get_value(row, col)]
                    self.fields[row][col]["disabledforeground"] = color

    def destroy_fields(self):
        for _, row in enumerate(self.fields):
            for _, field in enumerate(row):
                field.destroy()

    def draw_flag(self, row, col, option):
        if option == 1:
            self.fields[row][col]["text"] = "F"
            self.fields[row][col]["fg"] = RED
            self.fields[row][col]["disabledforeground"] = RED
        elif option == 2:
            self.fields[row][col]["text"] = "?"
        else:
            self.fields[row][col]["text"] = ""

    def disable_fields(self):
        for _, row in enumerate(self.fields):
            for _, field in enumerate(row):
                field["state"] = tk.DISABLED
                field.unbind("<Button-3>")

    def cheat(self, board):
        for row, col in board.mines_cords:
            self.fields[row][col]["bg"] = BASE01

    def _initial_board(self):
        self.fields = [[tk.Button(master=self.board_frame) for _ in range(10)]
                       for _ in range(10)]

        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                field["height"] = FIELD_HEIGHT
                field["width"] = FIELD_WIDTH
                field["state"] = tk.DISABLED
                field["bg"] = BASE00
                field.grid(row=i, column=j)

    def _draw_top_frame(self):
        self.flags_mines_frame = tk.Frame(master=self.top_frame)
        self.flags_mines_frame.pack()

        self.lb_flags = tk.Label(master=self.flags_mines_frame, text="Flags:", bg=BASE02, fg=CYAN)
        self.lb_flags.grid(row=0, column=0)

        self.lb_flags_number = tk.Label(master=self.flags_mines_frame, text="0", bg=BASE02, fg=CYAN)
        self.lb_flags_number.grid(row=0, column=1)

        self.lb_mines = tk.Label(master=self.flags_mines_frame, text="Mines:", bg=BASE02, fg=CYAN)
        self.lb_mines.grid(row=0, column=2)

        self.lb_mines_number = tk.Label(master=self.flags_mines_frame, text="0", bg=BASE02, fg=CYAN)
        self.lb_mines_number.grid(row=0, column=3)

    def _draw_bottom_frame(self):
        self.bottom_frame["bg"] = BASE02
        self.bottom_frame["pady"] = PAD_Y

        self.lb_message = tk.Label(master=self.bottom_frame, bg=BASE02)
        self.lb_message.pack()

        self.entries_frame = tk.Frame(master=self.bottom_frame, bg=BASE02, pady=PAD_Y)
        self.entries_frame.pack()

        self.ent_rows = tk.Entry(master=self.entries_frame, width=3, bg=BASE1, justify=tk.CENTER)
        self.ent_rows.insert(0, "10")
        self.ent_rows.grid(row=0, column=0)

        self.lb_x = tk.Label(master=self.entries_frame, text="x", bg=BASE02, fg=CYAN)
        self.lb_x.grid(row=0, column=1)

        self.lb_m = tk.Label(master=self.entries_frame, text="m:", bg=BASE02, fg=CYAN)
        self.lb_m.grid(row=0, column=3)

        self.ent_columns = tk.Entry(master=self.entries_frame, width=3, bg=BASE1, justify=tk.CENTER)
        self.ent_columns.insert(0, "10")
        self.ent_columns.grid(row=0, column=2)

        self.ent_mines = tk.Entry(master=self.entries_frame, width=3, bg=BASE1, justify=tk.CENTER)
        self.ent_mines.insert(0, "20")
        self.ent_mines.grid(row=0, column=4)

        self.btn_start_game = tk.Button(master=self.bottom_frame, text="Start game", bg=BASE1)
        self.btn_start_game.pack()
