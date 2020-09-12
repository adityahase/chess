import unittest
from pychess.engine import Board


class TestBoard(unittest.TestCase):
    def test_init_empty(self):
        board = Board()
        self.assertEqual(board.fen, Board.STARTING_FEN)

    def test_init_start_fen(self):
        board = Board(Board.STARTING_FEN)
        self.assertEqual(board.fen, Board.STARTING_FEN)

    def test_init_non_trivial_fen(self):
        FEN = "6n1/bPB1p3/4Pp1p/1p1p3P/1P1P1P2/8/5K1k/8 w - - 0 1"
        board = Board(FEN)
        self.assertEqual(board.fen, FEN)


if __name__ == "__main__":
    unittest.main()
