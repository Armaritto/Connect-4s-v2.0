import random
from helper import Helper
from expectiminimax_solver import Expectiminimax_solver
from alpha_beta_minimax import AlphaBetaMinimax

class Solver:
    # The Solver class is responsible for choosing the best move for the AI player
    def __init__(self, board):
        self.board = board
        self.helper = Helper()
        self.expectiminimax_solver = Expectiminimax_solver()
        self.ab_minimax_solver = AlphaBetaMinimax()

    def minimax(self, depth, maximizing):   #
        if maximizing:  # if maximizing, the AI player is the maximizing player
            child,_ = self.helper.maximize(depth, self.board.board, None)
        else:   # if minimizing, the human player is the minimizing player
            child,_ = self.helper.minimize(depth, self.board.board, None)

        # render the tree trace
        self.helper.dot.render('tree_trace', format='svg', cleanup=True)

        # find the best move
        best_move = None
        for i in range(6):
            for j in range(7):
                if self.board.board[i][j] != child[i][j]:
                    best_move = j
                    break
        return best_move

    def expectiminimax(self, depth, maximizing):
        if maximizing:  # if maximizing, the AI player is the maximizing player
            chosen_move,_ = self.expectiminimax_solver.maximize(depth, self.board.board, None)
        else:   # if minimizing, the human player is the minimizing player
            chosen_move,_ = self.expectiminimax_solver.minimize(depth, self.board.board, None)

        # render the tree trace
        self.expectiminimax_solver.dot.render('tree_trace', format='svg', cleanup=True)

        # find the best move
        moves = []
        for col in [chosen_move, chosen_move-1, chosen_move+1]:
            if 0 <= col <= 6:
                if self.board.board[0][col] == 'E':
                    moves.append(col)
        
        # max chooses the move and lets chance decide the state
        weight = 3
        samples = []
        for move in moves:
            for i in range(weight):
                samples.append(move)
            weight = 1
        random_move = random.choice(samples)
        
        return random_move

    def minimax_with_alpha_beta(self, depth, maximizing):
        if maximizing:  # if maximizing, the AI player is the maximizing player
            child, _ = self.ab_minimax_solver.maximize(depth, self.board.board, float('-inf'), float('inf'), None)
        else:       # if minimizing, the human player is the minimizing player
            child, _ = self.ab_minimax_solver.minimize(depth, self.board.board, float('-inf'), float('inf'), None)

        # render the tree trace
        self.ab_minimax_solver.helper.dot.render('tree_trace', format='svg', cleanup=True)

        # find the best move
        best_move = None
        for i in range(6):
            for j in range(7):
                if self.board.board[i][j] != child[i][j]:
                    best_move = j
                    break
        return best_move

    def get_random_move(self):      # if the AI player cannot find a winning move, it will choose a random move
        valid_columns = [col for col in range(7) if self.board.board[0][col] == 'E']
        return random.choice(valid_columns)