import unittest

from chess.engine import SimpleEngine

import pychess


class TestCLI(unittest.TestCase):
    def test_uci(self):
        engine = SimpleEngine.popen_uci("chesscli")
        self.assertIn("name", engine.id)
        self.assertIn(pychess.__name__, engine.id["name"])
        self.assertIn(pychess.__version__, engine.id["name"])
        self.assertIn("author", engine.id)
        self.assertIn(pychess.__author__, engine.id["author"])
        engine.close()


if __name__ == "__main__":
    unittest.main()
