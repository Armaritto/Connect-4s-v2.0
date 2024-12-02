import random
class Board:
    def __init__(self):
        self.board = ['E' * 7 for _ in range(6)]
        self.current_player = 'X'

    def toggle_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
            
    def make_move(self, column):
        for row in reversed(self.board):
            if row[column] == 'E':
                row[column] = self.current_player
                if self.current_player == 'X':
                    self.current_player = 'O'
                else:
                    self.current_player = 'X'
                return True
        return False
    
    def make_move_with_chance(self, column):
        chosen_move = column
        moves = []
        for col in [chosen_move, chosen_move-1, chosen_move+1]:
            if 0 <= col <= 6:
                if self.board[0][col] == 'E':
                    moves.append(col)
        
        weight = 3
        samples = []
        for move in moves:
            for i in range(weight):
                samples.append(move)
            weight = 1
        random_move = random.choice(samples)
        print("samples player :     " + str(samples))
        self.make_move(random_move)

    def get_children(self, board_state):
        children = []
        for col in range(7):
            if board_state[0][col] == 'E':
                child = [list(row) for row in board_state]
                for row in reversed(child):
                    if row[col] == 'E':  
                        row[col] = self.current_player
                        children.append(child)
                        break
        return children

    def is_full(self): #checks terminal state
        return all(cell != 'E' for row in self.board for cell in row)

    def check_player_score(self):
        return self.score('X')

    def check_agent_score(self):
        return self.score('O')

    def score(self, player):
        score = 0
        for row in self.board:
            for i in range(4):
                if row[i:i + 4] == [player] * 4:
                    score += 1
        for col in range(7):
            for i in range(3):
                if [self.board[i+j][col] for j in range(4)] == [player]*4:
                    score += 1
        for i in range(3):
            for j in range(4):
                if [self.board[i+k][j+k] for k in range(4)] == [player]*4:
                    score += 1
                if [self.board[i+k][j+3-k] for k in range(4)] == [player]*4:
                    score += 1
        return score

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.board)