import sys
import threading
import time

import IIPlay

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPen, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QDialogButtonBox, QVBoxLayout, \
    QMessageBox

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
        self.count_pass = 0
        self.button.clicked.connect(self.add_count_pass)
        self.button.setGeometry(int(self.width_desk * 0.4), int(self.height_desk * 0.9), int(self.width_desk * 0.2),
                                int(self.height_desk * 0.05))
        self.indent = int(self.width_desk * 0.1)
        self.size_sq = (self.width_desk - self.indent * 2) // 8
        self.board = Board()
        self.person_point = None
        self.click_pass = False
        self.flag = True
        self.dlg = QMessageBox(self)

    def add_count_pass(self):
        """sums up the number of passes"""
        self.count_pass += 1
        self.click_pass = True

    def paintEvent(self, e):
        """draws a board and stones"""
        qp = QPainter()
        qp.begin(self)
        self.draw_board(qp)
        self.draw_stone(qp)
        qp.end()

    def mousePressEvent(self, a0):
        """reacts to right-click and records coordinates"""
        self.person_point = (round((a0.x() - self.indent) / self.size_sq) + 1,
                             round((a0.y() - self.indent) / self.size_sq) + 1)

    def open_dialog(self):
        """creates a dialog box"""
        point = self.board.count_points()
        self.dlg.setStyleSheet(
                "color: black; font: bold 16px; background-color: white;"
            )
        self.dlg.setWindowTitle("Результат игры")
        self.dlg.setText("Очки игрока: " + str(point[1]) + '\nОчки компьютера: ' + str(point[0]))
        self.dlg.exec()

    def draw_board(self, qp):
        """
        creates a board by drawing lines
        :param qp: instance of QPainter
        """
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(9):
            qp.drawLine(self.indent, self.indent + self.size_sq * i, 9 * self.size_sq, self.indent + self.size_sq * i)
            qp.drawLine(self.indent + self.size_sq * i, self.indent, self.indent + self.size_sq * i, 9 * self.size_sq)

    def draw_stone(self, qp):
        """
        draws a stone at the desired point
        :param qp: instance of QPainter
        """
        for i in range(1, self.board.size + 1):
            for j in range(1, self.board.size + 1):
                self.set_stone(i, j, qp)

    def set_stone(self, i, j, qp):
        """
        checks whether the stone is within the board and determines which stone needs to be drawn
        :param qp: instance of QPainter
        :param i: x coordinates
        :param j: coordinates by y
        """
        if self.check_coord(self.size_sq * (i - 1) + self.indent, self.size_sq * (j - 1) + self.indent):
            if self.board.board[i][j] == Board.alien:
                self.draw_white_stone(qp, self.size_sq * (i - 1) + self.indent,
                                      self.size_sq * (j - 1) + self.indent)
            if self.board.board[i][j] == Board.our:
                self.draw_black_stone(qp, self.size_sq * (i - 1) + self.indent,
                                      self.size_sq * (j - 1) + self.indent)

    def round_cord(self, point) -> int:
        """
        rounds the coordinates received from the mouse click so that the stone is at the intersection of the lines'
        :param point: x or y coordinates of the player's click
        :return: rounded coordinates
        """
        return int(round(point // self.size_sq) * self.size_sq)

    def check_coord(self, x, y) -> bool:
        """
        checks that the stone does not go beyond the board
        :param x: coordinates by x
        :param y: coordinates by y
        :return: true or false depending on the ability to put a stone
        """
        if x > 9 * self.size_sq:
            return False
        elif y > 9 * self.size_sq:
            return False
        elif x < self.indent:
            return False
        return True

    def draw_white_stone(self, qp, x, y):
        """
        a white stone is created
        :param qp: instance of QPainter
        :param x: coordinates by x
        :param y: coordinates by y
        """

        stone = QBrush(Qt.white, Qt.SolidPattern)
        qp.setBrush(stone)
        qp.drawEllipse(x - int(self.size_sq * 0.25), y - int(self.size_sq * 0.25), int(self.size_sq * 0.5),
                       int(self.size_sq * 0.5))

    def draw_black_stone(self, qp, x, y):
        """
        a black stone is being created
        :param qp: instance of QPainter
        :param x: coordinates by x
        :param y: coordinates by y
        """
        stone = QBrush(Qt.black, Qt.SolidPattern)
        qp.setBrush(stone)
        qp.drawEllipse(x - int(self.size_sq * 0.25), y - int(self.size_sq * 0.25), int(self.size_sq * 0.5),
                       int(self.size_sq * 0.5))

    def main(self):
        """starts a stream with the game"""
        t = threading.Thread(target=self.game)
        t.start()

    def game(self):
        """The main method of the game"""
        stone_type = Board.our
        self.setEnabled(False)
        while True:
            if stone_type == Board.our:
                if self.flag:
                    self.do_comp_move()
                else:
                    continue
                stone_type = self.board.get_opposite_stone(stone_type)
            if stone_type == Board.alien:
                self.do_person_move()
                stone_type = self.board.get_opposite_stone(stone_type)
            if self.count_pass >= 2:
                self.open_dialog()
                break
            self.update()

    def do_comp_move(self):
        """creates the computer's progress"""
        move = IIPlay.make_comp_move(self.board)
        self.board = move[0]
        if not move[1]:
            self.count_pass += 1
        else:
            self.count_pass = 0
            self.click_pass = False
        self.update()
        self.flag = False

    def do_person_move(self):
        """processes the player 's move"""
        self.setEnabled(True)
        while not self.person_point and not self.click_pass:
            continue
        if not self.click_pass:
            if self.board.check_move_correctness(self.person_point, Board.alien):
                self.board.make_move(self.person_point, Board.alien)
                self.count_pass = 0
                self.click_pass = False
            else:
                self.person_point = None
                self.do_person_move()
        self.person_point = None
        self.setEnabled(False)
        self.update()
        self.flag = True
        time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.main()
    sys.exit(app.exec_())
