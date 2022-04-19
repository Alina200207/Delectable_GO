import unittest

import Board


class MyTestCase(unittest.TestCase):

    def test_is_visited(self):
        visited_list = [(1, 2), (3, 4), (5, 6)]
        queue_list = [(3, 5), (8, 9)]
        self.assertTrue(Board.is_visited(visited_list, queue_list, (3, 4)))
        self.assertFalse(Board.is_visited(visited_list, queue_list, (2, 6)))

    def test_dame_exists(self):
        board = Board.Board()
        board.board[4][4] = Board.Board.our
        board.board[4][6] = Board.Board.empty
        board.board[3][5] = Board.Board.alien
        board.board[5][5] = Board.Board.our
        self.assertTrue(board.dame_exists((4, 5)))
        board.board[4][6] = Board.Board.our
        self.assertFalse(board.dame_exists((4, 5)))

    def test_is_eye_point(self):
        board = Board.Board()
        board.board[2][3] = Board.Board.our
        board.board[1][4] = Board.Board.empty
        board.board[3][4] = Board.Board.our
        board.board[2][5] = Board.Board.our


if __name__ == '__main__':
    unittest.main()
