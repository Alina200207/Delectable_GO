import random

from Board import Board


def get_free_points(board, stone_type):
    """
    :param board: the board with current condition of the game
    :param stone_type: type of stone
    :return: list of points where stone can be put
    """
    free_points = []
    for i in range(1, board.size + 1):
        for j in range(1, board.size + 1):
            p = (i, j)
            if board.check_move_correctness(p, stone_type):
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
    board.make_move(move, Board.our)
    return board, move


def make_comp_move(board: Board):
    """
    makes a move relative to the player's move
    :param board: the board with current condition of the game
    :return: returns the board and the coordinates of the stone
    """
    for i in range(1, board.size + 1):
        for j in range(1, board.size + 1):
            point = (i, j)
            neighbors = board.get_close_neighbors(point)
            if board.get_point_type(point) == Board.alien:
                no_neighbors = True
                point_neighbor = None
                for neighbor in neighbors:
                    if board.get_point_type(neighbor) == Board.alien:
                        no_neighbors = False
                    if (board.get_point_type(neighbor) == Board.empty
                            and board.check_move_correctness(neighbor, board.our)):
                        if board.is_eye_point(neighbor, Board.our) and board.is_real_eye(neighbor):
                            continue
                        point_neighbor = neighbor
                        break
                if no_neighbors and point_neighbor:
                    board.make_move(point_neighbor, Board.our)
                    return board, point_neighbor
    return play_random_move(board)
