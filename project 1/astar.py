from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue
from pacman_module.util import manhattanDistance
def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    agrument : the current state game.

    """
    return (state.getPacmanPosition(), state.getFood())
    
def getCost(state, path, nb_caps_init):
    """
    Given a pacman state, returns an estimate final score 'f' of a state 
    which is a mix between the actual score 'g' and the score until the end 'h'. 

    argument : the current state game.

    """
    nb_caps = len(state.getCapsules())
    g = len(path) + (nb_caps_init - nb_caps)*5

    """ find the manhattan distance to the furthest food. """
    listFood = state.getFood().asList()
    pos = state.getPacmanPosition()
    md = 0
    while len(listFood) != 0:
        x = manhattanDistance(pos, listFood.pop())
        if x > md :
            md = x 

    h = md
    f = g+h

    return f 


class PacmanAgent(Agent):
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
            self.moves = self.astar(state)

        try:
            return self.moves.pop(0)

        except IndexError:
          return Directions.STOP
        
    def astar(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout in an optimal way.

        argument : the current state game.

        """
        path = []
        """ priorityqueue give state with best scoreEstimate. """
        fringe = PriorityQueue()
        nb_caps_init = len(state.getCapsules())
        cost = getCost(state, path, nb_caps_init)
        fringe.push([state, path],cost)
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
                    next_cost = getCost(next_state, next_path, nb_caps_init)
                    fringe.push([next_state, next_path], next_cost)


            
