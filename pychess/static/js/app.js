window.onload = function () {
  const config = {
    draggable: true,
    dropOffBoard: "snapback",
    onDragStart: onDragStart,
    onDrop: onDrop,
  };
  const board = ChessBoard("chess-board", config);
  let player = "w";

  $("#newgame").on("click", board.start);

  $("#load-fen").on("click", () => {
    const fen_string = $("#fen-input").val();
    board.position(fen_string);
  });

  function onDragStart(source, piece, position, orientation) {
    return piece[0] == player;
  }

  async function onDrop(source, target, piece, newPos, oldPos, orientation) {
    player = piece[0] == "w" ? "b" : "w";
    const player_move = `${source}-${target}`;
    let computer_move = "";

    // post req to get best move

    add_to_move_list(player_move, computer_move);
  }
};

function add_to_move_list(player_move, computer_move) {
  $("#moves-container").append(
    `<div class="flex rounded items-center border-t h-8">
      <p class="flex-1 border-r">${player_move}</p>
      <p class="flex-1">${computer_move}</p>
    </div>`
  );
  $("#moves-container").animate(
    { scrollTop: $("#moves-container").prop("scrollHeight") },
    500
  );
}
