import unittest

import Board
import IIPlay
from Point import OrdinaryPoint


class IIPlayTests(unittest.TestCase):
    def test_get_free_points(self):
        board = Board.Board(9)
        for i in range(1, board.size + 1):
            for j in range(1, board.size - 2):
                if i % 2 == 0 and j % 2 == 0:
                    board.set_point(OrdinaryPoint(i, j), board.alien)
                if i % 2 == 1 and j % 2 == 1:
                    board.set_point(OrdinaryPoint(i, j), board.alien)
        for k in range(1, board.size + 1):
            board.set_point(OrdinaryPoint(k, 9), board.alien)
            board.set_point(OrdinaryPoint(k, 8), board.alien)
        for n in range(1, board.size + 1):
            if n % 2 == 0:
                board.set_point(OrdinaryPoint(n, 7), board.alien)
        print(IIPlay.get_free_points(board, board.our))
        self.assertListEqual([OrdinaryPoint(1, 6), OrdinaryPoint(1, 7), OrdinaryPoint(3, 6), OrdinaryPoint(3, 7),
                              OrdinaryPoint(5, 6), OrdinaryPoint(5, 7), OrdinaryPoint(7, 6), OrdinaryPoint(7, 7),
                              OrdinaryPoint(9, 6), OrdinaryPoint(9, 7)],
                             IIPlay.get_free_points(board, board.our))

    def test_make_comp_move(self):
        board = Board.Board(9)
        board.set_point(OrdinaryPoint(5, 4), board.alien)
        for i in range(0, 4):
            move = IIPlay.make_comp_move(board)
            self.board = move[0]
            board.set_point(move[1], board.our)
        self.assertEqual(board.empty, board.get_point_type(OrdinaryPoint(5, 4)))
        random_move = IIPlay.make_comp_move(board)
        self.assertIsNotNone(random_move[1])


if __name__ == '__main__':
    unittest.main()
