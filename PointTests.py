import unittest
import Point
import Board


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_equal_points(self):
        board = Board.Board()
        first = Point.Point(3, 6, board)
        second = Point.Point(3, 6, board)
        self.assertTrue(first.equals(second))

    def test_not_equal_points(self):
        board = Board.Board()
        first = Point.Point(1, 6, board)
        second = Point.Point(3, 6, board)
        self.assertFalse(first.equals(second))


if __name__ == '__main__':
    unittest.main()
