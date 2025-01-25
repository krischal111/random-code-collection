MCTS
======
Theory
--------

What is **MCTS**?

**MCTS** stands for **Monte Carlo Tree Search**. It is employed in games or decision making process where we have to make a decision and maximize the chances of winning, even if opponent make their best moves. It makes a game tree based on choices of moves, and see which move leads to higher wins. Clever tricks go into making the algorithm do its work.

To really understand **MCTS** let's understand few related algorithms:

1. **Minmax algorithm**: In this algorithm, game tree is made based on the choices of moves up-to a certain depth. After the certain depth, if game is not terminal, we use some heuristics to calculate the chances of winning. And we analyze the preceeding move's value based on the result preference of the movemaker. And we do the same for the preceeding moves until we reach the move which we are analyzing. Which will guide us in the decision making process.

Let's take an example of chess.

Let's say, from the starting position, we create a tree by considering all moves upto the depth 5. So, the 5th move is made by the white. We have a function which sees the position and calculates how favorable is the position for white. Since it's white's turn to make the move, it is in white's best interest to choose the one which will maximize his reward, i.e. choosing his most favorable position. So, if white reaches that position, we can say, that position's value is the same as the maximum reward he can manage by making a move. This is maximizing step.

For the preceeding move, it would be black's turn, so he will choose the position which will minimize any reward that white can salvage from the position. So, if black reaches that position, we can say, the position's value is the same as the minimum reward for white caused by a move made by black. This is minimizing step.

For preceeding move, we can again choose a move that maximizes white's reward, and so on until we reach the point where we have to actually make a decision.

This algorithm is perfect as long as heuristic function is accurate. A perfect heuristic function is difficult to achieve because in chess, a position can look good, but if you analyze deeper, you can lose. An example is sacrificing a piece after 3 moves for a checkmate in another 4 moves. So, we can't rely on simple heuristic function and we have to look deeper, to be more accurate. But going deeper is not as easy as it seems. There are so many moves from a single position, and even if you go single level deep your number of position to analyze goes up by a factor of maybe 15 or so. You will run out of memory or time.

2. **Monte Carlo algorithm**: Monte carlo is an algorithm where we sample large number of random events and calculate probability of an event by dividing it's occurances by total number of experiments. An analogy is if you have a coin that lands on one side more than the other, you throw the coin 1000 times, and if you see head lands 650 times, you are confident that head probability is very close 0.65 and tail is 0.35. The more experiments you run, the more confident you can be on your results.

If you want to apply monte carlo to the chess, you can do the following.

1. Get a list of legal moves you can make from the position. 
2. For each move, start making random moves until you either win or lose at chess.
3. Choose the move where you won the maximum number of times.

Since we are only analyzing one particular chain of moves rather than considering all moves, we can analyze a games a lot faster, but this falls to a certain trap in complex games like chess.

For instance, there can be one move that can look very promising because you will win most of the time. But there can be exactly one countermove which will checkmate you in few steps. Making an assumption that each move is equally likely (from a random simulation) can trick you to make such move.

***Why not take best from both algorithms?***

Let's start with Monte Carlo algorithm and make it better. *The main problem with __simple Monte Carlo algorithm__ is an assumption that each move is equally likely.* However, the reality is, every player is more inclined to make a move that is beneficial for themselves, and they will very rarely play move a move that harms them.

### Arriving at MCTS

Instead of making a random move, why not select the move that has the most win probability on each step. But it is easier said than done.

Initially, we don't know the probability of win for any move, so we cannot make such choice. That's were main *Monte Carlo simulation* comes in. For each state we analyze, we have to play a few random games to gauge initial probability. This is the monte carlo part of the MCTS.

After that we can start to make more promising moves while also exploring the unexplored moves. This is the tree search part of the MCTS.

In other places you will often see MCTS being divided into four parts: selection, expansion, simulation and backpropagation. But, to really understand, dividing the game into **Monte Carlo** step and **Tree Search** step is enough. We will see later that in *Monte Carlo* steps we will perform *Expansion* and *Simulation*. In *Tree Search* steps we will perform selection. *Backpropagation* will be done in both steps.

The backpropagation is used on both monte carlo and tree search step. Expansion and simulation is used on the monte carlo step and selection is applied in the tree search step.

So, the real trick is to know when to use Monte Carlo and when to use Tree Search. Our default behaviour shall be Tree Search, where selection of next node to search is based on win statistics and exploration. This can only be applied when we have win statistics for all the possible move we make from the given state. So, in such case, we apply monte carlo simulation to get initial statistics for a move.

Now, let's be focused on implementation details for successful application of MCTS.

### Detailed working

Let's say, we are currently on a state 'S'. We have set of legal moves `M = {m1, m2, ... mn}`. From the given state, we make a root MCTS node: `N`. All MCTS decisions are made from this node.

We also have limited simulation budget because each simulation would take certain time to finish. So, each MCTS based searching would need to finish in certain number of simulations (or certain time).

From the state of node 'N', we see whether all possible moves have been simulated at least once. Even a single simulation is enough to get a very rough estimate of win probability. 

#### Monte Carlo step
If any unsimulated move exists, that state by making that move is appended as a new child node 'C'. We can follow the same process for the child node 'C', until terminal condition is reached. In that case, result statistics is backpropagated from the terminal node to all its ancestors by traversing the parent nodes. This process is called backpropagation.

#### Tree Search step
If all moves have been simulated, we analyze statistics to decide which move is to make. Generally an Upper Confidence Bound (UCB) is used to select a node balancing exploration and exploitation. UCB for all children node are calculated one with the highest score is selected.

$${UCB} = \frac{w_i}{n_i} + c \cdot \sqrt{\frac{\ln t}{n_i}}$$

Where:
- $w_i$ : Total wins of the child node
- $n_i$ : Total number of simulations run from the child node
- $c$ : exploration parameter, typically $\sqrt 2$
- $t$ : Total number of simulations run from the parent node.

Pseudo code for child node selection could look like:

`selected_node = children[` `argmax([UCB(child) for child in children])` `]`

The formula for UCB is divided into two parts:

1. Exploitation part: 

The term $\frac{w_i}{n_i}$ gives the average win rate of a move. We have to analyze the promising moves deeper, to be sure if its the move that really drives us to win.

Initially, when not much games are simulated, win rate would seem random. But as deeper winning positions are identified, such decisive position played would be selected more often, leading to more accurate estimation of win rate. 

Also, win rate is calculated based on who has control over that state. So, for multiplayer games, there would be different win rate for different players, and each node will use only the win rate for the player making the next move. For a dynamic game, it would take very high number of simulations to be certain about the win rates.

2. Exploration part:

The term $c \cdot \sqrt{\frac{\ln t}{n_i}}$ gives how less the move is simulated compared to all other alternatives combined. If a move isn't explored much, it would make sense for us to explore it further, and see if some hidden winning sequences are lurking behind the not much explored move.

The suitable choice of variable $c$ would allow us to control the exploration rate.

Also, the UCB formula depends on number of simulation of the child node. So, if any child node isn't simulated yet, its win rate would be undefined and thus the formula cannot be applied. So, a child has to be simulated at least once, which can be done using the monte carlo step.

After selecting the suitable move, we would do the same for the child nodes until we reach terminal condition and backpropagate the results. 

To be consistent with other tutorials for MCTS, we clarify the four steps of MCTS based on what we have discussed yet.

1. Backpropagation:
The process of updating result statistics and simulation count by traversing the parent nodes after a terminal node is reached where game becomes decisive (i.e. Some of the players win or game results in a draw.)

2. Simulation:
A game is randomly (or heuristically) played from a state until we reach a terminal state (game over). This allows us to get initial statistics for a particular move (and its parents). This is also called rollout or playout. If each move during simulation is chosen randomly, it is called light playout and if some heuristics is used to make game more realistic, it is heavy playout. This is the monte carlo step of the MCTS.

3. Selection:
From the parent node, one of the child node is selected based on win statistics and simulation counts. UCB is employed for the selection. This is the "Tree Search" step of the MCTS. This allows us to bias the selection towards the most likely moves for all the players, and simulate realistic gameplay statistics to base our decision upon.

4. Expansion:
When some of the moves haven't been simulated yet, we choose one of them and add it as a children node from the next state from it. This is immediately followed by simulation step, because we need at least one simulation for all children nodes if we have to select a child node based on their win statistics. Thus, this is also a part of "Monte Carlo" step.


#### Deciding on the final move
After we've exhausted the simulation budget whether it be count or total time. Its time to make a decion on which move to make.

We could go with several choices:
##### 1. Use UCB values with exploration constant (c = 0).
This is equivalent to going with the move with highest win rate. However, the win rate could be inflated by previous simulation when counter move were yet to be found. Most likely it wouldn't be so.

##### 2. Go with the move with highest simulation count
The moves that are simulated highest would have many lines well explored. Plus, any move that would be simulated more often means it has had historically higher win rate with many different win rates, because losing moves wouldn't be simulated that much. However, when exploration constant is low, we could go with suboptimal moves when left with low simulation budget, because other possible winning lines wouldn't be explored.

This is the main principles needed to make MCTS work.

Now, let's see one implemention of MCTS in python.

Implementation
----------------

### Helper libraries:
```python
import numpy as np
```
numpy provides us with some useful functions like:
- `argmax`: Getting the index of highest value item in a list.
- `random.choice`: Make a random choice from given list of items.
- `sqrt` and `log`: Used to invoke mathematical functions

### MCTS Node:

Implementation as a class:

```python
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
```

#### Attributes
The explanation for the attributes of the nodes are:
- `state`: Represent a game state. For tictactoe, it can be a board array.
    Further, the state must have following attributes and methods
    - `players`: List of all the players.
    - `player_id`: Id of the player who makes the move from this state
    - `get_legal_actions()`: Gives the list (or set) of all the legal actions from the state.
    - `move(action)`: Performs the given move and returns a new state.
    - `is_game_over()`: Checks if the game is over
    - `game_result()`: Returns the dictionary of reward points for all the players in the game.
- `parent`: Link to the parent node.
- `parent_action`: The move made by the parent node to arrive at this state. This is used when we identify this as our prferred state, and need the action which resulted in this state to use in a real game play.
- `children`: This list stores the children nodes. When we append children for the first time, we immediate simulate it so that we get initial statistics during the selection phase.
- `player_id`: This stores the player id who has control over the next state. (Current movemaker)
- `statistics`: This stores two fields:
    - `number_of_visits`: Total visits (simulations) made from the state that apperars after this node.
    - `values`: This is the dictionary that stores each player's win count in the simulations made from states that appear after this node.
- `_untried_actions`: This stores the list of actions (legal moves) that haven't been simulated yet.

#### Methods

```python
def untried_actions(self):
    self._untried_actions = self.state.get_legal_actions()
    return self._untried_actions
```
Generates list of legal moves while instantiating a node:

```python
def q(self, player_id): 
    "Total value of this state"
    return self.statistics['values'][player_id]
```
Gets the total value (wins/losses) of the node for the player of the current state.  
    
```python
def n(self): 
    "Total number of visits of this state"
    return self.statistics['number_of_visits']
```
Gets total number of visits of this node.
    
```python
def expand(self):
    "This expands the node by adding a new child node from an untried action"
    action = self._untried_actions.pop()
    next_state = self.state.move(action)
    child_node = MonteCarloTSNode(next_state, self, action)
    self.children.append(child_node)
    return child_node
```
Chooses a move from untried actions, uses it to get a new state, and adds that to a new children node.
    
```python
def is_terminal_node(self):
    return self.state.is_game_over()
```
Checks if the node is in game over state, from where win statistics can be calculated and backpropagated if needed.

```python
def backpropagate(self, result):
    self.statistics['number_of_visits'] += 1
    for player, value in result.items():
        self.statistics['values'][player] += value
    if self.parent:
        self.parent.backpropagate(result)
```
Updates the simulation and win statistics for all the parent nodes.

----

The following few methods are useful for monte carlo simulation part of the MCTS.

```python
def rollout_policy(self, possible_moves):
    return np.random.choice(possible_moves)
```
A light playout based rollout policy.

```python
def rollout(self, depth=100):
    current_rollout_state = self.state
    while not current_rollout_state.is_game_over() and depth:
        depth -= 1
        possible_moves = current_rollout_state.get_legal_actions()
        action = self.rollout_policy(possible_moves)
        current_rollout_state = current_rollout_state.move(action)
    return current_rollout_state.game_result()
```
A method to make "random" moves until terminal state is reached. No new children will be added in the process.

---

The following methods are useful for the "Tree Search" part of the MCTS

```python
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
```
Calculates the UCB values for all the children nodes using the formula:
$${UCB} = \frac{w_i}{n_i} + c \cdot \sqrt{\frac{\ln t}{n_i}}$$

```python
def select_best_child(self, c_param=1.41):
    return self.children[np.argmax(self.children_UCBs(c_param=c_param))]
```
Selects the child with the highest UCB value. The selection part of the MCTS.

```python
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
```
Simulates one game using the Monte Carlo Tree Search.

```python
def mcts_search(self, max_iterations=1000, max_depth=100):
    for _ in range(max_iterations):
        self.mcts_1_simulate(max_depth=max_depth)
    return self.best_so_far().parent_action
```
Performs many simulations of the games using MCTS.

_____

The following method helps us to select the best node after MCTS has been applied. 

```python
def best_so_far(self):
    # This will give the most robust child
    return max(self.children, key=lambda child: child.n())
```
Gets the best children node based on the number of visits. This function has already been used in the `mcts_search()` function.

#### Usage

To use this MCTS implementation in your code, you just need two lines to get to a best state:

```python
root = MonteCarloTSNode(state)
action = root.mcts_search(max_iterations=1000) # 1000 simulations
```

### Conclusion

In conclusion, MCTS is really interesting, and its implementation is also simple if we know what we are doing. I recommend anyone reading this to implement in your computer, change things and see what works better for you. 

In my experience, just changing the variable names and making minor modifications while copying greatly improves the understanding I achieve from the given code.

Also, understanding the MCTS really helps if you are learning reinforcement learning, or you want to make some game playing bot. It's 2:34 am, 26 January 2025. I really need to sleep now. Goodbye.