import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState

class q1a_problem:
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.startingGameState: GameState = gameState

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        return self.startingGameState

    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        return state.food_coord == state.visited[-1]

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        # ------------------------------------------
        "*** O(b*|visited|) time complexity ***"
        
        # get all neighbours
        curr_coord, rolling_weight, visited, food_coord, direction = state.visited[-1], state.rw, state.visited, state.food_coord, state.directions

        neighbours = self.graph[list_to_str(curr_coord)].neighbour
        new_succ = []
        for neighbour_dir in neighbours.keys():     # O(b)
            # make sure it hasn't been visited
            if neighbours[neighbour_dir].coord not in visited:      # O(visited)
                # O(Visited)
                new_succ.append([
                    State(
                        rolling_weight+1, 
                        visited+[neighbours[neighbour_dir].coord], 
                        food_coord,
                        direction + [neighbour_dir]),
                    neighbour_dir, 1])
        return new_succ

def list_to_str(l):
    return ",".join(str(r) for r in l)


class State:
  def __init__(self, rw, visited, food_coord, directions = []):
    self.rw = rw
    self.visited = visited
    self.food_coord = food_coord
    self.directions = directions

  def __eq__(self, other):
    return other.visited[-1] == self.visited[-1]

  def __str__(self):
    return 'rolling_weight:' + str(self.rw), 'visited: '+ self.visited.__str__()+ '. directions:' + self.directions.__str__()
