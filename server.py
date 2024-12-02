import time

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from board import Board
from solver import Solver
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS

board = Board()
nodes_expanded = 0
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
    global nodes_expanded
    data = request.json
    column = data['column']
    algorithm = data.get('algorithm', 'random')
    k = int(data.get('k', 5))  # Default to 5 if not provided
    board_state = data['board'].split('\n')
    board.board = [list(row) for row in board_state]
    solver = Solver(board, k)

    if column != -1:
        if algorithm == 'expectiminimax':
            board.make_move_with_chance(column)
        else:
            board.make_move(column)
    start_time = time.time()
    if algorithm == 'random':
        ai_move = solver.get_random_move()
    elif algorithm == 'minimax':
        ai_move, nodes_expanded = solver.minimax(maximizing =  True)
    elif algorithm == 'alpha-beta':
        ai_move, nodes_expanded  = solver.minimax_with_alpha_beta(maximizing =  True)
    elif algorithm == 'expectiminimax':
        ai_move, nodes_expanded = solver.expectiminimax(maximizing =  True)
    else:
        ai_move = solver.get_random_move()
    end_time = time.time()
    time_taken = end_time - start_time
    if ai_move is not None:
        board.make_move(ai_move)
    player_score = board.check_player_score()
    agent_score = board.check_agent_score()
    return jsonify({'board': str(board), 'ai_move': ai_move, 'player_score': player_score, 'agent_score': agent_score, 'nodes_expanded': nodes_expanded, 'time_taken': time_taken})

if __name__ == '__main__':
    app.run(debug=True)