from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from board import Board
from solver import Solver
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS

board = Board()
solver = Solver(board)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    column = data['column']
    algorithm = data.get('algorithm', 'random')
    board_state = data['board'].split('\n')
    board.board = [list(row) for row in board_state]

    if column != -1:
        board.make_move(column)

    if algorithm == 'random':
        ai_move = solver.get_random_move()
    elif algorithm == 'minimax':
        ai_move = solver.minimax(depth=4, maximizing_player=True)
    elif algorithm == 'alpha-beta':
        ai_move = solver.minimax(depth=4, maximizing_player=True)
    elif algorithm == 'expectiminimax':
        ai_move = solver.expectiminimax(depth=4, maximizing_player=True)
    else:
        ai_move = solver.get_random_move()

    board.make_move(ai_move)
    player_score = board.check_player_score()
    agent_score = board.check_agent_score()
    return jsonify({'board': str(board), 'ai_move': ai_move, 'player_score': player_score, 'agent_score': agent_score})

if __name__ == '__main__':
    app.run(debug=True)