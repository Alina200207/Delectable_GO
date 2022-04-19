import random

from Board import Board


def get_free_points(board, stone_type):
    """
    :param board: the board with current condition of the game
    :param stone_type: type of stone
    :return: list of points where stone can be put
    """
    free_points = []
    for i in range(board.size + 1):
        for j in range(board.size + 1):
            p = (i, j)
            if board.check(p, stone_type):
                if board.is_eye_point(p, Board.our) and board.is_real_eye(p):
                    continue
                free_points.append(p)
    return free_points


def play_random_move(board: Board):
    """
    :param board: the board with current condition of the game
    :return: tuple of new condition the board with set move and the move itself
    """
    free_points = get_free_points(board, Board.our)
    if len(free_points) == 0:
        return board, None
    move = free_points.pop(random.randint(0, len(free_points) - 1))
    print(move)
    board.make_move(move, Board.our)
    return board, move


