from pacman_module.game import Agent
from pacman_module.pacman import Directions

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

def getUtility(state):
    """
    Returns the utility score for a terminal state.

    argument : the current game state

    """

    return state.getScore()

def mini(state, closed):
    """
    Returns the minimum value for the utility evaluated recursively.

    argument : a game state and the set of different state already explored.

    """

    if terminal_state(state):
        return getUtility(state)

    mini = float('inf') 
    for next_state, action in state.generateGhostSuccessors(1):
        state_key=key(next_state)
        if state_key not in closed:
            closed.add(state_key)
            utility = getMax(next_state,closed)
            if utility < mini :
                mini = utility

    if mini == float('inf'):
        return -mini

    return mini


def getMax(state, closed):
    """
    Returns the maximum value for the utility evaluated recursively.

    argument : a game state, the depth and the set of different state already explored.
    
    """

    if terminal_state(state):
        return getUtility(state)

    maxi = float('-inf')
    for next_state, action in state.generatePacmanSuccessors():
        state_key=key(next_state)
        if state_key not in closed:
            closed.add(state_key)
            utility = mini(next_state,closed)
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
        self.move = self.minimax(state)
        try:
            return self.move

        except IndexError:
            return Directions.STOP

    def minimax(self, state):
        """
        Returns the optimal move considered by the minimax algorithme.

        Argument : The state of the game.

        """

        if terminal_state(state):
            return []

        maxi = float('-inf')
        closed = set()
        for next_state, action in state.generatePacmanSuccessors():
            utility = mini(next_state,closed)
            if utility > maxi:
                maxi = utility
                move = action
                
        return move