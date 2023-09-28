
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance

def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    argument : the current state game.

    """
    return (state.getPacmanPosition(), state.getFood(),state.getGhostPosition(1))

def terminal_state(state):
    """
    Returns True if the game is in a terminal state, false otherwise.

    argument : the current game state.

    """
    return state.isWin() or state.isLose()

def eval(state):
    """
    Returns an evaluation of the expected score for a Pacaman game state.

    argument : the current game state.

    """

    listFood = state.getFood().asList()
    pos = state.getPacmanPosition()
    md = 0
    md1 = float('inf')
    while len(listFood) != 0:
        x = manhattanDistance(pos, listFood.pop())
        if x > md :
            md = x 
        if x < md1:
            md1 = x
    if md1 == float('inf'):
        md1 = 0
    fin = 0
    if state.isLose():
        fin = -500
    if state.isWin():
        fin = 500


    return fin+manhattanDistance(state.getPacmanPosition(), state.getGhostPosition(1))-50*state.getFood().depth() - 4*md1

def mini(state, closed, depth):
    """
    Returns the minimum value for the utility evaluated recursively.

    argument : a game state, the depth and the set of different state already explored.

    """

    if depth == 4 or terminal_state(state):
        return eval(state)

    mini = float('inf') 
    for next_state, action in state.generateGhostSuccessors(1):
        state_key=key(next_state)
        if state_key not in closed:
            closed.add(state_key)
            utility = getMax(next_state,closed,depth+1)
            if utility < mini :
                mini = utility

    if mini == float('inf'):
        return -mini

    return mini


def getMax(state, closed, depth):
    """
    Returns the maximum value for the utility evaluated recursively.

    argument : a game state, the depth and the set of different state already explored.
    
    """
    
    if depth == 4 or terminal_state(state):
        return eval(state)

    maxi = float('-inf')
    for next_state, action in state.generatePacmanSuccessors():
        state_key=key(next_state)
        if state_key not in closed:
            closed.add(state_key)
            utility = mini(next_state,closed,depth+1)
            if utility > maxi :
                maxi = utility

    if maxi == float('-inf'):
        return -maxi

    return maxi

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        self.move = self.hminimax0(state)

        try:
            return self.move

        except IndexError:
            return Directions.STOP

    def hminimax0(self, state):
        """
        Returns the optimal move considered by the hminimax algorithme.

        Argument : The state of the game.

        """

        if terminal_state(state):
            return []
        maxi = float('-inf')
        closed = set()
        depth = 0
        move = 'Stop'
        for next_state, action in state.generatePacmanSuccessors():
            utility = mini(next_state,closed,depth)
            if utility > maxi:
                maxi = utility
                move = action

        return move