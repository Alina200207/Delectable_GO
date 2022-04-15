import sys
import time

from PyQt5.QtWidgets import QApplication

import IIPlay
from Board import Board
from gui import MainWindow


class Game:
    def __init__(self):
        self.board = Board()
        self.count_pass = 0
        self.gui = MainWindow()
        self.gui.show()
        self.gui.update_board(self.board)

    def main(self):
        print("ndnkd")
        stone_type = Board.our
        self.gui.setEnabled(False)
        while True:
            if stone_type == Board.our:
                move = IIPlay.play_random_move(self.board)
                self.board = move[0]
                if not move[1]:
                    self.count_pass += 1
                else:
                    self.count_pass = 0
                self.gui.update_board(self.board)
                self.gui.upd()
                time.sleep(5)
            if stone_type == Board.alien:
                self.gui.setEnabled(True)
                #person_move = self.gui.person_move
                person_move = self.gui.person_move
                if person_move == "pass":
                    self.count_pass += 1
                elif self.board.check(person_move, stone_type):
                    self.board.make_move(person_move, stone_type)
                    self.count_pass = 0
                self.gui.update_board(self.board)
                self.gui.upd()
                self.gui.setEnabled(False)
            if self.count_pass >= 2:
                self.count_points(self.board)
                break
            self.gui.update_board(self.board)
            self.gui.upd()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.main()
    sys.exit(app.exec_())
