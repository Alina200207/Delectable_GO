import sys
import threading

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPen, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QDialogButtonBox, \
    QVBoxLayout

import IIPlay
from Board import Board


def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """

    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


class MainWindow(QMainWindow):
    my_signal = QtCore.pyqtSignal(name='my_signal')

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
        self.otst = int(self.width_desk * 0.1)
        self.size_sq = (self.width_desk - self.otst * 2) // 8
        self.board = Board()
        self.setUpdatesEnabled(True)
        self.person_mov = None
        self.click_pass = False
        self.count_pass = 0
        self.lock = threading.Lock()
        self.my_signal.connect(self.mySignalHandler, QtCore.Qt.QueuedConnection)

    def mySignalHandler(self):
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        print("fvjhfbc")
        qp.begin(self)
        self.draw_board(qp)
        self.draw_stone(qp)
        qp.end()

    def upd(self):
        self.update()

    def mousePressEvent(self, a0):
        print(round((a0.x() - self.otst) / self.size_sq), round((a0.y() - self.otst) / self.size_sq))
        self.person_mov = (round((a0.x() - self.otst) / self.size_sq),
                           round((a0.y() - self.otst) / self.size_sq))
        self.update()

    def update_board(self, board):
        self.board = board

    def open_dialog(self):
        self.click_pass = True
        dlg = CustomDialog()
        dlg.exec()

    def get_pass(self):
        return self.click_pass

    def draw_board(self, qp):
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(9):
            qp.drawLine(self.otst, self.otst + self.size_sq * i, 9 * self.size_sq, self.otst + self.size_sq * i)
            qp.drawLine(self.otst + self.size_sq * i, self.otst, self.otst + self.size_sq * i, 9 * self.size_sq)

    def draw_stone(self, qp):
        for i in range(1, self.board.size + 1):
            for j in range(1, self.board.size + 1):
                print(i, j)
                if self.check_coord(self.size_sq * (i - 1) + self.otst, self.size_sq * (j - 1) + self.otst):
                    if self.board.board[i][j] == Board.alien:
                        self.draw_white_stone(qp, self.size_sq * (i - 1) + self.otst,
                                              self.size_sq * (j - 1) + self.otst)
                    if self.board.board[i][j] == Board.our:
                        self.draw_black_stone(qp, self.size_sq * (i - 1) + self.otst,
                                              self.size_sq * (j - 1) + self.otst)

            # верхний левый угол коорд - x - 100, y - 20 разница по 80

    def round_cord(self, point):
        return int(round(point // self.size_sq) * self.size_sq)

    def check_coord(self, x, y):
        if x > 9 * self.size_sq:
            return False
        elif y > 9 * self.size_sq:
            return False
        elif x < self.otst:
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


    #@thread
    #def ii_move(self, sygnal):
     #   move = IIPlay.play_random_move(self.board)
     #   self.board = move[0]
    #    if not move[1]:
    #        self.count_pass += 1
    #    else:
     #       self.count_pass = 0
     #   sygnal.emit()

    @thread
    def person_mo(self, sygnal):
        self.setEnabled(True)
        while not self.person_mov:
            continue
        if self.person_mov == "pass":
            self.count_pass += 1
        elif self.board.check(self.person_mov, Board.alien):
            self.board.make_move(self.person_mov, Board.alien)
            self.count_pass = 0
        self.setEnabled(False)
        sygnal.emit()

    def main(self):
        stone_type = Board.our
        self.setEnabled(False)
        while True:
            if stone_type == Board.our:
                with self.lock:
                    move = IIPlay.play_random_move(self.board)
                    self.board = move[0]
                    if not move[1]:
                        self.count_pass += 1
                    else:
                        self.count_pass = 0
                self.update()
            if stone_type == Board.alien:
                with self.lock:
                    self.person_mo(self.my_signal)
            if self.count_pass >= 2:
                self.count_points(self.board)
                break
            stone_type = self.board.get_opposite_stone(stone_type)

    def get_board(self):
        return self.board

    def person_move(self, x, y):
        if self.board.check((x, y), Board.alien):
            self.board.make_move((x, y), Board.alien)
        return self.board

    def count_points(self, board: Board):
        comp_score = 0
        person_score = 0
        for i in range(board.size):
            for j in range(board.size):
                point = (i, j)
                if board.get_point(point) == Board.empty:
                    survivors = board.get_close_neighbours(point)
                    isCompPoint = True
                    isPersonPoint = True
                    for p in survivors:
                        point_type = board.get_point(p)
                        if point_type != Board.our and point_type != Board.border:
                            isCompPoint = False
                            break
                    for p in survivors:
                        point_type = board.get_point(p)
                        if point_type != Board.alien and point_type != Board.border:
                            isPersonPoint = False
                            break
                    if isCompPoint:
                        comp_score += 1
                    if isPersonPoint:
                        person_score += 1
                else:
                    if board.get_point(point) == Board.our:
                        comp_score += 1
                    if board.get_point(point) == Board.alien:
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
