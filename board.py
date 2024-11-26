class Board:
    def __init__(self):
        self.board = ['E' * 7 for _ in range(6)]
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

    def is_full(self):
        return all(cell != 'E' for row in self.board for cell in row)

    def check_player_score(self):
        return sum(row.count('X') for row in self.board)

    def check_agent_score(self):
        return sum(row.count('O') for row in self.board)

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.board)