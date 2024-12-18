from board import Board
from helper import Helper
from digraph_factory import Digraph_factory


class AlphaBetaMinimax:
    def __init__(self, k):
        self.board = Board()
        self.factory = Digraph_factory()
        self.dot = self.factory.create_digraph("alpha-beta", k)
        self.helper = Helper(k)
        self.node_counter = 0

    def board_to_string(self, board_state):
        if board_state is None:
            return "No valid moves"
        return '\n'.join([''.join(row) for row in board_state])  # Convert board state to string

    def add_node(self, node_id, label):
        self.dot.node(node_id, label)  # Add a node to the graph

    def add_edge(self, parent_id, child_id):
        self.dot.edge(parent_id, child_id)  # Add an edge to the graph

    def maximize(self, depth, board_state, alpha, beta, parent_id):
        self.board.current_player = 'O'     # set the current player to the AI player
        if self.board.is_full(board_state) or depth == 0: # if the board is full or the depth is 0 (Terminal State)
            # set the node id to the current node counter
            node_id = str(self.node_counter)
            self.node_counter += 1
            utility = self.helper.heuristic(board_state)        # calculate the utility of the board state
            # set the label of the node and add it to the graph
            label = f'Leaf: Depth {depth}, Utility: {utility} \n{self.board_to_string(board_state)}'
            self.add_node(node_id, label)
            if parent_id is not None:
                self.add_edge(parent_id, node_id)
            return board_state, utility

        # set the node id to the current node counter
        node_id = str(self.node_counter)
        self.node_counter += 1
        # add the node to the graph
        label = " "
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        max_child, max_utility = None, float('-inf')        # initialize the max child and max utility

        for child in self.board.get_children(board_state):
            _, utility = self.minimize(depth - 1, child, alpha, beta, node_id)      # minimize the child

            if utility > max_utility:       # if the utility is greater than the max utility, update the max child and max utility
                max_child, max_utility = child, utility

            if max_utility >= beta:         # if the max utility is greater than or equal to beta, break (prune the tree)
                break

            if max_utility > alpha:     # if the max utility is greater than alpha, update alpha
                alpha = max_utility

        # set the label of the node and add it to the graph
        label = f'Maximize: Depth {depth}, Utility: {max_utility} \n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)

        return max_child, max_utility

    def minimize(self, depth, board_state, alpha, beta, parent_id):
        self.board.current_player = 'X'     # set the current player to the human player
        if self.board.is_full(board_state) or depth == 0: # if the board is full or the depth is 0 (Terminal State)
            node_id = str(self.node_counter)
            self.node_counter += 1
            utility = self.helper.heuristic(board_state)        # calculate the utility of the board state

            # set the label of the node and add it to the graph
            label = f'Leaf: Depth {depth}, Utility: {utility} \n{self.board_to_string(board_state)}'
            self.add_node(node_id, label)
            if parent_id is not None:
                self.add_edge(parent_id, node_id)
            return board_state, utility

        # set the node id to the current node counter
        node_id = str(self.node_counter)
        self.node_counter += 1
        # add the node to the graph
        label = " "
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        min_child, min_utility = None, float('inf')     # initialize the min child and min utility

        for child in self.board.get_children(board_state):      # get the children of the board state
            _, utility = self.maximize(depth - 1, child, alpha, beta, node_id)      # maximize the child

            if utility < min_utility:           # if the utility is less than the min utility, update the min child and min utility
                min_child, min_utility = child, utility

            if min_utility <= alpha:        # if the min utility is less than or equal to alpha, break (prune the tree)
                break

            if min_utility < beta:      # if the min utility is less than beta, update beta
                beta = min_utility

        # set the label of the node and add it to the graph
        label = f'Minimize: Depth {depth}, Utility:{min_utility} \n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)

        return min_child, min_utility



