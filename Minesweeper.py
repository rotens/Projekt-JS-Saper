from exceptions import BoardParametersError


class Minesweeper(object):
    def __init__(self, board, game_window):
        self.board = board
        self.gw = game_window

    def init_game(self):
        self.gw.init_window()
        self.gw.btn_start_game.bind("<Button-1>", lambda event: self._start_game())

    def _bind_events(self):
        for i, row in enumerate(self.gw.fields):
            for j, field in enumerate(row):
                field.config(command=lambda x=i, y=j: self._left_click(x, y))
                field.bind("<Button-3>", lambda event, x=i, y=j: self._right_click(x, y))

        self.gw.master.bind("xyzzy", lambda event: self._cheat())

    def _start_game(self):
        try:
            rows = int(self.gw.ent_rows.get())
            columns = int(self.gw.ent_columns.get())
            mines = int(self.gw.ent_mines.get())
        except ValueError:
            self.gw.draw_message("Incorrect board parameters", color="red")
            return

        try:
            self.board.create_board(rows, columns, mines)
        except BoardParametersError:
            self.gw.draw_message("Incorrect board parameters", color="red")
            return
        else:
            self.gw.destroy_fields()
            self.gw.draw_board(self.board)
            self._bind_events()
            self.gw.draw_message("")
            self.gw.draw_mines_number(self.board)
            self.gw.draw_flag_counter(self.board)

    def _left_click(self, row, col):
        """Funkcja wywoływana przy naciśnięciu pola lewym przyciskiem myszy"""
        val = self.board.clear_field(row, col)
        if val == 1:
            self.gw.draw_mines(self.board, row, col)
            self._end_game(option=0)
        elif val == 0:
            self.gw.update_fields(self.board)
        self._game_state()

    def _right_click(self, row, col):
        val = self.board.flag_field(row, col)

        option = 0
        if val == 0:
            option = 1
        elif val == 2:
            option = 2

        self.gw.draw_flag(row, col, option)
        self.gw.draw_flag_counter(self.board)
        self._game_state()

    def _game_state(self):
        state = self.board.check_state()
        if state == 1:
            self._end_game(option=1)

    def _end_game(self, option):
        self.gw.disable_fields()
        if option == 1:
            self.gw.draw_message("You have won!", "green")
        else:
            self.gw.draw_message("You have lost!", "red")

    def _cheat(self):
        self.gw.cheat(self.board)
