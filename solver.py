import random
from helper import Helper
from expectiminimax_solver import Expectiminimax_solver

class Solver:
    def __init__(self, board):
        self.board = board
        self.helper = Helper()
        self.expectiminimax_solver = Expectiminimax_solver()

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
        if maximizing:
            chosen_move,_ = self.expectiminimax_solver.maximize(depth, self.board.board)
        else:
            chosen_move,_ = self.expectiminimax_solver.minimize(depth, self.board.board)

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
        # Implement the minimax algorithm with alpha-beta pruning
        pass

    def get_random_move(self):
        valid_columns = [col for col in range(7) if self.board.board[0][col] == 'E']
        return random.choice(valid_columns)