import random
import Board
from Point import OrdinaryPoint


def get_free_points(board: Board, stone_type: int):
    """
    :param board: the board with current condition of the game
    :param stone_type: type of stone
    :return: list of points where stone can be put
    """
    free_points = []
    for i in range(1, board.size + 1):
        for j in range(1, board.size + 1):
            p = OrdinaryPoint(i, j)
            if board.check_move_correctness(p, stone_type):
                if board.is_eye_point(p, Board.Board.our) and board.is_real_eye(p):
                    continue
                free_points.append(p)
    return free_points


def play_random_move(board: Board):
    """
    :param board: the board with current condition of the game
    :return: tuple of new condition the board with set move and the move itself
    """
    free_points = get_free_points(board, Board.Board.our)
    if len(free_points) == 0:
        return board, None
    move = free_points.pop(random.randint(0, len(free_points) - 1))
    board.make_move(move, Board.Board.our)
    return board, move


def make_comp_move(board: Board):
    """
    makes a move relative to the player's move
    :param board: the board with current condition of the game
    :return: returns the board and the coordinates of the stone
    """
    groups = find_groups_and_count_dame(board)
    if not groups:
        return play_random_move(board)
    sorted(groups.items(), key=lambda x: x[0])
    groups = groups.values()
    for group in groups:
        if board.is_eye_point(group[0], Board.Board.our) and board.is_real_eye(group[0]):
            continue
        point = find_dame(board, group[0])
        if not point:
            continue
        else:
            if not board.check_move_correctness(point, Board.Board.our):
                continue
            board.make_move(point, Board.Board.our)
            return board, point
    return play_random_move(board)


def find_groups_and_count_dame(board: Board):
    """
    :param board: the board with current condition of the game
    :return: returns a dictionary with the key - the number of free points and the value - the coordinates of the stones
    """
    count = 0
    groups = {}
    for i in range(1, board.size + 1):
        for j in range(1, board.size + 1):
            point = OrdinaryPoint(i, j)
            neighbors = find_group(board, point)
            if neighbors is None:
                continue
            if board.get_point_type(point) == Board.Board.alien:
                for neighbor in neighbors:
                    count = count_dame(board, neighbor)
                if count not in groups:
                    groups[count] = neighbors
    return groups


def find_dame(board: Board, point: OrdinaryPoint) -> OrdinaryPoint:
    """
    :param board: the board with current condition of the game
    :param point: the point at which the existence of a dame is determined
    :return: empty point
    """
    neighbours = point.get_close_neighbors()
    for neighbour in neighbours:
        if board.get_point_type(neighbour) == Board.Board.empty:
            return neighbour
    return None


def find_group(board: Board, point: OrdinaryPoint) -> list:
    """
    :param board: the board with current condition of the game
    :param point: the point from which the search for the group begins
    :return: a group of stones
    """
    queue = []
    visited = []
    if board.get_point_type(point) == Board.Board.alien:
        queue.append(point)
        while len(queue) > 0:
            current = queue.pop()
            neighbours = current.get_close_neighbors()
            visited.append(current)
            for neighbour in neighbours:
                if (board.get_point_type(current) == board.get_point_type(neighbour) and
                        not Board.is_visited(visited, queue, neighbour)):
                    queue.append(neighbour)
    return visited


def count_dame(board: Board, point: OrdinaryPoint):
    """
    :param board: the board with current condition of the game
    :param point: the point at which the existence of a dame is determined
    :return: the number of free points next to the stone
    """
    count = 0
    neighbours = point.get_close_neighbors()
    for neighbour in neighbours:
        if board.get_point_type(neighbour) == Board.Board.empty:
            count += 1
    return count
