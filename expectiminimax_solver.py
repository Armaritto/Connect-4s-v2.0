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
        return '\n'.join([''.join(row) for row in board_state])  # Convert board state to string

    def add_node(self, node_id, label):
        self.dot.node(node_id, label)  # Add a node to the graph

    def add_edge(self, parent_id, child_id):
        self.dot.edge(parent_id, child_id)  # Add an edge to the graph

    def get_max_min_children(self, board_state):
        children = []
        for col in range(7):
            if board_state[0][col] == 'E':  # Check if the column is not full
                children.append(col)
        return children  # Return list of valid columns

    def get_chance_children(self, board_state, desired_move):
        children = []
        for col in [desired_move, desired_move-1, desired_move+1]:  # Consider desired move and adjacent columns
            if 0 <= col <= 6:
                if board_state[0][col] == 'E':  # Check if the column is not full
                    child = [list(row) for row in board_state]  # Copy the board state
                    for row in reversed(child):
                        if row[col] == 'E':  # Find the first empty cell in the column
                            row[col] = self.board.current_player  # Place the current player's token
                            children.append(child)  # Add the new board state to children
                            break
        return children  # Return list of possible board states

    def maximize(self, depth, board_state, parent_id):
        if self.board.is_full(board_state) or depth < 1:  # Terminal state check
            node_id = str(self.node_counter)
            self.node_counter += 1
            utility = self.heuristic(board_state)  # Evaluate the board state
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

        max_child, max_utility = None, float('-inf')  # Initialize max utility

        for child in self.get_max_min_children(board_state):  # Iterate over valid moves
            utility = self.chance_node(depth - 1, board_state, child, True, node_id)  # Evaluate chance node

            if utility > max_utility:  # Update max utility
                max_child, max_utility = child, utility

        label = f'Maximize: Depth {depth}, Utility: {max_utility:.4f} \n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)
        return max_child, max_utility

    def minimize(self, depth, board_state, parent_id):
        if self.board.is_full(board_state) or depth < 1:  # Terminal state check
            node_id = str(self.node_counter)
            self.node_counter += 1
            utility = self.heuristic(board_state)  # Evaluate the board state
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

        min_child, min_utility = None, float('inf')  # Initialize min utility

        for child in self.get_max_min_children(board_state):  # Iterate over valid moves
            utility = self.chance_node(depth - 1, board_state, child, False, node_id)  # Evaluate chance node

            if utility < min_utility:  # Update min utility
                min_child, min_utility = child, utility

        label = f'Minimize: Depth {depth}, Utility:{min_utility:.4f} \n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)
        return min_child, min_utility

    def chance_node(self, depth, board_state, desired_move, is_parent_max, parent_id):
        if is_parent_max:
            self.board.current_player = 'O'  # Set current player to AI
        else:
            self.board.current_player = 'X'  # Set current player to human

        node_id = str(self.node_counter)
        self.node_counter += 1
        label = " "
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        expected_utility = 0
        weight = 3  # Initial weight for desired move
        weight_sum = 0

        for child in self.get_chance_children(board_state, desired_move):  # Iterate over possible outcomes
            if is_parent_max:
                _, utility = self.minimize(depth-1, child, node_id)  # Evaluate minimize node
            else:
                _, utility = self.maximize(depth-1, child, node_id)  # Evaluate maximize node
            expected_utility += weight * utility  # Accumulate weighted utility
            weight_sum += weight
            weight = 1  # Set weight for adjacent moves

        expected_utility = expected_utility / weight_sum  # Calculate expected utility

        label = f'Chance: Depth {depth}, Utility:{expected_utility:.4f}'
        self.add_node(node_id, label)
        return expected_utility

    def heuristic(self, board_state):
        return self.helper.heuristic(board_state)  # Use helper to evaluate board state