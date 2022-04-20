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
        self.assertFalse(board.is_eye_point((2, 4), board.our))
        board.board[1][4] = Board.Board.our
        self.assertTrue(board.is_eye_point((2, 4), board.our))

    def test_is_real_eye(self):
        board = Board.Board()
        board.board[3][2] = board.our
        board.board[5][2] = board.our
        self.assertTrue(board.is_real_eye((4, 1)))
        board.board[6][4] = board.our
        board.board[8][6] = board.empty
        board.board[6][6] = board.alien
        board.board[8][4] = board.our
        self.assertTrue(board.is_real_eye((7, 5)))
        board.board[8][6] = board.alien
        self.assertFalse(board.is_real_eye((7, 5)))

    def test_get_point_type(self):
        board = Board.Board()
        board.board[3][2] = board.our
        board.board[2][3] = board.alien
        self.assertEqual(board.get_point_type((3, 2)), 2)
        self.assertEqual(board.get_point_type((2, 3)), 3)
        self.assertEqual(board.get_point_type((0, 4)), 4)
        self.assertEqual(board.get_point_type((5, 2)), 1)

    def test_set_point(self):
        board = Board.Board()
        board.set_point((4, 5), board.our)
        self.assertEqual(board.last_point, (4, 5))
        self.assertEqual(board.get_point_type((4, 5)), board.our)

    def test_get_opposite_stone(self):
        board = Board.Board()
        board.set_point((4, 5), board.our)
        self.assertEqual(board.get_opposite_stone(board.get_point_type((4, 5))), board.alien)
        board.set_point((6, 7), board.alien)
        self.assertEqual(board.get_opposite_stone(board.get_point_type((6, 7))), board.our)

    def test_try_move(self):
        board = Board.Board()
        board.try_move((5, 6), board.alien)
        self.assertEqual((5, 6), board.try_point)
        self.assertEqual(board.alien, board.get_point_type((5, 6)))

    def test_undo_move(self):
        board = Board.Board()
        board.try_move((5, 6), board.alien)
        board.undo_move()
        self.assertEqual(None, board.try_point)
        self.assertEqual(board.empty, board.get_point_type((5, 6)))

    def test_set_last_point(self):
        board = Board.Board()
        board.set_last_point((6, 8))
        self.assertEqual((6, 8), board.get_last_point())

    def test_set_ko_position(self):
        board = Board.Board()
        board.set_ko_position((4, 5), board.alien)
        self.assertEqual((4, 5), board.ko_point)
        self.assertEqual(board.alien, board.ko_stone_type)

    def test_is_ko_point(self):
        board = Board.Board()
        self.assertFalse(board.is_ko_point((2, 1), board.alien))
        board.set_ko_position((3, 4), board.our)
        self.assertTrue(board.is_ko_point((3, 4), board.our))
        self.assertFalse(board.is_ko_point((3, 4), board.alien))

    def test_get_last_point(self):
        board = Board.Board()
        board.set_last_point((4, 5))
        self.assertEqual((4, 5), board.get_last_point())

    def test_make_move(self):
        board = Board.Board()
        board.set_point((2, 3), board.alien)
        board.set_point((2, 5), board.alien)
        board.set_point((1, 4), board.alien)
        board.set_point((2, 4), board.our)
        board.make_move((3, 4), board.alien)
        self.assertEqual(board.get_point_type((3, 4)), board.alien)
        self.assertEqual(board.get_point_type((2, 4)), board.empty)

    def test_get_close_neighbors(self):
        board = Board.Board()
        self.assertListEqual([(4, 6), (5, 5), (6, 6), (5, 7)], board.get_close_neighbors((5, 6)))

    def test_get_diagonal_neighbors(self):
        board = Board.Board()
        self.assertListEqual([(4, 5), (6, 5), (6, 7), (4, 7)], board.get_diagonal_neighbors((5, 6)))

    def test_get_all_neighbors(self):
        board = Board.Board()
        self.assertListEqual([(4, 6), (5, 5), (6, 6), (5, 7), (4, 5), (6, 5), (6, 7), (4, 7)],
                             board.get_all_neighbors((5, 6)))


if __name__ == '__main__':
    unittest.main()
