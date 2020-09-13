from flask import Flask, request
from flask.json import jsonify

import chess
from chess.engine import SimpleEngine

app = Flask(__name__)

STOCKFISH = "stockfish"


@app.route("/", methods=["POST"])
def play():
    data = request.get_json(force=True)
    engine = SimpleEngine.popen_uci(STOCKFISH)
    board = chess.Board(data["fen"])

    result = engine.play(
        board, limit=chess.engine.Limit(time=0.5), info=chess.engine.INFO_ALL
    )
    return jsonify(
        {
            "bestmove": str(result.move),
            "ponder": str(result.ponder),
            "resigned": str(result.resigned),
            "draw_offered": str(result.draw_offered),
            "info": {
                "depth": result.info["depth"],
                "seldepth": result.info["seldepth"],
                "multipv": result.info["multipv"],
                "nodes": result.info["nodes"],
                "nps": result.info["nps"],
                "time": result.info["time"],
                "tbhits": result.info["tbhits"],
                "pv": [str(pv) for pv in result.info["pv"]],
            },
        }
    )
