import numpy as np
from copy import deepcopy

class State:
    "Tic Tac Toe State class"
    def __init__(self):
        "Creates a new Tic Tac Toe State"
        self.player_id = 1 # turn of the player
        self.players = [-1, 1]
        self.board = np.zeros(9, dtype=int)
    
    def get_legal_actions(self):
        return [i for i, v in enumerate(self.board) if v == 0]
    
    def move(self, action) -> 'State':
        new_state = deepcopy(self)
        new_state.board[action] = self.player_id
        new_state.player_id = -self.player_id
        return new_state

    def is_game_over(self):
        return self.winner() != 0 or all(v != 0 for v in self.board) 
    
    def winner(self):
        for player in self.players:
            for i in range(3):
                if all(self.board[i*3+j] == player for j in range(3)): # horizontal
                    return player
                if all(self.board[j*3+i] == player for j in range(3)): # vertical
                    return player
            if all(self.board[i*3+i] == player for i in range(3)): # diagonal 1
                return player
            if all(self.board[i*3+2-i] == player for i in range(3)): # diagonal 2
                return player
        return 0

    def game_result(self):
        winner = self.winner()
        if winner == 0:
            return {player: 0 for player in self.players}
        return {player: 1 if player == winner else -1 for player in self.players}
    
    def __str__(self):
        legal_moves = set(self.get_legal_actions())
        return ('\n--+---+--  ##  --+---+--\n').join(
            # iteration of rows
            ' | '.join(' XO'[v] for v in self.board[i*3:i*3+3]) 
            + '  ##  '
            + ' | '.join(str(i) if i in legal_moves else ' '  for i in range(i*3, i*3+3))
            for i in range(3)
        )