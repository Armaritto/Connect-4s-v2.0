from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from board import Board
from solver import Solver
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS

board = Board()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')
@app.route('/script.js')
def script():
    return send_from_directory(app.static_folder, 'script.js')
@app.route('/styles.css')
def style():
    return send_from_directory(app.static_folder, 'styles.css')

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    column = data['column']
    algorithm = data.get('algorithm', 'random')
    board_state = data['board'].split('\n')
    board.board = [list(row) for row in board_state]
    solver = Solver(board)

    if column != -1:
        board.make_move(column)

    ai_move = None
    trace = ""

    if algorithm == 'random':
        ai_move = solver.get_random_move()
        trace = "Random move selected."
    elif algorithm == 'minimax':
        ai_move = solver.minimax(depth=3, maximizing=True)  # maximize ai score
    elif algorithm == 'alpha-beta':
        ai_move, trace = solver.minimax_with_alpha_beta(depth=2, maximizing=True, current_player='X')
    elif algorithm == 'expectiminimax':
        ai_move, trace = solver.expectiminimax(depth=4, maximizing=True)
    else:
        ai_move = solver.get_random_move()
        trace = "Random move selected."

    if ai_move is not None:
        board.make_move(ai_move)

    player_score = board.check_player_score()
    agent_score = board.check_agent_score()
    return jsonify({'board': str(board), 'ai_move': ai_move, 'player_score': player_score, 'agent_score': agent_score, 'trace': trace})

if __name__ == '__main__':
    app.run(debug=True)