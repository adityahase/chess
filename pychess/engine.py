from chess import Board
from pychess.evaluate import SCORES


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
        moves = list(self.board.legal_moves)
        scores = [(move, self.evaluate(move)) for move in moves]
        moves = sorted(scores, key=lambda x: x[1], reverse=True)
        move = moves[0][0]
        return str(move)

    def evaluate(self, move):
        board = self.board.copy()
        board.push(move)

        score = 0
        for square, piece in board.piece_map().items():
            ii, jj = square // 8, square % 8
            score += SCORES[piece.piece_type][ii][jj]
        return score
