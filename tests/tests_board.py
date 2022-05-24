import unittest

import Board
from Point import OrdinaryPoint


class BoardTests(unittest.TestCase):
    def test_is_visited(self):
        visited_list = [OrdinaryPoint(1, 2), OrdinaryPoint(3, 4), OrdinaryPoint(5, 6)]
        queue_list = [OrdinaryPoint(3, 5), OrdinaryPoint(8, 9)]
        self.assertTrue(Board.is_visited(visited_list, queue_list, OrdinaryPoint(3, 4)))
        self.assertFalse(Board.is_visited(visited_list, queue_list, OrdinaryPoint(2, 6)))

    def test_dame_exists(self):
        board = Board.Board(9)
        board.board[4][4] = Board.Board.our
        board.board[4][6] = Board.Board.empty
        board.board[3][5] = Board.Board.alien
        board.board[5][5] = Board.Board.our
        self.assertTrue(board.dame_exists(OrdinaryPoint(4, 5)))
        board.board[4][6] = Board.Board.our
        self.assertFalse(board.dame_exists(OrdinaryPoint(4, 5)))

    def test_is_eye_point(self):
        board = Board.Board(9)
        board.board[2][3] = Board.Board.our
        board.board[1][4] = Board.Board.empty
        board.board[3][4] = Board.Board.our
        board.board[2][5] = Board.Board.our
        self.assertFalse(board.is_eye_point(OrdinaryPoint(2, 4), board.our))
        board.board[1][4] = Board.Board.our
        self.assertTrue(board.is_eye_point(OrdinaryPoint(2, 4), board.our))

    def test_is_real_eye(self):
        board = Board.Board(9)
        board.board[3][2] = board.our
        board.board[5][2] = board.our
        self.assertTrue(board.is_real_eye(OrdinaryPoint(4, 1)))
        board.board[6][4] = board.our
        board.board[8][6] = board.empty
        board.board[6][6] = board.alien
        board.board[8][4] = board.our
        self.assertTrue(board.is_real_eye(OrdinaryPoint(7, 5)))
        board.board[8][6] = board.alien
        self.assertFalse(board.is_real_eye(OrdinaryPoint(7, 5)))

    def test_get_point_type(self):
        board = Board.Board(9)
        board.board[3][2] = board.our
        board.board[2][3] = board.alien
        self.assertEqual(board.get_point_type(OrdinaryPoint(3, 2)), 2)
        self.assertEqual(board.get_point_type(OrdinaryPoint(2, 3)), 3)
        self.assertEqual(board.get_point_type(OrdinaryPoint(0, 4)), 4)
        self.assertEqual(board.get_point_type(OrdinaryPoint(5, 2)), 1)

    def test_set_point(self):
        board = Board.Board(9)
        board.set_point(OrdinaryPoint(4, 5), board.our)
        self.assertEqual(board.last_point, OrdinaryPoint(4, 5))
        self.assertEqual(board.get_point_type(OrdinaryPoint(4, 5)), board.our)

    def test_get_opposite_stone(self):
        board = Board.Board(9)
        board.set_point(OrdinaryPoint(4, 5), board.our)
        self.assertEqual(board.get_opposite_stone(board.get_point_type(OrdinaryPoint(4, 5))), board.alien)
        board.set_point(OrdinaryPoint(6, 7), board.alien)
        self.assertEqual(board.get_opposite_stone(board.get_point_type(OrdinaryPoint(6, 7))), board.our)

    def test_try_move(self):
        board = Board.Board(9)
        board.try_move(OrdinaryPoint(5, 6), board.alien)
        self.assertEqual(OrdinaryPoint(5, 6), board.try_point)
        self.assertEqual(board.alien, board.get_point_type(OrdinaryPoint(5, 6)))

    def test_undo_move(self):
        board = Board.Board(9)
        board.try_move(OrdinaryPoint(5, 6), board.alien)
        board.undo_move()
        self.assertEqual(None, board.try_point)
        self.assertEqual(board.empty, board.get_point_type(OrdinaryPoint(5, 6)))

    def test_set_last_point(self):
        board = Board.Board(9)
        board.set_last_point(OrdinaryPoint(6, 8))
        self.assertEqual(OrdinaryPoint(6, 8), board.get_last_point())

    def test_set_ko_position(self):
        board = Board.Board(9)
        board.set_ko_position(OrdinaryPoint(4, 5), board.alien)
        self.assertEqual(OrdinaryPoint(4, 5), board.ko_point)
        self.assertEqual(board.alien, board.ko_stone_type)

    def test_is_ko_point(self):
        board = Board.Board(9)
        self.assertFalse(board.is_ko_point(OrdinaryPoint(2, 1), board.alien))
        board.set_ko_position(OrdinaryPoint(3, 4), board.our)
        self.assertTrue(board.is_ko_point(OrdinaryPoint(3, 4), board.our))
        self.assertFalse(board.is_ko_point(OrdinaryPoint(3, 4), board.alien))

    def test_get_last_point(self):
        board = Board.Board(9)
        board.set_last_point(OrdinaryPoint(4, 5))
        self.assertEqual(OrdinaryPoint(4, 5), board.get_last_point())

    def test_make_move(self):
        board = Board.Board(9)
        board.set_point(OrdinaryPoint(2, 3), board.alien)
        board.set_point(OrdinaryPoint(2, 5), board.alien)
        board.set_point(OrdinaryPoint(1, 4), board.alien)
        board.set_point(OrdinaryPoint(2, 4), board.our)
        board.make_move(OrdinaryPoint(3, 4), board.alien)
        self.assertEqual(board.get_point_type(OrdinaryPoint(3, 4)), board.alien)
        self.assertEqual(board.get_point_type(OrdinaryPoint(2, 4)), board.empty)

    # def test_get_close_neighbors(self):
    #    board = Board.Board(9)
    #   self.assertListEqual([(4, 6), (5, 5), (6, 6), (5, 7)], board.get_close_neighbors((5, 6)))

    # def test_get_diagonal_neighbors(self):
    #    board = Board.Board(9)
    #    self.assertListEqual([(4, 5), (6, 5), (6, 7), (4, 7)], board.get_diagonal_neighbors((5, 6)))

    # def test_get_all_neighbors(self):
    #    board = Board.Board(9)
    #    self.assertListEqual([(4, 6), (5, 5), (6, 6), (5, 7), (4, 5), (6, 5), (6, 7), (4, 7)],
    #                         board.get_all_neighbors((5, 6)))

    def test_check_move_correctness(self):
        board = Board.Board(9)
        board.set_point(OrdinaryPoint(2, 3), board.alien)
        board.set_point(OrdinaryPoint(2, 5), board.alien)
        board.set_point(OrdinaryPoint(1, 4), board.alien)
        board.set_point(OrdinaryPoint(2, 4), board.our)
        # point is not empty
        self.assertFalse(board.check_move_correctness(OrdinaryPoint(2, 4), board.alien))
        board.set_ko_position(OrdinaryPoint(5, 6), board.our)
        # point is ko
        self.assertFalse(board.check_move_correctness(OrdinaryPoint(5, 6), board.our))
        # point has dame
        self.assertTrue(board.check_move_correctness(OrdinaryPoint(3, 4), board.alien))
        # make a situation when point can make a "suicidal" move if it can kill enemy's points
        board.set_point(OrdinaryPoint(9, 1), board.our)
        board.set_point(OrdinaryPoint(7, 1), board.alien)
        board.set_point(OrdinaryPoint(8, 1), board.our)
        board.set_point(OrdinaryPoint(7, 2), board.alien)
        board.set_point(OrdinaryPoint(8, 2), board.our)
        board.set_point(OrdinaryPoint(8, 3), board.alien)
        board.set_point(OrdinaryPoint(9, 3), board.our)
        board.set_point(OrdinaryPoint(8, 4), board.alien)
        board.set_point(OrdinaryPoint(9, 4), board.our)
        board.set_point(OrdinaryPoint(9, 5), board.alien)
        self.assertTrue(board.check_move_correctness(OrdinaryPoint(9, 2), board.alien))
        # make a situation when point can not make suicidal move
        board.set_point(OrdinaryPoint(1, 8), board.our)
        board.set_point(OrdinaryPoint(2, 9), board.our)
        self.assertFalse(board.check_move_correctness(OrdinaryPoint(1, 9), board.alien))

    def test_count_points(self):
        board = Board.Board(9)
        for i in range(1, board.size + 1):
            for j in range(1, board.size - 3):
                if i % 2 == 0 and j % 2 == 0:
                    board.make_move(OrdinaryPoint(i, j), board.alien)
                if i % 2 == 1 and j % 2 == 1:
                    board.make_move(OrdinaryPoint(i, j), board.alien)
        for i in range(1, board.size + 1):
            for j in range(board.size - 3, board.size + 1):
                if i % 2 == 1 and j % 2 == 0:
                    board.make_move(OrdinaryPoint(i, j), board.our)
                if i % 2 == 0 and j % 2 == 1:
                    board.make_move(OrdinaryPoint(i, j), board.our)
        self.assertEqual((36, 45), board.count_points())


if __name__ == '__main__':
    unittest.main()
