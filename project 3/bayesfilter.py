from pacman_module.game import Agent
import numpy as np
from pacman_module import util
from scipy.stats import binom

class BeliefStateAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'update_belief_state' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None

        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None

        # Hyper-parameters
        self.ghost_type = self.args.ghostagent
        self.sensor_variance = self.args.sensorvariance

        self.p = 0.5
        self.n = int(self.sensor_variance/(self.p*(1-self.p)))

    def getNeighbor(self, n, m, pacpos):
        """
        Given a position, returns the weighted number of neighbor which are not walls depending the type of ghost

        Arguments:
        ----------
        - `n, m`: 2D coordinates of a position.
        - `pacpos`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A weighted number of neighbor of de position (n,m) which are not walls 

        """
        neighborNb = 0
        dist = util.manhattanDistance(pacpos,(n,m))

        """ 
        the weigth of the neighbor is always 1 for a neighbor who is closer to pacman and is param if neighbor is faster.
        param depends on ghost type 
        """
        if self.ghost_type == 'confused':
            param = 1
        elif self.ghost_type == 'afraid':
            param = 2
        else :
            param = 8

        if self.walls[n - 1][m] == 0:
            if util.manhattanDistance(pacpos,(n-1,m)) < dist:
                neighborNb += 1
            else:
                neighborNb += param

        if self.walls[n + 1][m]  == 0:
            if util.manhattanDistance(pacpos,(n+1,m)) < dist:
                neighborNb += 1
            else:
                neighborNb += param

        if self.walls[n][m-1]  == 0:
            if util.manhattanDistance(pacpos,(n,m-1)) < dist:
                neighborNb += 1
            else:
                neighborNb += param

        if self.walls[n][m+1]  == 0:
            if util.manhattanDistance(pacpos,(n,m+1)) < dist:
                neighborNb += 1
            else:
                neighborNb += param

        return neighborNb

    def update_belief_state(self, evidences, pacman_position, ghosts_eaten):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step
        - `ghosts_eaten`: list of booleans indicating
          whether ghosts have been eaten or not

        Return:
        -------
        - A list of Z belief states at state x_{t}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze.
               Matrices filled with zeros must be returned for eaten ghosts.
        """
        beliefStates = self.beliefGhostStates
        z = 0
        bs = beliefStates[z]
        size_maze = np.shape(bs)

        """ 
        the weigth of the neighbor is always 1 for a neighbor who is closer to pacman and is param if neighbor is faster.
        param depends on ghost type 
        """
        if self.ghost_type == 'confused':
            param = 1
        elif self.ghost_type == 'afraid':
            param = 2
        else :
            param = 8

        for eaten in ghosts_eaten:
            bs = beliefStates[z]
            """ ubs = update belief state initialize to a n*m tab of 0 """
            ubs = np.zeros(size_maze[0]*size_maze[1]).reshape(size_maze[0],size_maze[1]) 
            if eaten == 0:
                n = 1
                while n < size_maze[0]-1:
                    m = 1
                    while m < size_maze[1]-1:
                        if self.walls[n][m] == 1:
                            ubs[n,m] = 0
                        else:
                            """ look the probability to arrive in position (n,m) from neighbor position """
                            prob_bottom = 0
                            prob_top = 0
                            prob_left = 0
                            prob_right = 0
                            dist = util.manhattanDistance(pacman_position,(n,m))

                            """
                            probability to go further to pacman depends on the parameter
                            """
                            if self.walls[n][m-1] == 0:
                                if util.manhattanDistance(pacman_position,(n,m-1)) > dist:
                                    prob_bottom = 1/self.getNeighbor(n,m-1,pacman_position)
                                else:
                                    prob_bottom = param/self.getNeighbor(n,m-1,pacman_position)
                                
                            if self.walls[n][m+1] == 0:
                                if util.manhattanDistance(pacman_position,(n,m+1)) > dist:
                                    prob_top = 1/self.getNeighbor(n,m+1,pacman_position)
                                else:
                                    prob_top = param/self.getNeighbor(n,m+1,pacman_position)

                            if self.walls[n-1][m] == 0:
                                if util.manhattanDistance(pacman_position,(n-1,m)) > dist:
                                    prob_left = 1/self.getNeighbor(n-1,m,pacman_position)
                                else:
                                    prob_left = param/self.getNeighbor(n-1,m,pacman_position)

                            if self.walls[n+1][m] == 0:
                                if util.manhattanDistance(pacman_position,(n+1,m)) > dist:
                                    prob_right = 1/self.getNeighbor(n+1,m,pacman_position)
                                else:
                                    prob_right = param/self.getNeighbor(n+1,m,pacman_position)

                            """ calculate the probability of position (n,m) given the evidence """
                            noise = dist - evidences[z] + self.n*self.p
                            prob_evidence = binom.pmf(noise, self.n, self.p)
                            """ bayesfilter """
                            ubs[n,m] = prob_evidence*(prob_bottom*bs[n,m-1]+prob_top*bs[n,m+1]+prob_left*bs[n-1,m]+prob_right*bs[n+1,m])
                        m+=1
                    n+=1
                """normalization"""
                prob_tot = 0
                n = 1
                while n < size_maze[0]-1:
                    m = 1
                    while m < size_maze[1]-1:
                        prob_tot += ubs[n,m]
                        m+=1
                    n+=1
                n = 1
                if prob_tot > 0:
                    while n < size_maze[0]-1:
                        m = 1
                        while m < size_maze[1]-1:
                            ubs[n,m] /= prob_tot
                            m+=1
                        n+=1
                else :
                    """ if all probability == 0 (because to small value are 0) put an equiprobal value on all position """
                    prob_eq = (size_maze[0]-2)*(size_maze[1]-2)
                    n = 1
                    while n < size_maze[0]-1:
                        m = 1
                        while m < size_maze[1]-1:
                            ubs[n,m] = 1/prob_eq
                            m+=1
                        n+=1

            else:
                """ if ghost is eaten, all probabilities put to 0 """
                n = 1
                while n < size_maze[0]-1:
                    m = 1
                    while m < size_maze[1]-1:
                        ubs[n,m] = 0
                        m+=1
                    n+=1

            beliefStates[z] = ubs 
            z+=1           
        self.beliefGhostStates = beliefStates
        return beliefStates

    def _get_evidence(self, state):
        """
        Computes noisy distances between pacman and ghosts.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.


        Return:
        -------
        - A list of Z noised distances in real numbers
          where Z is the number of ghosts.

        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []

        for pos in positions:
            true_distance = util.manhattanDistance(pos, pacman_position)
            noise = binom.rvs(self.n, self.p) - self.n*self.p
            noisy_distances.append(true_distance + noise)

        return noisy_distances

    def _record_metrics(self, belief_states, state):
        """
        Use this function to record your metrics
        related to true and belief states.
        Won't be part of specification grading.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.
        - `belief_states`: A list of Z
           N*M numpy matrices of probabilities
           where N and M are respectively width and height
           of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """
        z = 0
        bs = belief_states[z]
        size_maze = np.shape(bs)
        uncertainty = 0
        quality = 0
        positions = state.getGhostPositions()
        for bs in belief_states:
            ghost_pos = positions[z]
            max_prob = 0
            qual = 0
            n = 1
            while n < size_maze[0]-1:
                m = 1
                while m < size_maze[1]-1:
                    qual += bs[n,m] * util.manhattanDistance((n,m), ghost_pos)
                    if bs[n,m] > max_prob:
                        max_prob = bs[n,m]
                    m+=1
                n+=1
            uncertainty += max_prob
            quality += qual
            z += 1
        uncertainty /= z
        quality /= z
        quality *= -1
        quality += 27
        quality /= 27

        return uncertainty, quality


    def get_action(self, state):
        """
        Given a pacman game state, returns a belief state.

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A belief state.
        """

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()

        evidence = self._get_evidence(state)
        newBeliefStates = self.update_belief_state(evidence,
                                                   state.getPacmanPosition(),
                                                   state.data._eaten[1:])
        print(self._record_metrics(self.beliefGhostStates, state))
        return newBeliefStates, evidence
