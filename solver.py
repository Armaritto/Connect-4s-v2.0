import random
from helper import Helper

class Solver:
    def __init__(self, board):
        self.board = board
        self.helper = Helper()

    def minimax(self, depth, maximizing):
        if maximizing:
            return self.helper.maximize(depth, self.board.board)
        else:
            return self.helper.minimize(depth, self.board.board)

    def expectiminimax(self, depth, maximizing):
        # Implement the expectiminimax algorithm
        pass

    def minimax_with_alpha_beta(self, depth, maximizing):
        # Implement the minimax algorithm with alpha-beta pruning
        pass

    def get_random_move(self):
        valid_columns = [col for col in range(7) if self.board.board[0][col] == 'E']
        return random.choice(valid_columns)