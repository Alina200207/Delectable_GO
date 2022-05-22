import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit, QMainWindow, QWidget

import gui


def set_board_size_19():
    window_board = gui.MainWindow(19)
    window_board.show()
    window_board.main()


def set_board_size_9():
    window_board = gui.MainWindow(9)
    window_board.show()
    window_board.main()


class SelectionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("Го")
        self.setStyleSheet("background-color: #F0C98D;")
        self.lbl = QLabel(self)
        self.button1 = QPushButton("9*9", self)
        self.button2 = QPushButton("19*19", self)
        self.button1.setStyleSheet("background-color: #FFE7AB; font-size: 20px;")
        self.button2.setStyleSheet("background-color: #FFE7AB; font-size: 20px;")
        self.desktop = QApplication.desktop()
        self.height_desk = int(self.desktop.height() * 0.8)
        self.width_desk = int(self.height_desk * 0.9)
        self.lbl.move(int(self.width_desk * 0.2), int(self.height_desk * 0.2))
        self.lbl.setText("Выберите размер доски")
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setStyleSheet("color: #8E4014; font-size: 40px;")
        self.lbl.adjustSize()
        self.setFixedSize(QSize(self.width_desk, self.height_desk))
        self.button1.clicked.connect(set_board_size_9)
        self.button2.clicked.connect(set_board_size_19)
        self.button1.setGeometry(int(self.width_desk * 0.1), int(self.height_desk * 0.4),
                                 int(self.width_desk * 0.35),
                                 int(self.height_desk * 0.35))
        self.button2.setGeometry(int(self.width_desk * 0.55), int(self.height_desk * 0.4),
                                 int(self.width_desk * 0.35),
                                 int(self.height_desk * 0.35))
