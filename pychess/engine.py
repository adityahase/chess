COLORS = [True, False]
PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]


class Piece:
    def __init__(self, symbol):
        self.type = PIECE_SYMBOLS.index(symbol.lower())
        self.color = symbol.isupper()

    @property
    def symbol(self):
        symbol = PIECE_SYMBOLS[self.type]
        return symbol.upper() if self.color else symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return str(self.symbol)


class Board:
    STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    STARTING_BOARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    def __init__(self, fen=None):
        self.fen = fen or self.STARTING_FEN

    def __str__(self):
        ranks = []
        for rank in self.board:
            file = []
            for square in rank:
                file.append(str(square or " "))
            ranks.append("".join(file))
        return "\n".join(ranks)

    def __repr__(self):
        return str(self.__str__())

    @property
    def fen(self):
        return " ".join(
            [
                self.board_fen,
                self.turn_fen,
                self.castling_fen,
                self.en_passant_fen,
                self.half_move_fen,
                self.full_move_fen,
            ]
        )

    @fen.setter
    def fen(self, value):
        """Parse passed FEN string and set self.board"""
        # A FEN string looks like
        # "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        # https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
        # https://ia802908.us.archive.org/26/items/pgn-standard-1994-03-12/PGN_standard_1994-03-12.txt
        board, turn, castling, en_passant, half_move, full_move = value.split()
        self.board_fen = board
        self.turn_fen = turn
        self.castling_fen = castling
        self.en_passant_fen = en_passant
        self.half_move_fen = half_move
        self.full_move_fen = full_move

    @property
    def board_fen(self):
        def _encode_fen_rank(rank):
            encoded = []
            for square in rank:
                if square == " ":
                    if encoded and encoded[-1].isdigit():
                        encoded[-1] = str(int(encoded[-1]) + 1)
                    else:
                        encoded.append("1")
                else:
                    encoded.append(square)
            return encoded

        rank_fens = []
        for rank in self.board:
            square_fens = []
            for square in rank:
                square_fen = str(square or " ")
                square_fens.append(square_fen)
            rank_fen = "".join(_encode_fen_rank(square_fens))
            rank_fens.append(rank_fen)
        return "/".join(rank_fens)

    @board_fen.setter
    def board_fen(self, board_fen):
        def _decode_fen_rank(rank):
            decoded = []
            for square in rank:
                if square.isdigit():
                    decoded.extend([None] * int(square))
                else:
                    decoded.append(square)
            return decoded

        self.board = []
        for fen_rank in board_fen.split("/"):
            rank = []
            for fen_square in _decode_fen_rank(fen_rank):
                if fen_square:
                    piece = Piece(fen_square)
                else:
                    piece = None
                rank.append(piece)
            self.board.append(rank)

    @property
    def turn_fen(self):
        return ""

    @turn_fen.setter
    def turn_fen(self, turn_fen):
        return ""

    @property
    def castling_fen(self):
        return ""

    @castling_fen.setter
    def castling_fen(self, castling_fen):
        return ""

    @property
    def en_passant_fen(self):
        return ""

    @en_passant_fen.setter
    def en_passant_fen(self, en_passant_fen):
        return ""

    @property
    def half_move_fen(self):
        return ""

    @half_move_fen.setter
    def half_move_fen(self, half_move_fen):
        return ""

    @property
    def full_move_fen(self):
        return ""

    @full_move_fen.setter
    def full_move_fen(self, full_move_fen):
        return ""
