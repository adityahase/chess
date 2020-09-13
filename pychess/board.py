COLORS = [WHITE, BLACK] = [True, False]

PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = list(range(1, 7))

SQUARES = list(range(64))

FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANK_NAMES = ["1", "2", "3", "4", "5", "6", "7", "8"]
SQUARE_NAMES = [file + rank for rank in RANK_NAMES for file in FILE_NAMES]


def square_mirror(square):
    """Mirror the square vertically"""
    # https://www.chessprogramming.org/Flipping_Mirroring_and_Rotating
    # This works because 56 = 0b111000, Rest is trivial
    return square ^ 56


SQUARES_MIRRORED = [square_mirror(sq) for sq in SQUARES]

B_EMPTY = 0
B_SQUARES = [1 << square for square in SQUARES]
B_FILES = [
    B_FILE_A,
    B_FILE_B,
    B_FILE_C,
    B_FILE_D,
    B_FILE_E,
    B_FILE_F,
    B_FILE_G,
    B_FILE_H,
] = [0x0101010101010101 << i for i in range(8)]

B_RANKS = [
    B_RANK_1,
    B_RANK_2,
    B_RANK_3,
    B_RANK_4,
    B_RANK_5,
    B_RANK_6,
    B_RANK_7,
    B_RANK_8,
] = [0xFF << (8 * i) for i in range(8)]


class Piece:
    def __init__(self, type, color):
        self.type = type
        self.color = color

    @property
    def symbol(self):
        symbol = PIECE_SYMBOLS[self.type]
        return symbol.upper() if self.color else symbol

    @classmethod
    def from_symbol(cls, symbol):
        type = PIECE_SYMBOLS.index(symbol.lower())
        color = symbol.isupper()
        return cls(type, color)

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return str(self.symbol)


class Move:
    def __init__(self, from_square=None, to_square=None):
        self.from_square = from_square
        self.to_square = to_square

    def uci(self):
        return SQUARE_NAMES[self.from_square] + SQUARE_NAMES[self.to_square]

    def __str__(self):
        return self.uci()

    def __repr__(self):
        return self.__str__()


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

    def clear(self):
        self.pawns = B_EMPTY
        self.knights = B_EMPTY
        self.bishops = B_EMPTY
        self.rooks = B_EMPTY
        self.queens = B_EMPTY
        self.kings = B_EMPTY
        self.castling = B_EMPTY

        self.occupied = B_EMPTY
        self.occupied_color = [B_EMPTY, B_EMPTY]

    def set_piece_on(self, piece, square):
        type, color = piece.type, piece.color
        square_mask = B_SQUARES[square]
        if type == PAWN:
            self.pawns |= square_mask
        elif type == KNIGHT:
            self.knights |= square_mask
        elif type == BISHOP:
            self.bishops |= square_mask
        elif type == ROOK:
            self.rooks |= square_mask
        elif type == QUEEN:
            self.queens |= square_mask
        elif type == KING:
            self.kings |= square_mask

        self.occupied |= square_mask
        self.occupied_color[color] |= square_mask

    def piece_on(self, square):
        type = self._type_on(square)
        if type:
            color = self._color_on(square)
            return Piece(type, color)
        else:
            return None

    def _type_on(self, square):
        square_mask = B_SQUARES[square]
        if not self.occupied & square_mask:
            return None
        elif self.pawns & square_mask:
            return PAWN
        elif self.knights & square_mask:
            return KNIGHT
        elif self.bishops & square_mask:
            return BISHOP
        elif self.rooks & square_mask:
            return ROOK
        elif self.queens & square_mask:
            return QUEEN
        else:
            return KING

    def _color_on(self, square):
        square_mask = B_SQUARES[square]
        if self.occupied_color[WHITE] & square_mask:
            return WHITE
        elif self.occupied_color[BLACK] & square_mask:
            return BLACK
        else:
            return None

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
        self.clear()
        board, turn, castling, en_passant, half_move, full_move = value.split()
        self.board_fen = board
        self.turn_fen = turn
        self.castling_fen = castling
        self.en_passant_fen = en_passant
        self.half_move_fen = half_move
        self.full_move_fen = full_move

    def moves(self):
        """Generate all possible moves from this position"""
        yield from self._pawn_moves()

    def scan(self, bitboard):
        while bitboard:
            square = bitboard.bit_length() - 1
            yield square
            bitboard ^= B_SQUARES[square]

    def _pawn_moves(self):
        pawns = self.pawns & self.occupied_color[self.turn]
        # If we don't have any pawns, just skip.
        if not pawns:
            return

        # Figure out where the pawns would jump after the move (to_square)
        # Shift squares to find out from_square
        # We can't walk over any piece
        # Double move can only be performed in following cases
        # from 2nd to 4th Rank (white) and
        # from 7th to 5th rank (Black)
        if self.turn:
            single_advance = (pawns << 8) & (~self.occupied)
            double_advance = (pawns << 16) & (~self.occupied) & B_RANK_4
            single_reverse_step, double_reverse_step = -8, -16
        else:
            single_advance = (pawns >> 8) & (~self.occupied)
            double_advance = (pawns >> 16) & (~self.occupied) & B_RANK_5
            single_reverse_step, double_reverse_step = 8, 16

        for to_square in self.scan(single_advance):
            from_square = to_square + single_reverse_step
            yield Move(from_square, to_square)

        for to_square in self.scan(double_advance):
            from_square = to_square + double_reverse_step
            yield Move(from_square, to_square)

    @property
    def board_fen(self):
        rank_fens, rank_squares, blank = [], [], 0
        for square in SQUARES_MIRRORED:
            piece = self.piece_on(square)
            if not piece:
                blank += 1
            else:
                if blank:
                    rank_squares.append(str(blank))
                    blank = 0

                rank_squares.append(piece.symbol)

            if B_SQUARES[square] & B_FILE_H:
                if blank:
                    rank_squares.append(str(blank))
                    blank = 0
                rank_fens.append("".join(rank_squares))
                rank_squares = []

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
        for ii, fen_rank in enumerate(board_fen.split("/")):
            for jj, fen_square in enumerate(_decode_fen_rank(fen_rank)):
                if fen_square:
                    piece = Piece.from_symbol(fen_square)
                    square = SQUARES_MIRRORED[ii * 8 + jj]
                    self.set_piece_on(piece, square)

    @property
    def turn_fen(self):
        return "w" if self.turn else "b"

    @turn_fen.setter
    def turn_fen(self, turn_fen):
        if turn_fen == "w":
            self.turn = WHITE
        else:
            self.turn = BLACK

    @property
    def castling_fen(self):
        flags = []

        for color in COLORS:
            backrank = B_RANK_1 if color else B_RANK_8

            for file, flag in ((B_FILE_H, "k"), (B_FILE_A, "q")):
                if self.castling & backrank & file:
                    flags.append(flag.upper() if color else flag)

        if flags:
            return "".join(flags)
        else:
            return "-"

    @castling_fen.setter
    def castling_fen(self, castling_fen):
        self.castling = B_EMPTY
        if castling_fen == "-":
            return

        for flag in castling_fen:
            color = flag.isupper()
            flag = flag.lower()
            backrank = B_RANK_1 if color else B_RANK_8

            if flag == "q":
                # Queen rook, A file
                self.castling |= B_FILE_A & backrank
            elif flag == "k":
                # King rook, H File
                self.castling |= B_FILE_H & backrank

    @property
    def en_passant_fen(self):
        if self.en_passant is None:
            return "-"
        return SQUARE_NAMES[self.en_passant]

    @en_passant_fen.setter
    def en_passant_fen(self, en_passant_fen):
        if en_passant_fen == "-":
            self.en_passant = None
        else:
            self.en_passant = SQUARE_NAMES.index(en_passant_fen)

    @property
    def half_move_fen(self):
        return str(self.half_move_clock)

    @half_move_fen.setter
    def half_move_fen(self, half_move_fen):
        self.half_move_clock = int(half_move_fen)

    @property
    def full_move_fen(self):
        return str(self.full_move_number)

    @full_move_fen.setter
    def full_move_fen(self, full_move_fen):
        self.full_move_number = int(full_move_fen)
