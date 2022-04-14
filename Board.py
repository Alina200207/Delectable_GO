from Point import Point


def is_visited(visited, queue, point: Point):
    for elem in visited:
        if point.equals(elem):
            return True
    for elem_q in queue:
        if point.equals(elem_q):
            return True
    return False


class Board:
    empty = 1
    our = 2
    alien = 3
    border = 4

    def __init__(self):
        self.size = 9
        self.ko_time = 0
        self.ko_point = None
        self.ko_stone_type = Board.empty
        self.last_point = None
        self.try_point = None
        self.board = [[self.empty for _ in range(0, 11)] for _ in range(0, 11)]
        for k in range(0, 9):
            self.board[0][k] = self.border
            self.board[k][0] = self.border
            self.board[k][self.size] = self.border
            self.board[self.size][k] = self.border

    def dame_exists(self, point: Point):
        neighbours = point.get_close_neighbours()
        for neighbour in neighbours:
            if neighbour.get_point_type() == Board.empty:
                return True
        return False

    def is_eye_point(self, point: Point):
        neighbours = point.get_close_neighbours()
        for neighbour in neighbours:
            if neighbour.get_point_type() == Board.empty or neighbour.get_point_type() == \
                    self.get_opposite_stone(self.get_point_type(neighbour)):
                return False
        return True

    def is_real_eye(self, point: Point):
        diag_neighbours = point.get_diagonal_neighbours()
        same_stones = 0
        another_stones = 0
        is_border = False
        for neighbor in diag_neighbours:
            if neighbor.get_point_type() == Board.our:
                same_stones += 1
            if neighbor.get_point_type() == Board.alien:
                another_stones += 1
            if neighbor.get_point_type() == Board.border:
                is_border = True
        if (another_stones == 0 and is_border) or (another_stones <= 1 and not is_border):
            return True
        return False

    def get_point(self, point: Point):
        return self.board[point.x][point.y]

    def get_point_type(self, point: Point):
        return self.get_point(point)

    def set_point(self, point: Point, pointType: int):
        self.board[point.x][point.y] = pointType
        if pointType == self.alien or pointType == self.our:
            self.last_point = Point(point.x, point.y)
            self.ko_time += 1

    def get_opposite_stone(self, stone_type: int):
        if stone_type == self.our:
            return self.alien
        else:
            return self.our

    def try_move(self, point: Point, point_type: int):
        self.try_point = point
        self.set_point(point, point_type)

    def undo_move(self):
        self.set_point(self.try_point, self.empty)
        self.try_point = None

    def set_last_point(self, point: Point):
        self.last_point = point

    def set_ko(self, point: Point, point_type):
        self.ko_stone_type = point_type
        self.ko_point = point
        self.ko_time = 0

    def is_ko_point(self, point: Point):
        if self.ko_time == 0 and self.ko_point:
            if point.equals(self.ko_point) and self.get_point(self.ko_point) == self.get_point(point):
                return True
        return False

    def get_last_point(self):
        return self.last_point

    def make_move(self, point: Point, point_type: int):
        self.set_point(point, point_type)
        self.remove_dead_stones(point)

    def check(self, point: Point, point_type: int):
        if self.get_point(point) != Board.empty:
            return False
        if self.dame_exists(point):
            return True
        if self.is_ko_point(point):
            return False
        neighbours = point.get_close_neighbours()
        self.try_move(point, point_type)
        if self.is_dead(point):
            for neighbour in neighbours:
                if self.get_opposite_stone(point_type) != neighbour.get_point_type():
                    if self.is_dead(neighbour):
                        self.undo_move()
                        return True
        else:
            self.undo_move()
            return True
        self.undo_move()
        return False

    def is_dead(self, point: Point):
        queue = []
        visited = []
        if self.get_point(point) == Board.our or self.get_point(point) == Board.alien:
            queue.append(point)
            while len(queue) > 0:
                current = queue.pop()
                if current.dame_exists():
                    return []
                neighbours = current.get_close_neighbours()
                visited.append(current)
                for neighbour in neighbours:
                    if self.get_point(current) == self.get_point(neighbour) and \
                            not is_visited(visited, queue, neighbour):
                        queue.append(neighbour)
        return visited

    def remove_dead_stones(self, last: Point):
        stone_type = self.get_opposite_stone(self.get_point(last))
        last_neighbours = last.get_close_neighbours()
        all_deleted = 0
        is_eye = self.is_eye_point(last)
        for neighbour in last_neighbours:
            if self.get_point(neighbour) == stone_type:
                deleted = self.delete_group_if_it_is_dead(neighbour)
                all_deleted += deleted
                if deleted == 1:
                    last = neighbour
        if all_deleted == 1 and last and is_eye:
            self.set_ko(last, stone_type)
        if all_deleted > 0:
            return True
        return False

    def delete_group_if_it_is_dead(self, point: Point):
        group = self.is_dead(point)
        for point_from_group in group:
            self.set_point(point_from_group, Board.empty)
        return len(group)
