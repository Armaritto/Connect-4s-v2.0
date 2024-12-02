from board import Board

class AlphaBetaMinimax:
    def __init__(self, board):
        self.board = board
        pass

    def maximize(self, depth, board_state, alpha, beta, indent=0):
        if self.board.is_full() or depth == 0:
            utility = self.heuristic(board_state)
            print(f"{' ' * indent}Maximize: Depth {depth}, Utility {utility}, State:\n{board_state}")
            return board_state, utility

        max_child, max_utility = None, float('-inf')

        for child in self.board.get_children(board_state):
            _, utility = self.minimize(depth - 1, child, alpha, beta, indent + 2)

            if utility > max_utility:
                max_child, max_utility = child, utility

            if max_utility >= beta:
                break

            if max_utility > alpha:
                alpha = max_utility

        print(f"{' ' * indent}Maximize: Depth {depth}, Utility {max_utility}, State:\n{board_state}")
        return max_child, max_utility

    def minimize(self, depth, board_state, alpha, beta, indent=0):
        if self.board.is_full() or depth == 0:
            utility = self.heuristic(board_state)
            print(f"{' ' * indent}Minimize: Depth {depth}, Utility {utility}, State:\n{board_state}")
            return board_state, utility

        min_child, min_utility = None, float('inf')

        for child in self.board.get_children(board_state):
            _, utility = self.maximize(depth - 1, child, alpha, beta, indent + 2)

            if utility < min_utility:
                min_child, min_utility = child, utility

            if min_utility <= alpha:
                break

            if min_utility < beta:
                beta = min_utility

        print(f"{' ' * indent}Minimize: Depth {depth}, Utility {min_utility}, State:\n{board_state}")
        return min_child, min_utility

    def heuristic_helper(self, player, board_state):
        pot_horizontal = 0
        pot_vertical = 0
        pot_diagonal = 0
        # move a window of 4 over the row, column, or diagonal if the window contains a token that is not the player or an empty space, don't increment the potential score, otherwise increment
        #Horizontal
        for row in board_state:
           for i in range(len(row) - 3):
                window = row[i:i + 4]
                if all(cell == player or cell == 'E' for cell in window):
                    pot_horizontal += 1

        #Vertical
        for col in range(7):
            for i in range(3):
                window = [board_state[i + j][col] for j in range(4)]
                if all(cell == player or cell == 'E' for cell in window):
                    pot_vertical += 1

        #Diagonal
        for i in range(3):
            for j in range(4):
                #positive slope
                window = [board_state[i + k][j + k] for k in range(4)]
                if all(cell == player or cell == 'E' for cell in window):
                    pot_diagonal += 1
                #negative slope
                window = [board_state[i + k][j + 3 - k] for k in range(4)]
                if all(cell == player or cell == 'E' for cell in window):
                    pot_diagonal += 1

        return pot_horizontal + pot_vertical + pot_diagonal

    def heuristic(self, board_state):

        #calculate the difference between the agent's and the player's actual scores
        h_current = self.board.check_agent_score() - self.board.check_player_score()

        #calculate the difference between the agent's and the player's potential scores
        h_potential = self.heuristic_helper('O', board_state) - self.heuristic_helper('X', board_state)

        return h_current + h_potential


