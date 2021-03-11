# boginjasholsta

import sys
from PyQt5.QtWidgets import QApplication, \
    QWidget, QPushButton, \
    QLabel, QRadioButton


class Cell(QPushButton):
    def __init__(self, father, x, y):
        self.coordinates = x, y
        super().__init__(father)

    def get_row(self):
        return self.coordinates[0]

    def get_column(self):
        return self.coordinates[1]


class Example(QWidget):
    def __init__(self):

        # margins
        self.margin_top = 25
        self.margin_left = 70

        # cells
        self.cells = [[], [], []]

        # the current turn
        self.turn = 'X'

        # the first sign placed
        self.first_sign_placed = False

        # game ended
        self.game_ended = False

        # used cells number
        self.used_cells = 0

        # number X and O in rows, columns, diagonals
        # first for X, second for O
        self.number_signs = {
            'rows': [[0, 0] for _ in range(3)],
            'columns': [[0, 0] for _ in range(3)],
            'main_diagonal': [0, 0],
            'side_diagonal': [0, 0]
        }

        # init
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # window settings
        self.setGeometry(1000, 200, 350, 400)
        self.setWindowTitle('Крестики-нолики')

        # radio x
        self.button_x = QRadioButton('X', self)
        self.button_x.move(self.margin_left + 70, self.margin_top)
        self.button_x.click()
        self.button_x.clicked.connect(self.first_player)

        # radio y
        self.button_y = QRadioButton('O', self)
        self.button_y.move(self.margin_left + 115, self.margin_top)
        self.button_y.clicked.connect(self.first_player)

        self.margin_top += 50

        # buttons
        self.tec_row = 0
        for i in range(9):
            self.cells[self.tec_row].append(Cell(self, self.tec_row, i % 3))
            self.cells[self.tec_row][-1].move(self.margin_left, self.margin_top)
            self.cells[self.tec_row][-1].resize(70, 70)
            self.cells[self.tec_row][-1].clicked.connect(self.cell_clicked)

            self.margin_left += 70
            if i % 3 == 2:
                self.tec_row += 1
                self.margin_left = 70
                self.margin_top += 70

        self.margin_top += 10

        # winner label
        self.winner_label = QLabel(self)
        self.winner_label.move(self.margin_left + 35, self.margin_top)

        self.margin_top += 20

        # button "new game"
        self.new_game_button = QPushButton("Новая игра", self)
        self.new_game_button.move(self.margin_left + 58, self.margin_top)
        self.new_game_button.clicked.connect(self.new_game)

    def first_player(self):
        if not self.first_sign_placed:
            self.turn = self.sender().text()
        else:
            if self.game_ended:
                self.turn = self.sender().text()
                self.new_game()
            else:
                pass

    def cell_clicked(self):
        if not self.first_sign_placed:
            self.first_sign_placed = True

        # if cell isn`t used
        if self.sender().text() == "":
            # update used cells
            self.used_cells += 1

            self.sender().setText(self.turn)
            if self.turn == 'X':
                self.turn = 'O'
                self.index = 0
            else:
                self.turn = 'X'
                self.index = 1

            # updating number of signs
            self.winner = ''

            # update rows information
            self.number_signs['rows'][
                self.sender().get_row()][self.index] += 1

            if self.number_signs['rows'][self.sender().get_row()][self.index] \
                    == 3:
                if self.index == 0:
                    self.winner = 'X'
                else:
                    self.winner = 'O'

            # update columns information
            self.number_signs['columns'][
                self.sender().get_column()][self.index] += 1

            if self.number_signs['columns'][self.sender().get_column()][self.index] \
                    == 3:
                if self.index == 0:
                    self.winner = 'X'
                else:
                    self.winner = 'O'

            # update main diagonal information
            if self.sender().get_row() == self.sender().get_column():
                self.number_signs['main_diagonal'][self.index] += 1

            if self.number_signs['main_diagonal'][self.index] == 3:
                if self.index == 0:
                    self.winner = 'X'
                else:
                    self.winner = 'O'

            if (self.sender().get_row(), self.sender().get_column()) in \
                    [(0, 2), (1, 1), (2, 0)]:
                self.number_signs['side_diagonal'][self.index] += 1

            if self.number_signs['side_diagonal'][self.index] == 3:
                if self.index == 0:
                    self.winner = 'X'
                else:
                    self.winner = 'O'

            if self.winner == '' and self.used_cells == 9:
                self.winner = 'Nobody'

            if self.winner != '':
                self.game_ended = True
                self.end_game(self.winner)

    def end_game(self, name_winner):
        if name_winner != 'Nobody':
            self.winner_label.setText(f'Выиграл {name_winner}!')
        else:
            self.winner_label.setText('Ничья!')

        self.winner_label.resize(self.winner_label.sizeHint())

        for i in range(3):
            for j in range(3):
                self.cells[i][j].setEnabled(False)

    def new_game(self):
        self.winner_label.setText("")
        for i in range(3):
            for j in range(3):
                self.cells[i][j].setEnabled(True)
                self.cells[i][j].setText("")

        self.game_ended = False
        self.first_sign_placed = False

        self.number_signs['rows'] = [[0, 0] for _ in range(3)]
        self.number_signs['columns'] = [[0, 0] for _ in range(3)]
        self.number_signs['main_diagonal'] = [0, 0]
        self.number_signs['side_diagonal'] = [0, 0]

        self.used_cells = 0


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
