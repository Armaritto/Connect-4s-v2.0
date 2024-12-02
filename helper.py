from board import Board
from digraph_factory import Digraph_factory

class Helper:

    def __init__(self, k):
        self.board = Board()
        self.factory = Digraph_factory()
        self.dot = self.factory.create_digraph("minimax", k)
        self.node_counter = 0
        pass

    def board_to_string(self, board_state):
        if board_state is None:     # if the board state is None, return "No valid moves"
            return "No valid moves"
        return '\n'.join([''.join(row) for row in board_state])
    
    def add_node(self, node_id, label):     # add a node to the graph
        self.dot.node(node_id, label)

    def add_edge(self, parent_id, child_id):        # add an edge to the graph
        self.dot.edge(parent_id, child_id)
    
    def maximize(self, depth, board_state, parent_id):
        # set the current player to the AI player
        self.board.current_player = 'O'
        if self.board.is_full() or depth == 0:      # if the board is full or the depth is 0 (Terminal State)
            node_id = str(self.node_counter)        # set the node id to the current node counter
            self.node_counter += 1
            utility = self.heuristic(board_state)       # calculate the utility of the board state
            # set the label of the node
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

        # initialize the max child and max utility
        max_child, max_utility = None, float('-inf')

        for child in self.board.get_children(board_state):      # get the children of the board state
            _, utility = self.minimize(depth - 1, child, node_id)       # minimize the child

            if utility > max_utility:          # if the utility is greater than the max utility
                max_child, max_utility = child, utility
        
        label = f'Maximize: Depth {depth}, Utility: {max_utility} \n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)

        return max_child, max_utility

    def minimize(self, depth, board_state, parent_id):
        self.board.current_player = 'X'
        if self.board.is_full() or depth == 0:
            node_id = str(self.node_counter)
            self.node_counter += 1
            utility = self.heuristic(board_state)
            label = f'Leaf: Depth {depth}, Utility: {utility} \n{self.board_to_string(board_state)}'
            self.add_node(node_id, label)
            self.add_edge(parent_id, node_id)
            return board_state, self.heuristic(board_state)
        
        node_id = str(self.node_counter)
        self.node_counter += 1
        label = " "
        self.add_node(node_id, label)
        if parent_id is not None:
            self.add_edge(parent_id, node_id)

        min_child, min_utility = None, float('inf')

        for child in self.board.get_children(board_state):
            _, utility = self.maximize(depth - 1, child, node_id)

            if utility < min_utility:
                min_child, min_utility = child, utility
        
        label = f'Minimize: Depth {depth}, Utility:{min_utility} \n{self.board_to_string(board_state)}'
        self.add_node(node_id, label)

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
