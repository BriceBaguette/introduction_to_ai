# Complete this class for all parts of the project
from pacman_module import util
from pacman_module.game import Agent
from pacman_module.pacman import Directions
import numpy as np


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

    def get_action(self, state, belief_state):
        """
        Given a pacman game state and a belief state,
                returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - `belief_state`: a list of probability matrices.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        z = 0
        bs = belief_state[z]
        size_maze = np.shape(bs)
        """ looking for the closest belief ghost """
        ghost_dist_min = size_maze[0]+size_maze[1]
        best_n = 0
        best_m = 0
        pac_pos = state.getPacmanPosition()
        for bs in belief_state:
            """ belief ghost position is the position with highest probability """
            max_prob = 0
            pos_n = 0
            pos_m = 0
            n = 1
            while n < size_maze[0]-1:
                m = 1
                while m < size_maze[1]-1:
                    if bs[n,m]>max_prob:
                        max_prob = bs[n,m]
                        pos_n = n
                        pos_m = m
                    m+=1
                n+=1
            """ in this case, ghost is already eaten """
            if max_prob == 0:
                continue
            if util.manhattanDistance(pac_pos,(pos_n,pos_m)) < ghost_dist_min:
                ghost_dist_min = util.manhattanDistance(pac_pos,(pos_n,pos_m))
                best_n = pos_n
                best_m = pos_m

        """ looking for the best move to approach the closest ghost """
        move = 'Directions.STOP'
        dist_h = best_n-pac_pos[0]
        dist_v = best_m-pac_pos[1]
        walls = state.getWalls()

        if abs(dist_h) > abs(dist_v):
            if dist_h > 0:
                move = 'East'
                n = 1
            else:
                move = 'West'
                n = -1
            if move not in state.getLegalActions(0):
                if dist_v > 0:
                    move = 'North'
                    m = 1
                else:
                    move = 'South'
                    m = -1
                if move not in state.getLegalActions(0):
                    action = state.getLegalActions(0)
                    move = action[0]
        else:
            if dist_v>0:
                move = 'North'
                m = 1
            else:
                move = 'South'
                m = -1
            if move not in state.getLegalActions(0):
                if dist_h > 0:
                    move = 'East'
                    n = 1
                else:
                    move = 'West'
                    n = -1
                if move not in state.getLegalActions(0):
                    action = state.getLegalActions(0)
                    move = action[0]
                    
        return move

