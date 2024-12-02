from board import Board
from digraph_factory import Digraph_factory
from helper import Helper

class Expectiminimax_solver:
    def __init__(self, k):
        self.board = Board()
        self.factory = Digraph_factory()
        self.dot = self.factory.create_digraph("expectiminimax", k)
        self.helper = Helper(k)
        self.node_counter = 0
        pass

    def board_to_string(self, board_state):
        if board_state is None:
            return "No valid moves"
        return '\n'.join([''.join(row) for row in board_state])
    
    def add_node(self, node_id, label):
        self.dot.node(node_id, label)

    def add_edge(self, parent_id, child_id):
        self.dot.edge(parent_id, child_id)

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
                            children.append(child)
                            break
        return children

    def maximize(self, depth, board_state, parent_id):
        if self.board.is_full() or depth < 1:
            node_id = str(self.node_counter)
            self.node_counter += 1
            utility = self.heuristic(board_state)
            label = f'Leaf: Depth {depth}, Utility: {utility} \n{self.board_to_string(board_state)}'
            self.add_node(node_id, label)
            self.add_edge(parent_id, node_id)

            return board_state, utility
           
        node_id = str(self.node_counter)
        self.node_counter += 1
        label = " "
        
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        max_child, max_utility = None, float('-inf')

        for child in self.get_max_min_children(board_state):
            utility = self.chance_node(depth - 1, board_state, child, True, node_id)

            if utility > max_utility:
                max_child, max_utility = child, utility

        label = f'Maximize: Depth {depth}, Utility: {max_utility:.4f} \n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)

        return max_child, max_utility
    
    def minimize(self, depth, board_state, parent_id):
        if self.board.is_full() or depth < 1:
            node_id = str(self.node_counter)
            self.node_counter += 1
            utility = self.heuristic(board_state)
            label = f'Leaf: Depth {depth}, Utility: {utility} \n{self.board_to_string(board_state)}'
            self.add_node(node_id, label)
            self.add_edge(parent_id, node_id)

            return board_state, utility
        
        node_id = str(self.node_counter)
        self.node_counter += 1
        label = " "
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        min_child, min_utility = None, float('inf')

        for child in self.get_max_min_children(board_state):
            utility = self.chance_node(depth - 1, board_state, child, False, node_id)

            if utility < min_utility:
                min_child, min_utility = child, utility

        label = f'Minimize: Depth {depth}, Utility:{min_utility:.4f} \n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)

        return min_child, min_utility

    
    def chance_node(self, depth, board_state, desired_move, is_parent_max, parent_id):
        if is_parent_max:
            self.board.current_player = 'O'
        else:
            self.board.current_player = 'X'
        node_id = str(self.node_counter)
        self.node_counter += 1
        label = " "
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        expected_utility = 0
        weight = 3
        weigth_sum = 0
        for child in self.get_chance_children(board_state, desired_move):
            if is_parent_max:
                _, utility = self.minimize(depth-1, child, node_id) 
            else: 
                _, utility = self.maximize(depth-1, child, node_id) 
            expected_utility += weight * utility
            weigth_sum += weight
            weight = 1
            
        expected_utility = expected_utility/weigth_sum

        label = f'Chance: Depth {depth}, Utility:{expected_utility:.4f}'
        self.add_node(node_id, label)
        return expected_utility


    def heuristic(self, board_state):
        return self.helper.heuristic(board_state)