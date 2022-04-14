import random

from Board import Board
from Point import Point


def get_free_points(board, stone_type):
    free_points = []
    for i in range(board.size):
        for j in range(board.size):
            p = Point(i, j, board)
            if board.get_point(p) == Board.empty:
                if board.check(p, stone_type):
                    if p.is_eye_point() and p.is_real_eye():
                        continue
                    free_points.append(p)
    return free_points


def play_random_move(board: Board):
    free_points = get_free_points(board, Board.our)
    if len(free_points) == 0:
        return board, None
    move = free_points.pop(random.randint(0, len(free_points)))
    board.make_move(move, Board.our)
    return board, move

