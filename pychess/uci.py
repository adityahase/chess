import pychess


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

    def process_command(self, command):
        method_map = {
            "isready": self.isready,
            "quit": self.quit,
            "uci": self.uci,
        }
        method = method_map.get(command, self.unknown_command)
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
