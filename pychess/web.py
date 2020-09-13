from flask import Flask, request, render_template
from flask.json import jsonify

import chess
from chess.engine import SimpleEngine

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/play", methods=["POST"])
def play():
    data = request.get_json(force=True)
    engine = SimpleEngine.popen_uci(data.get("engine", "chesscli"))
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
                "depth": result.info.get("depth"),
                "seldepth": result.info.get("seldepth"),
                "multipv": result.info.get("multipv"),
                "nodes": result.info.get("nodes"),
                "nps": result.info.get("nps"),
                "time": result.info.get("time"),
                "tbhits": result.info.get("tbhits"),
                "pv": [str(pv) for pv in result.info.get("pv", [])],
            },
        }
    )
