from tic_tac_toe import State

if __name__ == "__main__":
    state = State()
    while not state.is_game_over():
        print(state)
        print("Legal actions:", state.get_legal_actions())
        while True:
            action = int(input("Enter your move: "))
            if action in state.get_legal_actions():
                break
            print("Invalid move")
        state = state.move(action)
    print(state)
    print("Game Over")
    winner = {0: "Draw", 1: "Player 1", -1: "Player 2"}[state.winner()]
    print("Winner:", winner)
    print("Game result:", state.game_result())