import pychess
from pychess.engine import Engine


class UCIQuitException(Exception):
    pass


class UCI:
    def isready(self, command=None):
        return ["readyok"]

    def quit(self, command=None):
        raise UCIQuitException

    def uci(self, command=None):
        return [
            f"id name {pychess.__name__} {pychess.__version__} ",
            f"id author {pychess.__author__}",
            "uciok",
        ]

    def position(self, command=None):
        fen, moves = None, []
        tokens = command.split()
        if len(tokens) == 2:
            _, fen = tokens
        elif "moves" in command:
            _, fen, _, *moves = tokens
        elif "fen" in command:
            _, __, fen = command.split(maxsplit=2)
        self.engine = Engine(fen, moves)

    def go(self, command=None):
        return [f"bestmove {self.engine.go()}"]

    def ucinewgame(self, command=None):
        self.engine = Engine(None, None)

    def process_command(self, command):
        method_map = {
            "isready": self.isready,
            "quit": self.quit,
            "uci": self.uci,
            "ucinewgame": self.ucinewgame,
            "position": self.position,
            "go": self.go,
        }
        method = method_map.get(command.split()[0], self.unknown_command)
        return method(command)

    def unknown_command(self, command):
        return [f"Unknown command: {command}"]

    def run(self):
        while True:
            command = input()
            try:
                result = self.process_command(command)
            except UCIQuitException:
                break
            if isinstance(result, list):
                for line in result:
                    print(line)
