
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue

def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    arument : the curent state game.

    """
    return (state.getPacmanPosition(), state.getFood())
    
def getCost(path):
    """
    return the cost to access to a state (1 point/action) 

    argument : the path associated to a state.

    """
    g = len(path)
    h = 0
    f = g + h

    return f 

class PacmanAgent(Agent):
    """
    A Pacman agent based on Depth-First-Search.
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.moves = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        argument : the current state game.

        """

        if not self.moves:
            self.moves = self.bfs(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def bfs(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state.

        """

        path = []
        """ priorityqueue give state with best scoreEstimate. """
        fringe = PriorityQueue()
        cost = getCost(path)
        fringe.push([state, path], cost)
        closed = set()

        while True:
            if fringe.isEmpty():
                return []

            cost, currentState = fringe.pop()
            current = currentState[0]
            path = currentState[1]

            if current.isWin():
                return path

            current_key = key(current)

            if current_key not in closed:
                closed.add(current_key)
                for next_state, action in current.generatePacmanSuccessors():
                    next_path = currentState[1] + [action]
                    next_cost = getCost(next_path)
                    fringe.push([next_state, next_path], next_cost)
