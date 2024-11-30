import random
from helper import Helper
from alpha_beta_minimax import AlphaBetaMinimax

class Solver:
    def __init__(self, board):
        self.board = board
        self.helper = Helper()

    def minimax(self, depth, maximizing):
        if maximizing:
            child,_ = self.helper.maximize(depth, self.board.board)
        else:
            child,_ = self.helper.minimize(depth, self.board.board)

        best_move = None
        for i in range(6):
            for j in range(7):
                if self.board.board[i][j] != child[i][j]:
                    best_move = j
                    break
        return best_move

    def expectiminimax(self, depth, maximizing):
        # Implement the expectiminimax algorithm
        pass

    def minimax_with_alpha_beta(self, depth, maximizing):
        ab_minimax = AlphaBetaMinimax()
        if maximizing:
            child, _ = ab_minimax.maximize(depth, self.board.board, float('-inf'), float('inf'))
        else:
            child, _ = ab_minimax.minimize(depth, self.board.board, float('-inf'), float('inf'))

    def get_random_move(self):
        valid_columns = [col for col in range(7) if self.board.board[0][col] == 'E']
        return random.choice(valid_columns)