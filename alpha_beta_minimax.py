from board import Board
from helper import Helper
from graphviz import Digraph

class AlphaBetaMinimax:
    def __init__(self, board):
        self.board = board
        self.helper = Helper()
        self.node_counter = 0
        self.dot = Digraph()

    def board_to_string(self, board_state):
        if board_state is None:
            return "No valid moves"
        return '\n'.join([''.join(row) for row in board_state])

    def add_node(self, node_id, label):
        print(f"Adding node: {node_id} -> {label}")
        self.dot.node(node_id, label)

    def add_edge(self, parent_id, child_id):
        print(f"Adding edge: {parent_id} -> {child_id}")
        self.dot.edge(parent_id, child_id)

    def is_terminal(self, board_state):
        return self.board.is_full() or self.helper.heuristic(board_state) in [float('inf'), float('-inf')]

    def evaluate_board(self, board_state, current_player):
        return self.helper.heuristic(board_state)

    def maximize(self, depth, board_state, alpha, beta, current_player, parent_id=None, indent=0):
        if depth == 0 or self.is_terminal(board_state):
            utility = self.evaluate_board(board_state, current_player)
            node_id = str(self.node_counter)
            self.node_counter += 1
            label = f'Maximize: Depth {depth}, Utility {utility}\n{self.board_to_string(board_state)}'
            self.add_node(node_id, label)
            if parent_id is not None:
                self.add_edge(parent_id, node_id)
            return board_state, utility, node_id

        max_utility = float('-inf')
        max_child = board_state
        node_id = str(self.node_counter)
        self.node_counter += 1
        label = f'Maximize: Depth {depth}, Utility {max_utility}\n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        for child in self.board.get_children(board_state, current_player):
            _, utility, child_id = self.minimize(depth - 1, child, alpha, beta, 'O', node_id, indent + 2)

            if utility > max_utility:
                max_utility = utility
                max_child = child

            alpha = max(alpha, utility)
            if beta <= alpha:
                break

        label = f'Maximize: Depth {depth}, Utility {max_utility}\n{self.board_to_string(max_child)}'
        self.dot.node(node_id, label)

        return max_child, max_utility, node_id

    def minimize(self, depth, board_state, alpha, beta, current_player, parent_id=None, indent=0):
        if depth == 0 or self.is_terminal(board_state):
            utility = self.evaluate_board(board_state, current_player)
            node_id = str(self.node_counter)
            self.node_counter += 1
            label = f'Minimize: Depth {depth}, Utility {utility}\n{self.board_to_string(board_state)}'
            self.add_node(node_id, label)
            if parent_id is not None:
                self.add_edge(parent_id, node_id)
            return board_state, utility, node_id

        min_utility = float('inf')
        min_child = board_state
        node_id = str(self.node_counter)
        self.node_counter += 1
        label = f'Minimize: Depth {depth}, Utility {min_utility}\n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        for child in self.board.get_children(board_state, current_player):
            _, utility, child_id = self.maximize(depth - 1, child, alpha, beta, 'X', node_id, indent + 2)

            if utility < min_utility:
                min_utility = utility
                min_child = child

            beta = min(beta, utility)
            if beta <= alpha:
                break

        label = f'Minimize: Depth {depth}, Utility {min_utility}\n{self.board_to_string(min_child)}'
        self.dot.node(node_id, label)

        return min_child, min_utility, node_id