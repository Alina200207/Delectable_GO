import sys
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
        self.otst = int(self.width_desk * 0.1)
        self.size_sq = (self.width_desk - self.otst * 2) // 8
        self.coord = Board()
        self.setUpdatesEnabled(True)
        self.person_move = None
        self.click_pass = False

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
        self.person_move = (round((a0.x() - self.otst) / self.size_sq),
                            round((a0.y() - self.otst) / self.size_sq))
        self.update()

    def update_board(self, board):
        self.coord = board

    def open_dialog(self):
        self.click_pass = True
        dlg = CustomDialog()
        dlg.exec()

    def get_pass(self):
        return self.click_pass

    def draw_board(self, qp):
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        print("bjkrj")
        for i in range(9):
            qp.drawLine(self.otst, self.otst + self.size_sq * i, 9 * self.size_sq, self.otst + self.size_sq * i)
            qp.drawLine(self.otst + self.size_sq * i, self.otst, self.otst + self.size_sq * i, 9 * self.size_sq)

    def draw_stone(self, qp):
        for i in range(1, self.coord.size + 1):
            for j in range(1, self.coord.size + 1):
                print(i, j)
                if self.check_coord(self.size_sq * (i - 1) + self.otst, self.size_sq * (j - 1) + self.otst):
                    if self.coord.board[i][j] == Board.alien:
                        self.draw_white_stone(qp, self.size_sq * (i - 1) + self.otst, self.size_sq * (j - 1) + self.otst)
                    if self.coord.board[i][j] == Board.our:
                        self.draw_black_stone(qp, self.size_sq * (i - 1) + self.otst, self.size_sq * (j - 1) + self.otst)

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

