import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Define constants for the players
PLAYER_1 = "o"  # Player1 is what the AI will play as
PLAYER_2 = "x"
EMPTY = ""

# Function to check if the game is over
def game_over(board):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return True
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return True
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return True
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return True

    # Check for a draw
    for row in board:
        if EMPTY in row:
            return False
    return True

# Function to evaluate the board
def evaluate(board):
    # Check for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == PLAYER_1:
            return 1
        if board[0][i] == board[1][i] == board[2][i] == PLAYER_1:
            return 1
    if board[0][0] == board[1][1] == board[2][2] == PLAYER_1:
        return 1
    if board[0][2] == board[1][1] == board[2][0] == PLAYER_1:
        return 1

    # Check for a loss
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == PLAYER_2:
            return -1
        if board[0][i] == board[1][i] == board[2][i] == PLAYER_2:
            return -1
    if board[0][0] == board[1][1] == board[2][2] == PLAYER_2:
        return -1
    if board[0][2] == board[1][1] == board[2][0] == PLAYER_2:
        return -1

    # Game is ongoing or a draw
    return 0

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    score = evaluate(board)

    # Base case: Game over or depth limit reached
    if score == 1:
        return 1
    if score == -1:
        return -1
    if game_over(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_1
                    score = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_2
                    score = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score

# Function to find the best move using Minimax
def find_best_move(board):
    best_score = -float("inf")
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_1
                score = minimax(board, 0, False)
                board[i][j] = EMPTY

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

def coordinates_to_number(x, y, grid_width):
    return x * grid_width + y


def return_best_move(input_board):
    board = [input_board[i:i + 3] for i in range(0, len(input_board), 3)]
    print("AI is thinking...")
    ai_move = find_best_move(board)
    print(f"Co-ord : {ai_move}")
    return coordinates_to_number(ai_move[0], ai_move[1], 3)


# @app.route is a decorator that turns a regular Python function into a Flask view function which converts the
# function’s return value into an HTTP response to be displayed by an HTTP client, such as a web browser
@app.route('/', methods=['POST'])
@cross_origin()
def index():
    record = json.loads(request.data)

    if record["currentPlayer"] == 'x':
        inverse_board = ['o' if char == 'x' else 'x' if char == 'o' else char for char in record["board"]]
        record["board"] = inverse_board

    return json.dumps({'optimalMoveIndex': return_best_move(record["board"])})


if __name__ == "__main__":
    app.run(debug=True, port=int(5000))