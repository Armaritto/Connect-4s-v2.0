import random
from helper import Helper
from expectiminimax_solver import Expectiminimax_solver
from alpha_beta_minimax import AlphaBetaMinimax

class Solver:

    def __init__(self, board, k):
        self.board = board
        self.k = k
        self.helper = Helper(k)
        self.expectiminimax_solver = Expectiminimax_solver(k)
        self.ab_minimax_solver = AlphaBetaMinimax(k)

    def minimax(self,  maximizing):
        if maximizing:
            child,_ = self.helper.maximize(self.k, self.board.board, None)
        else:
            child,_ = self.helper.minimize(self.k, self.board.board, None)

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


    def expectiminimax(self, maximizing):
        if maximizing:
            chosen_move,_ = self.expectiminimax_solver.maximize(self.k, self.board.board, None)
        else:
            chosen_move,_ = self.expectiminimax_solver.minimize(self.k, self.board.board, None)


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
        print("samples ai:     " + str(samples))
        return random_move


    def minimax_with_alpha_beta(self, maximizing):
        if maximizing:
            child, _ = self.ab_minimax_solver.maximize(self.k, self.board.board, float('-inf'), float('inf'), None)
        else:
            child, _ = self.ab_minimax_solver.minimize(self.k, self.board.board, float('-inf'), float('inf'), None)


        # render the tree trace
        self.ab_minimax_solver.dot.render('tree_trace', format='svg', cleanup=True)

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