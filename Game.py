import IIPlay
from Board import Board
from Point import Point


def main():
    board = Board
    stone_type = Board.our
    pass_move = 0
    while True:
        if stone_type == Board.our:
            move = IIPlay.play_random_move(board)
            if not move[1]:
                pass_move += 1
            else:
                pass_move = 0
        if stone_type == Board.alien:
            person_move = get_person_move()
            if board.check(person_move, stone_type):
                board.make_move(person_move, stone_type)
                pass_move = 0
            if is_passing:
                pass_move += 1
        if pass_move >= 2:
            count_points(board)
            break
        stone_type = board.get_opposite_stone(board, stone_type)


def count_points(board: Board):
    comp_score = 0
    person_score = 0
    for i in range(board.size):
        for j in range(board.size):
            point = Point(i, j, board)
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
