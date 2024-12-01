from board import Board

class Expectiminimax_solver:
    def __init__(self):
        self.board = Board()
        pass

    def get_max_min_children(self, board_state):
        children = []
        for col in range(7):
            if board_state[0][col] == 'E':
                children.append(col)
        return children
    
    def get_chance_children(self, board_state, desired_move):
        children = []
        for col in [desired_move, desired_move-1, desired_move+1]:
            if 0 <= col <= 6:
                if board_state[0][col] == 'E':
                    child = [list(row) for row in board_state]
                    for row in reversed(child):
                        if row[col] == 'E':
                            row[col] = self.board.current_player
                            if  self.board.current_player == 'X':
                                self.board.current_player = 'O'
                            else:
                                self.board.current_player = 'X'
                            children.append(child)
                            break
        return children

    def maximize(self, depth, board_state):
        if self.board.is_full() or depth < 1:
            return board_state, self.heuristic(board_state)

        max_child, max_utility = None, float('-inf')

        for child in self.get_max_min_children(board_state):
            utility = self.chance_node(depth - 1, board_state, child, True)

            if utility > max_utility:
                max_child, max_utility = child, utility

        return max_child, max_utility
    
    def minimize(self, depth, board_state):
        if self.board.is_full() or depth < 1:
            return board_state, self.heuristic(board_state)

        min_child, min_utility = None, float('inf')

        for child in self.get_max_min_children(board_state):
            utility = self.chance_node(depth - 1, board_state, child, False)

            if utility < min_utility:
                min_child, min_utility = child, utility

        return min_child, min_utility

    
    def chance_node(self, depth, board_state, desired_move, is_parent_max):
        expected_utility = 0
        weight = 3
        weigth_sum = 0
        for child in self.get_chance_children(board_state, desired_move):
            weigth_sum += weight
            weight = 1
            if is_parent_max:
                _, utility = self.minimize(depth-1, child) 
            else: 
                _, utility = self.maximize(depth-1, child) 
            expected_utility += weight * utility
        return expected_utility/weigth_sum


    def heuristic(self, board_state):
        return self.board.check_agent_score() - self.board.check_player_score()