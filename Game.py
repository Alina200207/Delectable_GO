import IIPlay
from Board import Board
from Point import Point


class Game:
    def __init__(self):
        self.board = Board()
        self.count_pass = 0


    def main(self):
        stone_type = Board.our
        while True:
            if stone_type == Board.our:
                move = IIPlay.play_random_move(self.board)
                if not move[1]:
                    self.count_pass += 1
                else:
                    self.count_pass = 0
            if stone_type == Board.alien:
                person_move = get_person_move()
                if self.board.check(person_move, stone_type):
                    self.board.make_move(person_move, stone_type)
                    self.count_pass = 0
                if is_passing:
                    self.count_pass += 1
            if self.count_pass >= 2:
                self.count_points(self.board)
                break
            stone_type = self.board.get_opposite_stone(stone_type)

    def get_board(self):
        return self.board

    def count_points(self, board: Board):
        comp_score = 0
        person_score = 0
        for i in range(board.size):
            for j in range(board.size):
                point = Point(i, j)
                if board.get_point(point) == Board.empty:
                    survivors = point.get_close_neighbours()
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
