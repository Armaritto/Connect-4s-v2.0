from board import Board

class AlphaBetaMinimax:
    def __init__(self):
        self.board = Board()
        pass

    def maximize(self, depth, board_state, alpha, beta):
        if self.board.is_full() or depth == 0:
            return board_state, self.heuristic(board_state)

        max_child, max_utility = None, float('-inf')

        for child in self.board.get_children(board_state):
            _, utility = self.minimize(depth - 1, child, alpha, beta)

            if utility > max_utility:
                max_child, max_utility = child, utility

            if max_utility >= beta:
                break

            if max_utility > alpha:
                alpha = max_utility

        return max_child, max_utility

    def minimize(self, depth, board_state, alpha, beta):
        if self.board.is_full() or depth == 0:
            return board_state, self.heuristic(board_state)

        min_child, min_utility = None, float('inf')

        for child in self.board.get_children(board_state):
            _, utility = self.maximize(depth - 1, child, alpha, beta)

            if utility < min_utility:
                min_child, min_utility = child, utility

            if min_utility <= alpha:
                break

            if min_utility < beta:
                beta = min_utility

        return min_child, min_utility

    def heuristic_helper(self, player): #INCOMPLETE
        potential_score = 0
        for row in self.board.board:
            #check for possible scores in each row, if there are possible 4 in a row, increment the potential score
            for i in range(4):
                pot_horizontal = 0
                for j in range(4):
                    if row[i + j] == player or row[i + j] == 'E':
                        pot_horizontal += 1
                potential_score += pot_horizontal
        for col in range(7):
            for i in range(3):
                if [self.board.board[i + j][col] for j in range(4)] == [player] * 4:
                    potential_score += 1
        for i in range(3):
            for j in range(4):
                if [self.board.board[i + k][j + k] for k in range(4)] == [player] * 4:
                    potential_score += 1
                if [self.board.board[i + k][j + 3 - k] for k in range(4)] == [player] * 4:
                    potential_score += 1

    def heuristic(self, board_state):

        #calculate the difference between the agent's and the player's actual scores
        h_current = self.board.check_agent_score() - self.board.check_player_score()

        #calculate the difference between the agent's and the player's potential scores


