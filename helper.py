from board import Board

class Helper:
    def __init__(self):
        self.board = Board()
        pass

    def maximize(self, depth, board_state):
        if self.board.is_full() or depth == 0:
            return board_state, self.heuristic(board_state)

        max_child, max_utility = None, float('-inf')

        for child in self.board.get_children(board_state):
            _, utility = self.minimize(depth - 1, child)

            if utility > max_utility:
                max_child, max_utility = child, utility

        return max_child, max_utility

    def minimize(self, depth, board_state):
        if self.board.is_full() or depth == 0:
            return board_state, self.heuristic(board_state)

        min_child, min_utility = None, float('inf')

        for child in self.board.get_children(board_state):
            _, utility = self.maximize(depth - 1, child)

            if utility < min_utility:
                min_child, min_utility = child, utility

        return min_child, min_utility

    def heuristic(self, board_state):
        return self.board.check_agent_score() - self.board.check_player_score()