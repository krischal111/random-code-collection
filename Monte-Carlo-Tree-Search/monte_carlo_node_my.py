import numpy as np

class MonteCarloTSNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action= parent_action
        
        self.children = []
        self.player_id = state.player_id
        self.statistics = {
            'number_of_visits': 0,
            'values': {
                player: 0 for player in state.players
            }
        }

        self._untried_actions = self.untried_actions()
    
    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions
    
    def q(self, player_id): 
        "Total value of this state"
        return self.statistics['values'][player_id]
    
    def n(self): 
        "Total number of visits of this state"
        return self.statistics['number_of_visits']
    
    def expand(self):
        "This expands the node by adding a new child node from an untried action"
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTSNode(next_state, self, action)
        self.children.append(child_node)
        return child_node
    
    def is_terminal_node(self):
        return self.state.is_game_over()
    
    def backpropagate(self, result):
        self.statistics['number_of_visits'] += 1
        for player, value in result.items():
            self.statistics['values'][player] += value
        if self.parent:
            self.parent.backpropagate(result)
    
    # methods for simulation for initial statistics
    def rollout_policy(self, possible_moves):
        return np.random.choice(possible_moves)
    
    def rollout(self, depth=100):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over() and depth:
            depth -= 1
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()
    
    # method for application of mcts
    def children_UCBs(self, c_param=1.41):
        "Upper confidence bound for trees"
        # I guarantee that this will not generate a division by zero
        # I will do this by immediate rollout of any node that has just been expanded.
        if any(child.n() == 0 for child in self.children):
            raise ValueError("At least one child has not been visited")
        return [
            (child.q(self.player_id) / child.n() +
             c_param * np.sqrt(2 * np.log(self.n()) / child.n()))
            for child in self.children
        ]
    
    def select_best_child(self, c_param=1.41):
        # if len(self.children_UCBs(c_param=c_param)) == 0:
        #     print(self)
        #     print(self._untried_actions)
        #     print(self.state.get_legal_actions())
        return self.children[np.argmax(self.children_UCBs(c_param=c_param))]

    def mcts_1_simulate(self, max_depth=100):
        current_node = self
        while not current_node.is_terminal_node():
            # just do one instance of the simulation
            if current_node._untried_actions:
                child_node = current_node.expand()
                result = child_node.rollout(depth=max_depth) # one simulation instance
                child_node.backpropagate(result)
                return
            else:
                current_node = current_node.select_best_child()
        result = current_node.state.game_result()
        current_node.backpropagate(result)
        return

    def mcts_search(self, max_iterations=1000, max_depth=100):
        for _ in range(max_iterations):
            self.mcts_1_simulate(max_depth=max_depth)
        return self.best_so_far().parent_action
    
    def best_so_far(self):
        # This will give the most robust child
        return max(self.children, key=lambda child: child.n())
    
    def __repr__(self):
        return (f"MonteCarloTSNode()\n{self.state})\n"
        + "Statistics:"
        + str(self.statistics)
        )
    