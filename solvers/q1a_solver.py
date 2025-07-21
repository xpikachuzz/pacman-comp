#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1a_problem import q1a_problem

def q1a_solver(problem: q1a_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

#-------------------#
# DO NOT MODIFY END #
#-------------------#

from game import Directions



class State:
  def __init__(self, rw, visited, food_coord, directions = []):
    self.rw = rw
    self.visited = visited
    self.food_coord = food_coord
    self.directions = directions

  def __eq__(self, other):
    return other.visited[-1] == self.visited[-1]

  def __str__(self):
    return 'rolling_weight:' +  str(self.rw) + 'visited: ' + self.visited.__str__() + '. directions:' + self.directions.__str__()

class Node:
    def __init__(self, coord, neighbour = [], heur = 0):
        self.coord = coord
        self.neighbour = {}
        self.heur = heur

    def get_neighbour(self):
        return self.neighbour


class AStarData:
    # YOUR CODE HERE
    def __init__(self):
        self.heuristic = []
        self.open = util.PriorityQueue()
        self.closed = []


def list_to_str(l):
    return ",".join(str(r) for r in l)

def astar_initialise(problem: q1a_problem):
    # YOUR CODE HERE
    astarData = AStarData()
    
    # Create graph
    pac_pos = problem.startingGameState.getPacmanPosition()
    nodes = {list_to_str(pac_pos): Node(pac_pos)}
    foodArray = problem.startingGameState.getFood()     # Un-needed, just use hasFood
    walls = problem.startingGameState.getWalls()
    food = []
    for y in range(walls.height):
        for x in range(walls.width):
            # don't implement if it's a wall
            if not problem.getStartState().hasWall(x, y):
                node = nodes.get(list_to_str([x,y]), False)
                # create new node if don't it exits
                if not node:
                    nodes[list_to_str([x,y])] = Node([x,y])
                    node = nodes[list_to_str([x,y])]
                
                # create it's neighbours
                # check left
                if not nodes.get(list_to_str([x-1, y]), False):
                    # when left node doesn't exist
                    pass
                else:
                    # node already exits
                    node.neighbour['West'] = nodes[list_to_str([x-1, y])]
                # check up
                if not nodes.get(list_to_str([x, y-1]), False):
                    # when up node doesn't exist
                    pass
                else:
                    # node already exits
                    node.neighbour['South'] = nodes[list_to_str([x, y-1])]

                # check right
                if x+1 < walls.width:
                    if not nodes.get(list_to_str([x+1, y]), False):
                        # when right node doesn't exist
                        # then check if it's wall
                        if not problem.getStartState().hasWall(x+1, y):
                            # when not a wall you create a new node
                            nodes[list_to_str([x+1,y])] = Node([x+1, y])
                            node.neighbour['East'] = nodes[list_to_str([x+1,y])]
                    else:
                        # node already exits
                        node.neighbour['East'] = nodes[list_to_str([x+1, y])]

                # check down
                if y+1 < walls.height:
                    if not nodes.get(list_to_str([x, y+1]), False):
                        # when down node doesn't exist
                        # then check if it's wall
                        if not problem.getStartState().hasWall(x, y+1):
                            # when not a wall you create a new node
                            nodes[list_to_str([x,y+1])] = Node([x, y+1])
                            node.neighbour['North'] = nodes[list_to_str([x,y+1])]
                            pass
                    else:
                        # node already exits
                        node.neighbour['North'] = nodes[list_to_str([x, y+1])]

                # is it a food slot
                if foodArray[x][y]:
                    food = [x,y]

    state = State(0, [pac_pos], food)
    astarData.open.push(state, state.rw+astar_heuristic(state, []))
    problem.graph = nodes
    return astarData

def astar_loop_body(problem: q1a_problem, astarData: AStarData):
    # Get pacman's possible moves
    #pacActions = problem.getStartState().getLegalPacmanActions()

    #if problem.open.isEmpty():
    #    return [True, []]

    # O(1)
    min_state = astarData.open.pop()

    #O(1)
    if problem.isGoalState(min_state):
        return [True, min_state.directions]

    # is this in closed? No need to check, we don't allow duplicate open elements
    #O(1)
    astarData.closed.append(min_state)

    # Get successors.
    # O(b*visited)
    new_open = problem.getSuccessors(min_state)
    #print("=================process new_state=================")
    #print("Closed:", astarData.closed)
    #print("NEW Open:", new_open)
    # get important open sets:
    # O(b)
    for [new_state, action, cost] in new_open:
        # check if new_state is in open set. Only when new_state[visited] is in closed
        ## DOESn't make sense if I was visited. It checks
        # O(closed) < O(b^d)
        if new_state not in astarData.closed:
            curr = min_state.visited[-1]
            new_curr = new_state.visited[-1]
            dist = new_state.rw+util.manhattanDistance(new_curr, new_state.food_coord)
            astarData.open.update(new_state, dist)  #O(log(|open|))
        #else:
        #    #print("in closed: ", new_state.__str__())
        #    for close in astarData.closed:
        #        if close == new_state:
        #            print("matching closed: ", close.__str__())

    return [False, 1]

def astar_heuristic(current, goal):
    return util.manhattanDistance(current.visited[-1], current.food_coord)

def heapify(list_pq):
    pq = util.PriorityQueue()
    for [elem, key] in list_pq:
        pq.push(elem, key)
    return pq

def printOpen(pq):
    elements = []
    while not pq.isEmpty():
        elements.append(pq.pop())
    for i in range(len(elements)):
        elements[i] = [elements[i], elements[i].rw + util.manhattanDistance(elements[i].visited[-1], elements[i].food_coord)]
    return elements
