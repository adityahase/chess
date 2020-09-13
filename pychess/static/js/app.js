window.onload = function () {
  const game = new Chess();
  window.game = game;

  function onDragStart(source, piece, position, orientation) {
    // do not pick up pieces if the game is over
    if (game.game_over()) return false;

    // only pick up pieces for the side to move
    if (
      (game.turn() === "w" && piece.search(/^b/) !== -1) ||
      (game.turn() === "b" && piece.search(/^w/) !== -1)
    ) {
      return false;
    }
  }

  function onDrop(source, target) {
    // see if the move is legal
    var move = game.move({
      from: source,
      to: target,
      promotion: "q",
    });

    // illegal move
    if (move === null) return "snapback";

    const player_move = `${source}-${target}`;
    updateStatus();
    fetch_ai_move(player_move);
  }

  function onSnapEnd() {
    board.position(game.fen());
  }

  function updateStatus() {
    var status = "";
    var moveColor = "White";
    if (game.turn() === "b") {
      moveColor = "Black";
    }
    // checkmate?
    if (game.in_checkmate()) {
      status = "Game over, " + moveColor + " is in checkmate.";
    }
    // draw?
    else if (game.in_draw()) {
      status = "Game over, drawn position";
    }
    // game still on
    else {
      status = moveColor + " to move";
      // check?
      if (game.in_check()) {
        status += ", " + moveColor + " is in check";
      }
    }

    $("#game-status").html(status);
    $("#fen-input").val(game.fen());
  }

  const config = {
    draggable: true,
    dropOffBoard: "snapback",
    position: "start",
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
  };
  const board = ChessBoard("chess-board", config);

  $("#newgame").on("click", board.start);

  $("#load-fen").on("click", () => {
    const fen_string = $("#fen-input").val();
    board.position(fen_string);
  });

  function fetch_ai_move(player_move) {
    $.ajax({
      type: "POST",
      url: "/play",
      data: `{ "fen": "${board.fen()}" }`,
      success: function (data) {
        ai_move = data.bestmove;
        ai_move = ai_move.slice(0, 2) + "-" + ai_move.slice(2);
        board.move(ai_move);
        add_move_to_list(player_move, ai_move);
      },
      contentType: "application/json",
      dataType: "json",
    });
  }

  function add_move_to_list(player_move, ai_move) {
    $("#moves-container").append(
      `<div class="flex rounded items-center border-t h-8">
      <p class="flex-1 border-r">${player_move}</p>
      <p class="flex-1">${ai_move}</p>
    </div>`
    );
    $("#moves-container").animate(
      { scrollTop: $("#moves-container").prop("scrollHeight") },
      500
    );
  }
};
