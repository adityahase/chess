import unittest
import pychess
from pychess.uci import UCI, UCIQuitException


class TestUCI(unittest.TestCase):
    def setUp(self):
        self.uci = UCI()

    def test_uci(self):
        uciok = self.uci.uci()
        self.assertEqual(len(uciok), 3)
        self.assertIn(pychess.__name__, uciok[0])
        self.assertIn(pychess.__version__, uciok[0])
        self.assertIn(pychess.__author__, uciok[1])
        self.assertEqual("uciok", uciok[2])

    def test_isready(self):
        readyok = self.uci.isready()
        self.assertEqual(len(readyok), 1)
        self.assertEqual("readyok", readyok[0])

    def test_quit(self):
        self.assertRaises(UCIQuitException, self.uci.quit)

    def test_unknown_command(self):
        unknown_command = self.uci.process_command("randomcommand")
        self.assertEqual(len(unknown_command), 1)
        self.assertIn("Unknown command", unknown_command[0])
        self.assertIn("randomcommand", unknown_command[0])

    def test_ucinewgame(self):
        ucinewgame = self.uci.ucinewgame()
        self.assertEqual(ucinewgame, None)


if __name__ == "__main__":
    unittest.main()
