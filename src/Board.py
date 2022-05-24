from Point import OrdinaryPoint


def is_visited(visited: list[OrdinaryPoint], queue: list[OrdinaryPoint], point: OrdinaryPoint) -> bool:
    """
    :param visited: list of visited points
    :param queue: list of points in queue
    :param point: point at which attendance is determined
    :return: a boolean value that determines whether the point is visited or not
    """
    for elem in visited:
        if point.equals(elem):
            return True
    for elem_q in queue:
        if point.equals(elem_q):
            return True
    return False


class Board:
    """
    Class of the game board.
    """
    empty = 1
    our = 2
    alien = 3
    border = 4

    def __init__(self, board_size: int):
        self.size = board_size
        self.ko_time = 0
        self.ko_point = None
        self.ko_stone_type = Board.empty
        self.last_point = None
        self.try_point = None
        self.board = [[self.empty for _ in range(0, self.size + 2)] for _ in range(self.size + 2)]
        for k in range(self.size + 2):
            self.board[0][k] = self.border
            self.board[k][0] = self.border
            self.board[k][self.size + 1] = self.border
            self.board[self.size + 1][k] = self.border

    def dame_exists(self, point: OrdinaryPoint) -> bool:
        """
        :param point: the point at which the existence of a dame is determined
        :return: a boolean value that determines whether the point has a dame or not
        """
        neighbours = point.get_close_neighbors()
        for neighbour in neighbours:
            if self.get_point_type(neighbour) == Board.empty:
                return True
        return False

    def is_eye_point(self, point: OrdinaryPoint, stone_type: int) -> bool:
        """
        :param stone_type:
        :param point: the point to check
        :return: a boolean value that determines whether the point is eye or not
        """
        neighbours = point.get_close_neighbors()
        for neighbour in neighbours:
            if self.get_point_type(neighbour) == Board.empty or (self.get_point_type(neighbour) ==
                                                                 self.get_opposite_stone(stone_type)):
                return False
        return True

    def is_real_eye(self, point: OrdinaryPoint) -> bool:
        """
        used only for computer move
        :param point: the point to check
        :return: a boolean value that determines whether the point is true eye or not
        """
        diag_neighbours = point.get_diagonal_neighbors()
        same_stones = 0
        another_stones = 0
        is_border = False
        for neighbor in diag_neighbours:
            if self.get_point_type(neighbor) == Board.our:
                same_stones += 1
            if self.get_point_type(neighbor) == Board.alien:
                another_stones += 1
            if self.get_point_type(neighbor) == Board.border:
                is_border = True
        if (another_stones == 0 and is_border) or (another_stones <= 1 and not is_border):
            return True
        return False

    def get_point_type(self, point: OrdinaryPoint) -> int:
        """
        :param point: point at which the stone type is required to determine
        :return: the type(can be 1(empty), 2(our), 3(alien), 4(border)) of point on the board
        """
        return self.board[point.x][point.y]

    def set_point(self, point: OrdinaryPoint, point_type: int):
        """
        Set the point_type at the point position on the board.

        :param point: point where put the stone
        :param point_type: stone type of point

        """
        self.board[point.x][point.y] = point_type
        if point_type == self.alien or point_type == self.our:
            self.last_point = OrdinaryPoint(point.x, point.y)
            self.ko_time += 1

    def get_opposite_stone(self, stone_type: int) -> int:
        """
        :param stone_type: type of the stone
        :return: the opposite type of the input stone type
        """
        if stone_type == self.our:
            return self.alien
        else:
            return self.our

    def try_move(self, point: OrdinaryPoint, point_type: int):
        """
        Set the point_type at the point position on the board to determine if the move is correct.

        :param point: point where put the stone
        :param point_type: type of the stone
        """
        self.try_point = point
        self.set_point(point, point_type)

    def undo_move(self):
        """
        Undo previous move after checking the correctness of the move.
        """
        self.set_point(self.try_point, Board.empty)
        self.try_point = None

    def set_last_point(self, point: OrdinaryPoint):
        """
        Set the last move point.

        :param point: the point of last move
        """
        self.last_point = point

    def set_ko_position(self, point: OrdinaryPoint, point_type):
        """
        Set the ko position (position that can lead to the repeating of the move).

        :param point:
        :param point_type:
        """
        self.ko_stone_type = point_type
        self.ko_point = point
        self.ko_time = 0

    def is_ko_point(self, point: OrdinaryPoint, point_type: int) -> bool:
        """
        :param point_type: type of the stone
        :param point: the point at which the presence of a ko position is determined
        :return: a boolean value that determines is the point makes ko position or not
        """
        if self.ko_time == 0 and self.ko_point:
            if point.equals(self.ko_point) and self.ko_stone_type == point_type:
                return True
        return False

    def get_last_point(self) -> OrdinaryPoint:
        """
        :return: the point of last move
        """
        return self.last_point

    def make_move(self, point: OrdinaryPoint, point_type: int):
        """
        Makes move and removes dead stones.

        :param point: the point at which stone move is made
        :param point_type: type of the stone
        """
        self.set_point(point, point_type)
        self.remove_dead_stones(point)

    def check_move_correctness(self, point: OrdinaryPoint, point_type: int) -> bool:
        """
        :param point: the point at which the correctness of the stone move is checked
        :param point_type: type of the stone
        :return: a boolean value of the correctness of the move
        """
        if self.get_point_type(point) != Board.empty:
            return False
        if self.is_ko_point(point, point_type):
            return False
        if self.dame_exists(point):
            return True
        neighbours = point.get_close_neighbors()
        self.try_move(point, point_type)
        if self.dead_points(point):
            for neighbour in neighbours:
                if self.get_opposite_stone(point_type) != self.get_point_type(neighbour):
                    if self.dead_points(neighbour):
                        self.undo_move()
                        return False
                else:
                    if self.dead_points(neighbour):
                        self.undo_move()
                        return True
        else:
            self.undo_move()
            return True
        self.undo_move()
        return False

    def dead_points(self, point: OrdinaryPoint) -> list:
        """
        Find the points that become dead.

        :param point: point from which start looking for potentially dead points
        :return: list of dead points
        """
        queue = []
        visited = []
        if self.get_point_type(point) == Board.our or self.get_point_type(point) == Board.alien:
            queue.append(point)
            while len(queue) > 0:
                current = queue.pop()
                if self.dame_exists(current):
                    return []
                neighbours = current.get_close_neighbors()
                visited.append(current)
                for neighbour in neighbours:
                    if (self.get_point_type(current) == self.get_point_type(neighbour) and
                            not is_visited(visited, queue, neighbour)):
                        queue.append(neighbour)
        return visited

    def remove_dead_stones(self, point: OrdinaryPoint):
        """
        Remove dead stones and set ko position if it exists.

        :param point: point from which the looking for dead points starts
        """
        point_type = self.get_point_type(point)
        stone_opposite_type = self.get_opposite_stone(point_type)
        last_neighbours = point.get_close_neighbors()
        all_deleted_count = 0
        is_eye = self.is_eye_point(point, stone_opposite_type)
        for neighbour in last_neighbours:
            if self.get_point_type(neighbour) == stone_opposite_type:
                deleted_count = self.delete_group_if_it_is_dead(neighbour)
                all_deleted_count += deleted_count
                if deleted_count == 1:
                    point = neighbour
        if all_deleted_count == 1 and point and is_eye:
            self.set_ko_position(point, stone_opposite_type)

    def delete_group_if_it_is_dead(self, point: OrdinaryPoint) -> int:
        """
        Deletes group of stones and returns size of group

        :param point: point from group
        :return: size of deleted group
        """
        group = self.dead_points(point)
        for point_from_group in group:
            self.set_point(point_from_group, Board.empty)
        return len(group)

    def count_stones_on_board(self):
        """

        :return: number of stones on the board
        """
        count = 0
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.get_point_type(OrdinaryPoint(i, j)) != self.empty:
                    count += 1
        return count

    def count_points(self) -> (int, int):
        """
        Computer and player scoring
        :return: returns a sheet with computer and player points
        """
        comp_score = 0
        person_score = 0
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                point = OrdinaryPoint(i, j)
                if self.get_point_type(point) == Board.empty:
                    survivors = point.get_close_neighbors()
                    is_comp_point, is_person_point = self.check_point_type(survivors)
                    if is_comp_point:
                        comp_score += 1
                    if is_person_point:
                        person_score += 1
                else:
                    if self.get_point_type(point) == Board.our:
                        comp_score += 1
                    if self.get_point_type(point) == Board.alien:
                        person_score += 1
        return comp_score, person_score

    def check_point_type(self, survivors: list):
        """
        :param survivors: survivors points
        :return: the boolean values that determines if the points are computer's or person's
        """
        is_comp_point = True
        is_person_point = True
        for p in survivors:
            point_type = self.get_point_type(p)
            if point_type != Board.our and point_type != Board.border:
                is_comp_point = False
                break
            if point_type != Board.alien and point_type != Board.border:
                is_person_point = False
                break
        return is_comp_point, is_person_point
