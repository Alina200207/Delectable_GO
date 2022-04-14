from Board import Board


class Point:
    def __init__(self, x: int, y: int):
        """Constructor"""
        self.x = x
        self.y = y

    def equals(self, other):
        if type(other) != type(self):
            return False
        if self.x == other.x & self.y == other.y:
            return True
        else:
            return False

    def get_close_neighbours(self):
        return [Point(self.x - 1, self.y), Point(self.x, self.y - 1), Point(self.x + 1, self.y),
                Point(self.x, self.y + 1)]

    def get_diagonal_neighbours(self):
        return [Point(self.x - 1, self.y - 1), Point(self.x + 1, self.y - 1), Point(self.x + 1, self.y + 1),
                Point(self.x - 1, self.y + 1)]

    def get_all_neighbours(self):
        return self.get_close_neighbours().extend(self.get_diagonal_neighbours())
