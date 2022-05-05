import os
import re
import sqlite3
import sys
import threading
import time

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPen, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QDialog

import IIPlay
from Board import Board
from Point import OrdinaryPoint

board_in_string_pattern = re.compile(r'board state: (.*)')
column_pattern = re.compile(r'\[(.*?)\]')


def rewrite_file(last_condition: str):
    """
    Rewrites the file with relevant board's states.
    :param last_condition: the last condition of the board that should be deleted from file.
    """
    with open('log_board.txt', 'r') as main_file:
        with open('auxiliary_file.txt', 'w') as auxiliary:
            for line in main_file:
                if line != last_condition:
                    auxiliary.write(line)
    os.remove('log_board.txt')
    os.replace('auxiliary_file.txt', 'log_board.txt')


class MainWindow(QMainWindow):
    def __init__(self, size_board, name):
        super().__init__()
        self.board_size = size_board
        self.setWindowTitle("Го")
        self.setStyleSheet("background-color: #F0C98D;")
        self.button_pass = QPushButton("Pass!", self)
        self.button_pass.setStyleSheet("background-color: #FFE7AB;")
        self.button_previous_move = QPushButton("Undo move!", self)
        self.button_previous_move.setStyleSheet("background-color: #FFE7AB;")
        self.desktop = QApplication.desktop()
        self.height_desk = int(self.desktop.height() * 0.8)
        self.width_desk = int(self.height_desk * 0.9)

        self.setFixedSize(QSize(self.width_desk, self.height_desk))
        self.count_pass = 0
        self.button_pass.clicked.connect(self.add_count_pass)
        self.button_previous_move.clicked.connect(self.set_previous_move)
        self.button_pass.setGeometry(int(self.width_desk * 0.6), int(self.height_desk * 0.9),
                                     int(self.width_desk * 0.2),
                                     int(self.height_desk * 0.05))
        self.button_previous_move.setGeometry(int(self.width_desk * 0.2), int(self.height_desk * 0.9),
                                              int(self.width_desk * 0.2),
                                              int(self.height_desk * 0.05))
        self.indent = int(self.width_desk * 0.1)
        self.size_sq = (self.width_desk - self.indent * 2) // (self.board_size - 1)
        self.board = Board(self.board_size )
        self.person_point = None
        self.click_pass = False
        self.flag = True
        self.player_name = name
        self.dlg = QMessageBox(self)

    def add_count_pass(self):
        """sums up the number of passes"""
        self.count_pass += 1
        self.click_pass = True

    def set_previous_move(self):
        """
        Undo last move on the board.
        """
        new_board = self.board.board
        with open('log_board.txt', 'r') as file:
            data = file.readline()
            line_length = len(data) + 1
            position_of_current = 0
            position_of_previous = position_of_current
            while data:
                if re.match(board_in_string_pattern, data):
                    position_of_previous = position_of_current
                    position_of_current = file.tell() - line_length
                data = file.readline()
            file.seek(position_of_previous, 0)
            board_from_file = file.readline()
            match = re.match(board_in_string_pattern, board_from_file)
            if match:
                string_board = match.group(1).split(';')
                new_board = self.process_new_board(string_board)
            file.seek(position_of_current, 0)
            last_condition = file.readline()
        rewrite_file(last_condition)
        self.board.board = new_board
        self.repaint()

    def process_new_board(self, string_board: list[str]) -> list[list[int]]:
        """
        :param string_board: the board in a string state
        :return: relevant board state
        """
        new_board = []
        for i in range(self.board.size + 2):
            column_of_board = re.match(column_pattern, string_board[i])
            if column_of_board:
                new_board.append([int(element) for element in column_of_board.group(1).split(', ')])
        return new_board

    def paintEvent(self, e):
        """draws a board and stones"""
        qp = QPainter()
        qp.begin(self)
        self.draw_board(qp)
        self.draw_stone(qp)
        qp.end()

    def mousePressEvent(self, a0):
        """reacts to right-click and records coordinates"""
        self.person_point = OrdinaryPoint(round((a0.x() - self.indent) / self.size_sq) + 1,
                                          round((a0.y() - self.indent) / self.size_sq) + 1)

    def window_with_game_result(self):
        """creates a dialog box"""
        comp_score, person_score = self.board.count_points()
        self.work_with_database(comp_score, person_score)
        self.dlg.setStyleSheet(
            "color: black; font: bold 16px; background-color: white;"
        )
        self.dlg.setWindowTitle("Результат игры")
        self.dlg.setText("Очки игрока: " + str(person_score) + '\nОчки компьютера: ' + str(comp_score))
        self.dlg.exec()

    def pass_comp(self):
        """
        displays a message that the computer has passed
        """
        dlg = QDialog(self)
        dlg.setWindowTitle("Пасс компьютера")
        dlg.setGeometry(int(self.height_desk * 0.95), int(self.width_desk * 0.6),
                        int(self.width_desk * 0.4),
                        int(self.height_desk * 0.05))

        dlg.exec()

    def work_with_database(self, comp_score, person_score):
        base = sqlite3.connect('info_about_players.db')
        cur = base.cursor()
        base.execute('CREATE TABLE IF NOT EXISTS players(player_name PRIMARY KEY, game_count, win_game_count, '
                     'general_points_count)')
        base.commit()
        info = cur.execute('SELECT * FROM players WHERE player_name=?', (self.player_name,))
        win = 1 if comp_score < person_score else 0
        if not info.fetchone():
            cur.execute('INSERT INTO players VALUES(?, ?, ?, ?)', (self.player_name, 1, win, person_score,))
        else:

            cur.execute('UPDATE players SET game_count=game_count + ?, win_game_count=win_game_count + ?, '
                        'general_points_count=general_points_count + ? WHERE player_name=?',
                        (1, win, person_score, self.player_name,))
        base.commit()
        base.close()

    def draw_board(self, qp):
        """
        creates a board by drawing lines
        :param qp: instance of QPainter
        """
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(self.board_size):
            qp.drawLine(self.indent, self.indent + self.size_sq * i, self.indent + (self.board_size - 1) * self.size_sq,
                        self.indent + self.size_sq * i)
            qp.drawLine(self.indent + self.size_sq * i, self.indent, self.indent + self.size_sq * i,
                        self.indent + (self.board_size - 1) * self.size_sq)

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
        if x > self.indent + (self.board_size - 1) * self.size_sq:
            return False
        elif y > self.indent + (self.board_size - 1) * self.size_sq:
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
                    string_board = ''
                    with open('log_board.txt', 'a') as file:
                        file.write('board state: ')
                        for row in self.board.board:
                            string_board = string_board + str(row) + ';'
                        file.write(string_board + '\n')
                else:
                    continue
                stone_type = self.board.get_opposite_stone(stone_type)
            if stone_type == Board.alien:
                self.do_person_move()
                stone_type = self.board.get_opposite_stone(stone_type)
            if self.count_pass >= 2:
                self.window_with_game_result()
                self.setDisabled(True)
                os.remove('log_board.txt')
                break
            self.repaint()

    def do_comp_move(self):
        """creates the computer's progress"""
        self.setUpdatesEnabled(False)
        move = IIPlay.make_comp_move(self.board)
        self.setUpdatesEnabled(True)
        self.board = move[0]
        if not move[1]:
            self.count_pass += 1
            self.pass_comp()
        else:
            self.count_pass = 0
            self.click_pass = False
        self.flag = False

    def do_person_move(self):
        """processes the player 's move"""
        self.setEnabled(True)
        while not self.person_point and not self.click_pass:
            if self.board.count_stones_on_board() == 1:
                self.button_previous_move.setEnabled(False)
            else:
                self.button_previous_move.setEnabled(True)
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
        self.flag = True
        time.sleep(0.5)

    def closeEvent(self):
        """
        closes the window
        """
        sys.exit(0)


