import random
from helper import Helper
from alpha_beta_minimax import AlphaBetaMinimax
from expectiminimax_solver import Expectiminimax_solver

class Solver:
    def __init__(self, board):
        self.board = board
        self.helper = Helper()
        self.expectiminimax_solver = Expectiminimax_solver()

    def minimax(self, depth, maximizing):
        if maximizing:
            child,_ = self.helper.maximize(depth, self.board.board, None)
        else:
            child,_ = self.helper.minimize(depth, self.board.board, None)

        self.helper.dot.render('tree_trace', format='svg', cleanup=True)

        best_move = None
        for i in range(6):
            for j in range(7):
                if self.board.board[i][j] != child[i][j]:
                    best_move = j
                    break
        return best_move

    def expectiminimax(self, depth, maximizing):
        if maximizing:
            chosen_move,_ = self.expectiminimax_solver.maximize(depth, self.board.board, None)
        else:
            chosen_move,_ = self.expectiminimax_solver.minimize(depth, self.board.board, None)

        self.expectiminimax_solver.dot.render('tree_trace', format='svg', cleanup=True)

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

    def minimax_with_alpha_beta(self, depth, maximizing, current_player):
        ab_minimax = AlphaBetaMinimax(self.board)

        if maximizing:
            child, _, root_id = ab_minimax.maximize(depth, self.board.board, float('-inf'), float('inf'), current_player)
        else:
            child, _, root_id = ab_minimax.minimize(depth, self.board.board, float('-inf'), float('inf'), current_player)

        best_move = None
        for i in range(6):
            for j in range(7):
                if self.board.board[i][j] != child[i][j]:
                    best_move = j
                    break
            if best_move is not None:
                break

        ab_minimax.dot.render('tree_trace', format='png', cleanup=True)
        return best_move, root_id

    def get_random_move(self):
        valid_columns = [col for col in range(7) if self.board.board[0][col] == 'E']
        return random.choice(valid_columns)