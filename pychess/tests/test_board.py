import unittest

from pychess.board import Board


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

    def test_init_en_passant_fen(self):
        FEN = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        board = Board(FEN)
        self.assertEqual(board.fen, FEN)

    def test_init_en_passant_fen_2(self):
        FEN = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
        board = Board(FEN)
        self.assertEqual(board.fen, FEN)

    def test_moves_from_start_position(self):
        board = Board()
        uci_moves = sorted([move.uci() for move in board.moves()])
        self.assertEqual(
            uci_moves,
            [
                "a2a3",
                "a2a4",
                "b2b3",
                "b2b4",
                "c2c3",
                "c2c4",
                "d2d3",
                "d2d4",
                "e2e3",
                "e2e4",
                "f2f3",
                "f2f4",
                "g2g3",
                "g2g4",
                "h2h3",
                "h2h4",
            ],
        )


if __name__ == "__main__":
    unittest.main()
