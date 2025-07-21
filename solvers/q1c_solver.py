#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

def q1c_solver(problem: q1c_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result


class State:
  def __init__(self, rw, visited, food_coord, directions = [], food_found_cost = [], food_unreachable = False):
    self.rw = rw
    self.visited = visited
    self.food_coord = food_coord
    self.directions = directions
    self.food_found_cost = []
    self.food_unreachable = food_unreachable

  def __eq__(self, other):
    return other.visited[-1] == self.visited[-1]

  def __str__(self):
    return 'rolling_weight:' + str(self.rw) + '. visited: ' + self.visited.__str__() + '. directions:' + self.directions.__str__()


class Node:
    def __init__(self, coord, neighbour = [], heur = 0):
        self.coord = coord
        self.neighbour = {}
        self.heur = heur
        self.visited = False

    def get_neighbour(self):
        return self.neighbour


class AStarData:
    # YOUR CODE HERE
    def __init__(self):
        self.heuristic = []
        self.open = util.PriorityQueue()
        self.closed = []

def dfs(s, goal_coords):
    '''
    arg:
        s: Node you begin from
        goal_coords: List of goals to be found
    '''
    stack = []      # holds nodes
    s.visited = True
    stack.append(s)

    while len(stack) != 0:
        nex = stack.pop()
        nex.visited = True
        # check if this node is food?
        if nex.coord in goal_coords:
            goal_coords.remove(nex.coord)

        # go through neighbours
        for key in nex.neighbour:
            node = nex.neighbour[key]
            if not node.visited:
                stack.append(node)

    return goal_coords

def astar_initialise(problem: q1c_problem):
    # YOUR CODE HERE
    astarData = AStarData()
    
    # Create graph
    pac_pos = problem.startingGameState.getPacmanPosition()
    pac_pos = [pac_pos[0], pac_pos[1]]      # convert to list (was tuple)
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
                    food.append([x,y])

    ## check which foods are reachable from starting
    # dfs from starting position
    unreachable_food = dfs(nodes[list_to_str(pac_pos)], food[::])
    reachable_food = [item for item in food if item not in unreachable_food]

    
    state = State(0, [pac_pos], reachable_food, [], [], len(reachable_food) == len(food))
    astarData.open.push(state, state.rw+astar_heuristic(state, []))
    problem.graph = nodes
    
    return astarData

def astar_loop_body(problem: q1c_problem, astarData: AStarData):
    # Get pacman's possible moves
    pacActions = problem.getStartState().getLegalPacmanActions()
    min_state = astarData.open.pop()

    # does this have food?
    if problem.getStartState().hasFood(min_state.visited[-1][0], min_state.visited[-1][1]) and (min_state.visited[-1] in min_state.food_coord):
        found_food = min_state.visited[-1]
        # remove from food_coord
        min_state.food_coord.remove(found_food)
        # extended visited
        min_state.visited.append([found_food])

        ## empty the remaining open set
        # define the new state
        astarData.open = util.PriorityQueue()
        astarData.closed = []
        min_state.visited = min_state.visited[-1][::]
        min_state.food_found_cost = min_state.food_found_cost + [[min_state.rw]]

    # run problem 1a, trying to find food_coords[1]
    if problem.isGoalState(min_state):
        # investigae min_state.food_found_cost to see if persuing
        print("food_found_cost: ", min_state.food_found_cost)
        # iterate over min_state.food_found_cost
        [direction_turn, max_val] = 0, 0
        for i in range(len(min_state.food_found_cost)):
            if i*10 > min_state.food_found_cost[i][0]:
                direction_turn = min_state.food_found_cost[i][0]
                max_val = i*10 - min_state.food_found_cost[i][0]
        ## Is finishing the game better?
        # is finishing game possible
        if min_state.food_unreachable:
            # score after finishing
            fin_val = len(min_state.food_found_cost)*10 + 500 - min_state.food_found_cost[i][0]
            if fin_val > max_val:
                max_val = fin_val
                direction_turn = min_state.food_found_cost[-1][0]
        print(type(min_state.directions[:direction_turn][0]))

        return [True, min_state.directions[:direction_turn]]

    # is this in closed? No need to check, we don't allow duplicate open elements
    astarData.closed.append(min_state)

    # Get successors.
    new_open = problem.getSuccessors(min_state)

    # get important open sets:
    for [new_state, action, cost] in new_open:
        # check if new_state is in open set. Only when new_state[visited] is in closed
        ## DOESn't make sense if I was visited
        if new_state not in astarData.closed:
            h = astar_heuristic(new_state, [])
            dist = new_state.rw+h
            new_state.food_found_cost = min_state.food_found_cost
            astarData.open.update(new_state, dist)

    # finishing game is not possible. Don't need to check?
    if astarData.open.isEmpty():
        # Aim to maximze food!
        direction_turn = 0
        for i in range(len(min_state.food_found_cost)):
            if i*10 > min_state.food_found_cost[i][0]:
                direction_turn = min_state.food_found_cost[i][0]
        #print(direction_turn, min_state.directions)
        return [True, min_state.directions[:direction_turn]]
        #return [True, min_state.directions[:min_state.food_found_cost[-1][-1]]]

    return [False, 1]




def astar_heuristic(current, goals = []):
    # Return the minimum to the heuristics to all the 
    small = float('inf')
    for coord in current.food_coord:
        #print("current:", current.visited[-1])
        if h_dist(current.visited[-1], coord) < small:
            small = h_dist(current.visited[-1], coord)

    return small

def h_dist(coord1, coord2):
    deltaX = abs(coord1[0] - coord2[0])
    deltaY = abs(coord1[1] - coord2[1])
    D = 1
    return D * (deltaX + deltaY)

def list_to_str(l):
    return ",".join(str(r) for r in l)

def heapify(list_pq):
    pq = util.PriorityQueue()
    for [elem, key] in list_pq:
        pq.push(elem, key)
    return pq

def printOpen(pq):
    elements = []
    while not pq.isEmpty():
        mini = pq.pop()
        elements.append(mini)
    for i in range(len(elements)):
        elements[i] = [elements[i], elements[i].rw + astar_heuristic(elements[i], [])]
        #print(elements[i][0], "\t\t key=", elements[i][1])
    return elements
