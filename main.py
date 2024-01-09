from openai import OpenAI
client = OpenAI()

list_of_pieces = """
List of pieces:
White King: Ke1
White Queen: Qd1
White Rooks: Ra1, Rh1
White Knights: Nb1, Ng1
White Bishops: Bc1, Bf1
White Pawns: a2, b2, c2, d2, e2, f2, g2, h2
Black King: ke8
Black Queen: qd8
Black Rooks: ra8, rh8
Black Knights: nb8, ng8
Black Bishops: bc8, bf8
Black Pawns: a7, b7, c7, d7, e7, f7, g7, h7
"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system",
          "content": "You are a chess-playing assistant designed to play black. Your task is to output your next move in JSON format. When you receive the positions of the pieces, please provide the next move using algebraic chess notation and return it as a JSON object. The JSON should include two fields: 'from' (representing the starting square of the move) and 'to' (representing the destination square of the move). Ensure that the JSON output is well-structured and easily understandable. Ensure that the move is aligned with the rules of chess."},
        {"role": "user", "content": list_of_pieces},
    ]
)
print(response.choices[0].message.content)
