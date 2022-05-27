import sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QLineEdit, QMainWindow, QWidget

import selection_window


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Го")
        self.setStyleSheet("background-color: #F0C98D;")
        self.lbl = QLabel(self)
        self.qle = QLineEdit(self)
        self.button_enter = QPushButton("Ввести", self)
        self.button_enter.setStyleSheet("background-color: #FFE7AB;")
        self.desktop = QApplication.desktop()
        self.height_desk = int(self.desktop.height() * 0.8)
        self.width_desk = int(self.height_desk * 0.9)
        self.lbl.move(int(
            self.width_desk*0.1),
            int(self.height_desk*0.3)
        )
        self.lbl.setText("Добро пожаловать в игру \"Го\"\nВведи свое имя:")
        self.qle.setGeometry(int(
            self.width_desk*0.1),
            int(self.height_desk*0.5),
            int(self.width_desk*0.8),
            int(self.height_desk*0.05)
        )

        self.lbl.setStyleSheet("color: #8E4014;")
        self.lbl.setFont(QFont(
            "Times",
            int(self.width_desk*0.03),
            QFont.Bold)
        )
        self.button_enter.setFont(QFont(
            "Times",
            int(self.width_desk * 0.015)
        ))
        self.lbl.setAlignment(Qt.AlignVCenter)
        self.qle.setStyleSheet("background-color: white;")
        self.qle.setFont(QFont(
            "Times",
            int(self.width_desk * 0.015),
            QFont.Bold
        ))
        self.lbl.adjustSize()
        self.setFixedSize(QSize(
            self.width_desk,
            self.height_desk
        ))
        self.button_enter.clicked.connect(self.get_text)
        self.button_enter.setGeometry(
            int(self.width_desk * 0.3),
            int(self.height_desk * 0.6),
            int(self.width_desk * 0.4),
            int(self.height_desk * 0.05)
        )

    def get_text(self):
        """
        retrieves the entered text
        """
        name_player = self.qle.text()
        window_board = selection_window.SelectionWindow(
            name_player,
            self
        )
        window_board.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
