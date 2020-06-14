"""Zawiera klasę Minesweeper zajmująca się przetworzeniem akcji użytkownika."""


from exceptions import BoardParametersError


class Minesweeper(object):
    """Zajmuje się przetworzeniem akcji użytkownika."""

    def __init__(self, board, game_window):
        self.board = board
        self.game_window = game_window

    def init_game(self):
        """Inicjalizuje grę."""
        self.game_window.init_window()
        self.game_window.btn_start_game.bind("<Button-1>", lambda event: self._start_game())

    def _bind_events(self):
        """Przypisuje odpowiednie zdarzenia elementom."""
        for i, row in enumerate(self.game_window.fields):
            for j, field in enumerate(row):
                field.config(command=lambda x=i, y=j: self._left_click(x, y))
                field.bind("<Button-3>", lambda event, x=i, y=j: self._right_click(x, y))

        self.game_window.master.bind("xyzzy", lambda event: self._cheat())

    def _start_game(self):
        """Rozpoczyna nową rozgrywkę.

        Obsługuje ewentualne błędy wywołane podaniem przez
        użytkownika nieprawidłowych parametrów planszy.
        """
        try:
            rows = int(self.game_window.ent_rows.get())
            columns = int(self.game_window.ent_columns.get())
            mines = int(self.game_window.ent_mines.get())
        except ValueError:
            self.game_window.draw_message("Incorrect board parameters", color="red")
            return

        try:
            self.board.create_board(rows, columns, mines)
        except BoardParametersError:
            self.game_window.draw_message("Incorrect board parameters", color="red")
            return
        else:
            self.game_window.destroy_fields()
            self.game_window.draw_board(self.board)
            self._bind_events()
            self.game_window.draw_message("")
            self.game_window.draw_mines_number(self.board)
            self.game_window.draw_flag_counter(self.board)

    def _left_click(self, row, col):
        """Funkcja wywoływana po naciśnięciu pola lewym przyciskiem myszy.

        Funkcja zostaje wywołana, gdy użytkownik spróbuje odkryć pole.
        """
        val = self.board.clear_field(row, col)
        if val == 1:
            self.game_window.draw_mines(self.board, row, col)
            self._end_game(option=0)
            return
        elif val == 0:
            self.game_window.update_fields(self.board)
        self._game_state()

    def _right_click(self, row, col):
        """Funkcja wywoływana po naciśnięciu pola prawym przyciskiem myszy.

        Funkcja zostaje wywołana, gdy użytkownik spróbuje oflagować pole.
        """
        val = self.board.flag_field(row, col)
        if val == -1:
            return
        self.game_window.draw_flag(row, col, option=val)
        self.game_window.draw_flag_counter(self.board)
        self._game_state()

    def _game_state(self):
        """Sprawdza stan gry i podejmuje odpowiednią akcję."""
        state = self.board.check_state()
        if state == 1:
            self._end_game(option=1)

    def _end_game(self, option):
        """Kończy rozgrywkę.

        Wywołuje funkcję dezaktywującą wszytskie pola
        oraz wywołuje funkcję wyświetlajacą komunikat
        o wyniku rozgrywki. Komunikat zależy od wartości
        argumentu 'option'.
        """
        self.game_window.disable_fields()
        if option == 1:
            self.game_window.draw_message("You have won!", "green")
        else:
            self.game_window.draw_message("You have lost!", "red")

    def _cheat(self):
        """Funkcja wywoływana po wpisaniu kodu 'xyzzy'."""
        self.game_window.cheat(self.board)
