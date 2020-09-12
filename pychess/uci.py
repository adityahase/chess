import pychess


class UCI:
    def isready(self):
        return ["readyok"]

    def uci(self):
        return [
            f"id name {pychess.__name__} {pychess.__version__} ",
            f"id author {pychess.__author__}",
            "uciok",
        ]

    def process_command(self, command):
        method_map = {
            "isready": self.isready,
            "uci": self.uci,
        }
        method = method_map[command]
        return method()

    def run(self):
        while True:
            command = input()
            result = self.process_command(command)
            if isinstance(result, list):
                for line in result:
                    print(line)
