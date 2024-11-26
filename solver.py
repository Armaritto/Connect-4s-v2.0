import random

class Solver:
    def __init__(self, board):
        self.board = board

    def minimax(self, depth, alpha, beta, maximizing_player):
        # Implement the minimax algorithm with alpha-beta pruning
        pass

    def expectiminimax(self, depth, maximizing_player):
        # Implement the expectiminimax algorithm
        pass

    def get_best_move(self):
        # Determine the best move using one of the algorithms
        pass

    def get_random_move(self):
        valid_columns = [col for col in range(7) if self.board.board[0][col] == 'E']
        return random.choice(valid_columns)