"""Moduł zawierający klasę odpowiedzialną za rysowanie okna gry."""


import tkinter as tk


# Wymiary pola (jednostka TKUNIT)
FIELD_WIDTH = 2
FIELD_HEIGHT = 1

ENTRY_WIDTH = 3
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
    """ Klasa odpowiedzialna za rysowanie okna gry. """

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
        self.top_frame = None
        self.board_frame = None
        self.bottom_frame = None
        self.flags_mines_frame = None
        self.lb_flags = None
        self.lb_flags_number = None
        self.lb_mines = None
        self.lb_mines_number = None
        self.lb_message = None
        self.entries_frame = None
        self.ent_rows = None
        self.lb_x = None
        self.lb_m = None
        self.ent_columns = None
        self.ent_mines = None
        self.btn_start_game = None

    def init_window(self):
        """Inicjalizuje okno gry."""
        self.top_frame = tk.Frame(master=self)
        self.board_frame = tk.Frame(master=self)
        self.bottom_frame = tk.Frame(master=self)
        self.top_frame.pack()
        self.board_frame.pack()
        self.bottom_frame.pack()
        self.pack()
        self["bg"] = BASE02
        self._draw_top_frame()
        self._initial_board()
        self._draw_bottom_frame()

    def draw_message(self, message, color="black"):
        """Rysuje komunikat o stanie gry."""
        if color == "red":
            color = RED
        elif color == "green":
            color = GREEN
        self.lb_message["fg"] = color
        self.lb_message["text"] = message

    def draw_flag_counter(self, board):
        """Rysuje licznik flag."""
        self.lb_flags_number["text"] = board.flagged_fields

    def draw_mines_number(self, board):
        """Rysuje licznik min."""
        self.lb_mines_number["text"] = board.mines

    def draw_board(self, board):
        """Rysuje główną planszę."""
        self.fields = [[tk.Button(master=self.board_frame) for _ in row]
                       for row in board.fields]

        for i, row in enumerate(self.fields):
            for j, field in enumerate(row):
                field["bg"] = BASE00
                field["height"] = FIELD_HEIGHT
                field["width"] = FIELD_WIDTH
                field.grid(row=i, column=j)

    def draw_mines(self, board, row, col):
        """Rysuje miny na planszy."""
        for i, j in board.mines_cords:
            self.fields[i][j]["text"] = "*"
            self.fields[i][j]["disabledforeground"] = WHITE
            self.fields[i][j]["bg"] = BASE02
            self.fields[i][j]["relief"] = tk.SUNKEN
            self.fields[i][j]["state"] = tk.DISABLED

        self.fields[row][col]["disabledforeground"] = RED

    def update_fields(self, board):
        """Aktualizuje wyglad pól."""
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
        """Niszczy przyciski reprezentujące pola."""
        for _, row in enumerate(self.fields):
            for _, field in enumerate(row):
                field.destroy()

    def draw_flag(self, row, col, option):
        """Rysuje flagę 'F' lub oznaczenie '?' w zależnosci od podanej opcji."""
        if option == 0:
            self.fields[row][col]["text"] = "F"
            self.fields[row][col]["fg"] = RED
            self.fields[row][col]["disabledforeground"] = RED
        elif option == 1:
            self.fields[row][col]["text"] = "?"
            self.fields[row][col]["fg"] = WHITE
            self.fields[row][col]["disabledforeground"] = WHITE
        else:
            self.fields[row][col]["text"] = ""

    def disable_fields(self):
        """Dezaktywuje przyciski reprezentujące pola."""
        for _, row in enumerate(self.fields):
            for _, field in enumerate(row):
                field["state"] = tk.DISABLED
                field.unbind("<Button-3>")

    def cheat(self, board):
        """Przyciemnia pola, pod którymi ukryte są miny."""
        for row, col in board.mines_cords:
            self.fields[row][col]["bg"] = BASE01

    def _initial_board(self):
        """Rysuje poczatkową, dezaktywowną planszę."""
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
        """Rysuje gorną ramkę okna gry."""
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
        """Rysuje dolną ramkę okna gry."""
        self.bottom_frame["bg"] = BASE02
        self.bottom_frame["pady"] = PAD_Y

        self.lb_message = tk.Label(master=self.bottom_frame, bg=BASE02)
        self.lb_message.pack()

        self.entries_frame = tk.Frame(master=self.bottom_frame, bg=BASE02, pady=PAD_Y)
        self.entries_frame.pack()

        self.ent_rows = tk.Entry(master=self.entries_frame, width=ENTRY_WIDTH,
                                 bg=BASE1, justify=tk.CENTER)
        self.ent_rows.insert(0, "10")
        self.ent_rows.grid(row=0, column=0)

        self.lb_x = tk.Label(master=self.entries_frame, text="x", bg=BASE02, fg=CYAN)
        self.lb_x.grid(row=0, column=1)

        self.lb_m = tk.Label(master=self.entries_frame, text="m:", bg=BASE02, fg=CYAN)
        self.lb_m.grid(row=0, column=3)

        self.ent_columns = tk.Entry(master=self.entries_frame, width=ENTRY_WIDTH,
                                    bg=BASE1, justify=tk.CENTER)
        self.ent_columns.insert(0, "10")
        self.ent_columns.grid(row=0, column=2)

        self.ent_mines = tk.Entry(master=self.entries_frame, width=ENTRY_WIDTH,
                                  bg=BASE1, justify=tk.CENTER)
        self.ent_mines.insert(0, "20")
        self.ent_mines.grid(row=0, column=4)

        self.btn_start_game = tk.Button(master=self.bottom_frame, text="Start game", bg=BASE1)
        self.btn_start_game.pack()
