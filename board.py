"""Moduł zawierający klasy związane z logiką gry."""

import random

from exceptions import BoardParametersError


# Maksymalne i minimalne parametry planszy
ROWS_MAX = 15
COLUMNS_MAX = 15
ROWS_MIN = 2
COLUMNS_MIN = 2
MINES_MIN = 0


class Field(object):
    """Reprezentuje pojedyczne pole."""

    def __init__(self):
        self.revealed = False
        self.mine = False
        self.value = 0  # Liczba bomb w poblizu pola
        self.flag = False
        self.qmark = False


class Board(object):
    """Odpowiada za logikę gry."""

    def __init__(self):
        self.fields = []
        self.modified_fields = []
        self.mines_cords = []
        self.rows = 0
        self.cols = 0
        self.mines = 0
        self._flagged_mines = 0
        self.flagged_fields = 0
        self._unrevealed_fields = 0

    def create_board(self, rows, cols, mines):
        """Tworzy nową plansze.

        Sprawdza, czy podane wartości min i wymiarów planszy są prawidłowe.
        Jeśli nie, to rzuca wyjątek 'BoardParametersError'. Jeśli tak, to
        tworzy odpowiednią planszę.
        """
        if rows < ROWS_MIN or rows > ROWS_MAX:
            raise BoardParametersError

        if cols < COLUMNS_MIN or cols > COLUMNS_MAX:
            raise BoardParametersError

        if mines < MINES_MIN or mines > rows*cols:
            raise BoardParametersError

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.fields = [[Field() for _ in range(self.cols)]
                       for _ in range(self.rows)]
        self._unrevealed_fields = self.rows * self.cols - self.mines
        self._flagged_mines = 0
        self.flagged_fields = 0
        self.mines_cords = []
        self._generate_mines()

    def clear_field(self, row, col):
        """Odkyrwa pojedyncze pole.

        W zależności od stanu pola zwraca
        odpowiednią wartość.
        """

        if self.fields[row][col].flag:
            return 2

        if self.fields[row][col].revealed:
            return 2

        if self.fields[row][col].mine:
            self.fields[row][col].revealed = True
            return 1
        else:
            self.fields[row][col].revealed = True
            self._unrevealed_fields -= 1
            self.modified_fields = [(row, col)]
            if self.fields[row][col].value == 0:
                self._reveal(row, col)
            return 0

    def _reveal(self, row, col):
        """Odkrywa sąsiadów pola o indeksach podabnych jako argumenty."""
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
        """Oflagowuje pole.

        W zależności od stanu pola, pole zostaje oflagowane,
        oznaczone znakiem '?' lub przywrócone do pierwotnego
        stanu.
        """
        if self.fields[row][col].revealed:
            return -1

        if self.flagged_fields == self.mines:
            return -1

        if self.fields[row][col].flag:
            self.fields[row][col].flag = False
            self.fields[row][col].qmark = True
            self.flagged_fields -= 1
            if self.fields[row][col].mine:
                self._flagged_mines -= 1
            return 1

        if self.fields[row][col].qmark:
            self.fields[row][col].qmark = False
            return 2

        if self.fields[row][col].mine:
            self._flagged_mines += 1

        self.fields[row][col].flag = True
        self.flagged_fields += 1

        return 0

    def check_state(self):
        """Sprawdza stan gry.

        Sprawdza, czy zostały odkryte wszytskie pole
        lub czy zostały oflagowane wszystkie miny.
        """
        if self._unrevealed_fields == 0:
            return 1
        if self._flagged_mines == self.mines:
            return 1
        return 0

    def is_revealed(self, row, col):
        """Zwraca wartość pola, którego indeksy podane są jako argumenty."""
        return self.fields[row][col].revealed

    def get_value(self, row, col):
        """Zwraca wartość pola, którego indeksy podane są jako argumenty."""
        return self.fields[row][col].value

    def _generate_mines(self):
        """Losuje miny na planszy."""
        mines_left = self.mines
        while mines_left > 0:
            gen_row = random.randint(0, self.rows-1)
            gen_col = random.randint(0, self.cols-1)
            if not self.fields[gen_row][gen_col].mine:
                self.fields[gen_row][gen_col].mine = True
                self._increment_fields_values(gen_row, gen_col)
                self.mines_cords.append((gen_row, gen_col))
                mines_left -= 1

    def _increment_fields_values(self, row, col):
        """Inkrementacja wartosci pol sasiednich.

        Funkcja jest wywoływana, kiedy na danym polu
        ustawiona zostaje mina. Zwieksza ona wtedy
        wartości pól sąsiednich tego pola o jeden.
        """
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i < 0 or j < 0:
                    continue
                try:
                    self.fields[i][j].value += 1
                except IndexError:
                    continue
