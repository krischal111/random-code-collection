from tic_tac_toe import State
from monte_carlo_node_my import MonteCarloTSNode

def play_using_mcts(mcts_player=0):
    state = State()
    while not state.is_game_over():
        print(state)
        print("Legal actions:", state.get_legal_actions())
        if state.player_id == mcts_player:
            root = MonteCarloTSNode(state)
            action = root.mcts_search(1000)
        else:
            while True:
                action = int(input("Enter your move: "))
                if action not in state.get_legal_actions():
                    print("Invalid move")
                    continue
                break
        state = state.move(action)
    print(state)
    print("Game Over")
    winner = {0: "Draw", 1: "Player 1 (X)", -1: "Player 2 (O)"}[state.winner()]
    print("Winner:", winner)
    print("Game result:", state.game_result())

if __name__ == "__main__":
    choice = input("Do you want to play as X or O? (X/O): ").strip().lower()
    if choice in ["o", "0"]:
        play_using_mcts(mcts_player = 1)
    elif choice == "x":
        play_using_mcts(mcts_player = -1)
    else:
        play_using_mcts()