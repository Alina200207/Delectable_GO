class OrdinaryPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.equals(other)

    def equals(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def get_close_neighbors(self) -> list:
        """
        :return: list of direct neighbors of the point
        """
        return [
            OrdinaryPoint(self.x - 1, self.y), OrdinaryPoint(self.x, self.y - 1), OrdinaryPoint(self.x + 1, self.y),
            OrdinaryPoint(self.x, self.y + 1)
        ]

    def get_diagonal_neighbors(self) -> list:
        """
        :return: list of diagonal neighbors of the point
        """
        return [OrdinaryPoint(self.x - 1, self.y - 1), OrdinaryPoint(self.x + 1, self.y - 1),
                OrdinaryPoint(self.x + 1, self.y + 1),
                OrdinaryPoint(self.x - 1, self.y + 1)]

    def get_all_neighbors(self) -> list:
        """
        :return: list of all neighbors of the point
        """
        neighbors = self.get_close_neighbors()
        neighbors.extend(self.get_diagonal_neighbors())
        return neighbors
