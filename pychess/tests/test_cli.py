import unittest

from chess.engine import SimpleEngine
import pychess


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.engine = SimpleEngine.popen_uci("chesscli")

    def tearDown(self):
        self.engine.close()

    def test_uci(self):
        self.assertIn("name", self.engine.id)
        self.assertIn(pychess.__name__, self.engine.id["name"])
        self.assertIn(pychess.__version__, self.engine.id["name"])
        self.assertIn("author", self.engine.id)
        self.assertIn(pychess.__author__, self.engine.id["author"])

    def test_uci_quit(self):
        self.engine.quit()


if __name__ == "__main__":
    unittest.main()
