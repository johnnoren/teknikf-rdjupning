import chess
import chess.pgn
from openai import OpenAI


def get_legal_moves(board):
    return list(map(board.san, board.legal_moves))


def init_game() -> tuple[chess.pgn.Game, chess.Board]:
    board = chess.Board()
    game = chess.pgn.Game()
    game.headers["White"], game.headers["Black"] = "User", "ChatGPT"

    for header in ["Event", "Date", "Site", "Round"]:
        del game.headers[header]

    game.setup(board)
    return game, board


def generate_prompt(game: chess.pgn.Game, board: chess.Board) -> str:
    legal_moves = get_legal_moves(board)
    legal_moves_string = ",".join(legal_moves)
    return f"""You are a chess engine playing a chess match against the user as black and trying to win. The current PGN is:
    {str(game)}

    The current FEN notation is:
    {board.fen()}

    The valid moves are:
    {legal_moves_string}

    Pick a move from the list above that maximizes your chance of winning. Even if you think you can't win still pick a valid move using the following format:

    Move: e5"""


def get_move_from_prompt(prompt: str, client: OpenAI) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    line_containing_move = response.choices[0].message.content
    move = line_containing_move[6:]
    return move


def print_board(board):
    print(board)
    print(game)
    print(board.fen())
    print(get_legal_moves(board))


def try_moving(move: str, board: chess.Board):
    try:
        board.push_san(move)
    except ValueError:
        print("Invalid move")
        return False
    return True


game, board = init_game()
client = OpenAI()
while not board.is_game_over():
    if board.turn == chess.WHITE:
        print_board(board)
        move = input("Enter your move: ")
        moved_successfully = try_moving(move, board)
        if moved_successfully:
            game = game.add_variation(board.move_stack[-1])
            print(game, file=open("out.pgn", "w"), end="\n\n")
    else:
        prompt = generate_prompt(game, board)
        move = get_move_from_prompt(prompt, client)
        moved_successfully = try_moving(move, board)
        if moved_successfully:
            game = game.add_variation(board.move_stack[-1])
            print(game, file=open("out.pgn", "w"), end="\n\n")
        print(f"ChatGPT played {move}")
