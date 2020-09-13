from chess import Board


class Engine:
    def __init__(self, fen, moves):
        if fen and fen != "startpos":
            self.board = Board(fen)
        else:
            self.board = Board()

        if moves:
            for move in moves:
                self.board.push_uci(move)

    def go(self):
        import random

        moves = list(self.board.legal_moves)
        move = random.choice(moves)
        return str(move)
