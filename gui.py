import sys
import threading
import IIPlay

from multiprocessing.connection import wait
from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPen, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QDialogButtonBox, \
    QVBoxLayout

from Board import Board


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Го")
        self.setStyleSheet("background-color: #F0C98D;")
        self.button = QPushButton("Pass!", self)
        self.button.setStyleSheet("background-color: #FFE7AB;")
        self.desktop = QApplication.desktop()
        self.height_desk = int(self.desktop.height() * 0.8)
        self.width_desk = int(self.height_desk * 0.9)

        self.setFixedSize(QSize(self.width_desk, self.height_desk))
        self.button.clicked.connect(self.open_dialog)
        self.button.setGeometry(int(self.width_desk * 0.4), int(self.height_desk * 0.9), int(self.width_desk * 0.2),
                                int(self.height_desk * 0.05))
        self.indent = int(self.width_desk * 0.1)
        self.size_sq = (self.width_desk - self.indent * 2) // 8
        self.board = Board()
        self.person_point = None
        self.click_pass = False
        self.count_pass = 0
        self.flag = True

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_board(qp)
        self.draw_stone(qp)
        qp.end()

    def mousePressEvent(self, a0):
        self.person_point = (round((a0.x() - self.indent) / self.size_sq) + 1,
                             round((a0.y() - self.indent) / self.size_sq) + 1)

    def open_dialog(self):
        self.click_pass = True
        dlg = CustomDialog()
        dlg.exec()

    def get_pass(self) -> bool:
        return self.click_pass

    def draw_board(self, qp):
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(9):
            qp.drawLine(self.indent, self.indent + self.size_sq * i, 9 * self.size_sq, self.indent + self.size_sq * i)
            qp.drawLine(self.indent + self.size_sq * i, self.indent, self.indent + self.size_sq * i, 9 * self.size_sq)

    def draw_stone(self, qp):
        for i in range(1, self.board.size + 1):
            for j in range(1, self.board.size + 1):
                if self.check_coord(self.size_sq * (i - 1) + self.indent, self.size_sq * (j - 1) + self.indent):
                    if self.board.board[i][j] == Board.alien:
                        self.draw_white_stone(qp, self.size_sq * (i - 1) + self.indent,
                                              self.size_sq * (j - 1) + self.indent)
                    if self.board.board[i][j] == Board.our:
                        self.draw_black_stone(qp, self.size_sq * (i - 1) + self.indent,
                                              self.size_sq * (j - 1) + self.indent)

            # верхний левый угол коорд - x - 100, y - 20 разница по 80

    def round_cord(self, point) -> int:
        return int(round(point // self.size_sq) * self.size_sq)

    def check_coord(self, x, y) -> bool:
        if x > 9 * self.size_sq:
            return False
        elif y > 9 * self.size_sq:
            return False
        elif x < self.indent:
            return False
        return True

    def draw_white_stone(self, qp, x, y):
        stone = QBrush(Qt.white, Qt.SolidPattern)
        qp.setBrush(stone)
        qp.drawEllipse(x - int(self.size_sq * 0.25), y - int(self.size_sq * 0.25), int(self.size_sq * 0.5),
                       int(self.size_sq * 0.5))

    def draw_black_stone(self, qp, x, y):
        stone = QBrush(Qt.black, Qt.SolidPattern)
        qp.setBrush(stone)
        qp.drawEllipse(x - int(self.size_sq * 0.25), y - int(self.size_sq * 0.25), int(self.size_sq * 0.5),
                       int(self.size_sq * 0.5))

    def do_person_move(self):
        self.setEnabled(True)
        while not self.person_point:
            continue
        if self.person_point == "pass":
            self.count_pass += 1
        elif self.board.check(self.person_point, Board.alien):
            self.board.make_move(self.person_point, Board.alien)
            self.count_pass = 0
        else:
            self.person_point = None
            self.do_person_move()
        self.person_point = None
        self.setEnabled(False)

    def main(self):
        t = threading.Thread(target=self.game)
        t.start()

    def game(self):
        stone_type = Board.our
        self.setEnabled(False)
        while True:
            if stone_type == Board.our:
                if self.flag:
                    move = IIPlay.play_random_move(self.board)
                    self.board = move[0]
                    print(move[1])
                    for row in self.board.board:
                        print(row)
                    if not move[1]:
                        self.count_pass += 1
                    else:
                        self.count_pass = 0
                    self.update()
                    self.flag = False
                else:
                    continue
            if stone_type == Board.alien:
                if self.click_pass:
                    self.count_pass += 1
                else:
                    self.click_pass = False
                    self.do_person_move()
                self.update()
                self.flag = True
            if self.count_pass >= 2:
                self.count_points()
                break
            stone_type = self.board.get_opposite_stone(stone_type)

    def count_points(self) -> list[int]:
        comp_score = 0
        person_score = 0
        for i in range(self.board.size):
            for j in range(self.board.size):
                point = (i, j)
                if self.board.get_point_type(point) == Board.empty:
                    survivors = self.board.get_close_neighbors(point)
                    isCompPoint = True
                    isPersonPoint = True
                    for p in survivors:
                        point_type = self.board.get_point_type(p)
                        if point_type != Board.our and point_type != Board.border:
                            isCompPoint = False
                            break
                    for p in survivors:
                        point_type = self.board.get_point_type(p)
                        if point_type != Board.alien and point_type != Board.border:
                            isPersonPoint = False
                            break
                    if isCompPoint:
                        comp_score += 1
                    if isPersonPoint:
                        person_score += 1
                else:
                    if self.board.get_point_type(point) == Board.our:
                        comp_score += 1
                    if self.board.get_point_type(point) == Board.alien:
                        person_score += 1
        return [comp_score, person_score]


# qt.drawEllipse(175+80*2, 95+80*2, 50, 50)


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 100)
        self.setWindowTitle("Результат")
        QBtn = QDialogButtonBox.Close
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel("Счет: 0")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.main()
    sys.exit(app.exec_())
