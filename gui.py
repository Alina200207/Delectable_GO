import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPen, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QDialogButtonBox, \
    QVBoxLayout

from Game import Game
from Point import Point


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Го")
        self.setStyleSheet("background-color: #F0C98D;")
        self.button = QPushButton("Pass!", self)
        self.button.setStyleSheet("background-color: #FFE7AB;")
        self.button.move(800, 700)
        self.button.clicked.connect(self.open_dialog)
        self.button.setGeometry(350, 700, 200, 50)
        self.setFixedSize(QSize(900, 800))
        self.coord = []
        self.x = -1
        self.y = -1
        self.click_pass = False
        self.game = Game

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        draw_board(qp)
        draw_stone(qp, self.coord)
        qp.end()

    def mousePressEvent(self, a0):
        self.x = round_cord(a0.x())
        self.y = round_cord(a0.y())
        self.update()

    def get_board(self, board):
        self.coord = self.game.get_board()

    def open_dialog(self):
        self.click_pass = True
        dlg = CustomDialog()
        dlg.exec()

    def get_person_move(self):
        return Point(self.x, self.y)

    def get_pass(self):
        return self.click_pass

def draw_stone(qp, coord):
    for i in coord:
        if True:
            if check_coord(i[0], i[1]):
                draw_white_stone(qp, i[0], i[1])  # верхний левый угол коорд - x - 100, y - 20 разница по 80
    # qt.drawEllipse(175+80*2, 95+80*2, 50, 50)


def draw_white_stone(qp, x, y):
    stone = QBrush(Qt.white, Qt.SolidPattern)
    qp.setBrush(stone)
    qp.drawEllipse(x, y, 50, 50)


def draw_black_stone(qp, x, y):
    stone = QBrush(Qt.black, Qt.SolidPattern)
    qp.setBrush(stone)
    qp.drawEllipse(x, y, 50, 50)



def draw_board(qp):
    pen = QPen(Qt.black, 3, Qt.SolidLine)
    qp.setPen(pen)
    dis = 80
    for i in range(9):
        qp.drawLine(120, 40 + dis * i, 760, 40 + dis * i)
        qp.drawLine(120 + dis * i, 40, 120 + dis * i, 680)


def round_cord(point):
    return round(point // 80) * 80 + 15


def check_coord(x, y):
    if x > 760:
        return False
    elif y > 680:
        return False
    elif x < 95:
        return False
    return True


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
    sys.exit(app.exec_())