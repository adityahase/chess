import unittest
import pychess
from pychess.uci import UCI


class TestUCI(unittest.TestCase):
    def test_uci(self):
        uci = UCI()
        uciok = uci.uci()
        self.assertEqual(len(uciok), 3)
        self.assertIn(pychess.__name__, uciok[0])
        self.assertIn(pychess.__version__, uciok[0])
        self.assertIn(pychess.__author__, uciok[1])
        self.assertEqual("uciok", uciok[2])



if __name__ == "__main__":
    unittest.main()
