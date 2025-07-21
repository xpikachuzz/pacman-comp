import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance

import numpy as np

def reject_outliers(l, m = 2.):
    '''
    https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
    '''
    l = np.array(l)
    no_outlier = l[(l>np.quantile(l,0.1)) & (l<np.quantile(l,0.9))].tolist()
    if len(no_outlier) == 0:
        return l
    return l[(l>np.quantile(l,0.1)) & (l<np.quantile(l,0.9))].tolist()

def scoreEvaluationFunction(state):
    """

    """
    def valid_food(cut_off = np.inf):
        foods = state.getFood().asList()
        valid_food = []
        for coord in foods:
            if util.manhattanDistance(coord, pacman_pos) < cut_off:
                valid_food.append(util.manhattanDistance(coord, pacman_pos))
        return valid_food

    def valid_ghost(cut_off = np.inf):
        ghost_list = state.getGhostPositions()
        valid_ghost = []
        for coord in ghost_list:
            if util.manhattanDistance(coord, pacman_pos) < cut_off:
                valid_ghost.append(util.manhattanDistance(coord, pacman_pos))
        return valid_ghost
    

    current_score = state.getScore()
    pacman_pos = state.getPacmanPosition()
    capsule_list = state.getCapsules()

    ghost_list_wTimer = []
    for g in state.getGhostStates():
        ghost_list_wTimer.append([g.getPosition(), g.scaredTimer])
=======
def getDetails(state: GameState):
    def valid_food(cut_off = np.inf):
        foods = state.getFood().asList()
        valid_food = []
        for coord in foods:
            if util.manhattanDistance(coord, pacman_pos) < cut_off:
                valid_food.append(util.manhattanDistance(coord, pacman_pos))
        return valid_food

    def valid_ghost(cut_off = np.inf):
        ghost_states = state.getGhostStates()
        valid_ghost = []
        for ghost_state in ghost_states:
            if util.manhattanDistance(ghost_state.getPosition(), pacman_pos) < cut_off:
                # if the ghost is scared and close enough to catch then chase him
                if ghost_state.scaredTimer > util.manhattanDistance(ghost_state.getPosition(), pacman_pos)+3:
                    chase = True
                else: chase = False
                valid_ghost.append([util.manhattanDistance(ghost_state.getPosition(), pacman_pos), chase])

        return valid_ghost
    
    def valid_capsule(cut_off = np.inf):
        capsule_pos = state.getCapsules()
        valid_cap = []
        for pos in capsule_pos:
            if util.manhattanDistance(pos, pacman_pos) < cut_off:
                # if the ghost is scared and close enough to catch then chase him
                valid_cap.append(util.manhattanDistance(pos, pacman_pos))

        return valid_cap
    

    current_score = state.getScore()
    pacman_pos = state.getPacmanPosition()
    return pacman_pos, current_score, valid_capsule(), valid_ghost(), valid_food()

def scoreEvaluationFunction(state: GameState):
    """
    Time complexity is O(capsule + ghost + food)
    """
    pacman_pos, current_score, capsule_list, ghost_dist, food_dist = getDetails(state)
>>>>>>> af9390724656f3d9eb28f4855f9bb9d81322d681

    # If pacman wins the game
    if state.isWin() or state.isLose():
        return current_score

    # Get the distance from pacman to the closest food
<<<<<<< HEAD
    food_dist = valid_food()
    closest_food = min(food_dist)
    # Get the distances from pacman to the closest ghost
    ghost_dist = valid_ghost()
    if len(ghost_dist) == 0:
        closest_ghost = np.inf
    else: 
        closest_ghost = min(ghost_dist)
    # Get the number of foods left
    nb_foods_left = state.getNumFood()
    # Compute score
    # if ghost is a certain distance away then encourage pac to adventure
    ghost_chase = -3
    #if closest_ghost > 5:
    #    ghost_chase = 3
    score = (1 * current_score + ghost_chase * (1/closest_ghost) + 5 * 1/closest_food )
=======
    if len(food_dist) == 0:
        closest_food = np.inf
    else: 
        closest_food = min(food_dist)

    # Get the distances from pacman to the closest ghost, and is the ghost scared?
    if len(ghost_dist) == 0:
        closest_ghost = np.inf
    else: 
        closest_ghost = np.inf
        min_chase = False
        for [dist, chase] in ghost_dist:
            if dist < closest_ghost:
                closest_ghost, min_chase = dist, chase

    # get the closest capsule. Ignore it if the closest ghost is faraway
    if len(capsule_list) == 0:
        closest_cap = 0
    else:
        # if closest ghost is close then eat
        if closest_ghost < 3:
            closest_cap = 5*1/min(capsule_list)
        else: closest_cap = 0

    # Compute score
    # if closest ghost is scared then chase it
    ghost_chase = -10
    if (min_chase):# and (closest_ghost < 2):
        ghost_chase = 10

    #h_food
    if closest_food == 0: h_food = 0
    else: h_food = 7 * 1/closest_food

    # h_ghost
    if closest_ghost == 0: h_ghost = 0
    else: h_ghost = ghost_chase * (1/closest_ghost)

    score = (current_score + h_ghost + h_food) #+ closest_cap)
>>>>>>> af9390724656f3d9eb28f4855f9bb9d81322d681
    return score

class Q2_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    @log_function
    def getAction(self, gameState: GameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

            gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

            gameState.getNumAgents():   
            Returns the total number of agents in the game

        ● Eat a food dot: +10
        ● Eat a “scared” ghost: +200
        ● Eat the last food dot: +500
        """
        # Cycle through map
        #food, capsule, ghost = reachable_content(gameState)
<<<<<<< HEAD

        def max_score(state, depth, alpha, beta):
            # If the state is a terminal node, return the score.
            if state.isWin() or state.isLose():
                return [state.getScore()*0.75, 'null']
            # Otherwise examine every successor state and choose the move that is best for Max.
            best_score, best_action = -np.inf, Directions.STOP
            for action in state.getLegalActions(0):
                next_suc = state.generateSuccessor(0, action)
=======
        if len(gameState.getGhostPositions()) == 4: self.depth = 2

        def max_score(state, depth, alpha, beta):
            # If the state is a terminal node, return the modified score. O(1)
            if state.isWin() or state.isLose():
                return [state.getScore()*0.75, 'null']
            # O(1)
            best_score, best_action = -np.inf, Directions.STOP
            for action in state.getLegalActions(0): #O(b)
                next_suc = state.generateSuccessor(0, action)   # O(G)
>>>>>>> af9390724656f3d9eb28f4855f9bb9d81322d681
                candidate_value = min_score(next_suc, depth, 1, alpha, beta)
                if candidate_value > best_score:
                    best_score, best_action = candidate_value, action
                    alpha = max(best_score, alpha)
                if best_score >= beta:
                    break

<<<<<<< HEAD
            # if on the path to returning then return action
            return [best_score, best_action]

        def min_score(state, depth, agent_id, alpha, beta):
            # If the state is a terminal node, return its utility.
            if state.isLose() or state.isWin():
                return state.getScore()
            next_ghost = (agent_id + 1) % state.getNumAgents()
            #if next_ghost == state.getNumAgents():
            #    next_ghost = 0
            best_score = np.inf
            score = best_score
            scores = []
            for action in state.getLegalActions(agent_id):
                # Is the next agent pacman?
                if next_ghost == 0: 
                    # Has max depth been reached?
                    if depth == self.depth - 1:
                        score = self.evaluationFunction(state.generateSuccessor(agent_id, action))
                    else:
                        [score, _] = max_score(state.generateSuccessor(agent_id, action), depth + 1, alpha, beta)
                else:
                    score = min_score(state.generateSuccessor(agent_id, action), depth, next_ghost, alpha, beta)
                scores.append(score)
                if score < best_score:
                    best_score = score
                    beta = min(beta, best_score)
                if best_score <= alpha:
                    break
            return best_score

        [score, direc] = max_score(gameState, 0, float('-inf'), float('inf'))
=======
            return [best_score, best_action]

        def min_score(state, depth, agent_id, alpha, beta):
            # If the state is a terminal node, return its utility. O(1)
            if state.isLose() or state.isWin():
                return state.getScore()
            best_score = np.inf
            candidate_value = best_score
            next_agent = (agent_id + 1) % state.getNumAgents()
            scores = []
            for action in state.getLegalActions(agent_id): #O(b)
                # Is the next agent pacman?
                if next_agent == 0:
                    # Has max depth been reached?
                    if depth == self.depth - 1:
                        candidate_value = self.evaluationFunction(state.generateSuccessor(agent_id, action))
                    else:
                        [candidate_value, _] = max_score(state.generateSuccessor(agent_id, action), depth + 1, alpha, beta)
                else:
                    candidate_value = min_score(state.generateSuccessor(agent_id, action), depth, next_agent, alpha, beta)
                scores.append(candidate_value)
                if candidate_value < best_score:
                    best_score = candidate_value
                    beta = min(beta, best_score)
                if best_score <= alpha:
                    break
            return averageArr(scores) ## return best_score if you don't want expecti_search

        [candidate_value, direc] = max_score(gameState, 0, -np.inf, np.inf)
>>>>>>> af9390724656f3d9eb28f4855f9bb9d81322d681
        return direc


class Node:
    def __init__(self, coord, neighbour = [], heur = 0):
        self.coord = coord
        self.neighbour = {}
        self.heur = heur
        self.visited = False

    def get_neighbour(self):
        return self.neighbour

def reachable_content(state):
    pac_node = Node(state.getPacmanPosition())
    nodes = {list_to_str(state.getPacmanPosition()): pac_node}

    # Create a queue for BFS
    stack = []

    # food, capsules, ghost
    food, capsule, ghost = {}, {}, {}

    ghost_pos = state.getGhostPositions()
    capsules_pos = state.getCapsules()

    # Mark the source node as
    # visited and enqueue it
    stack.append(pac_node)

    while len(stack) != 0:  #O(V)

        # get next node
        s = stack.pop()

        # Get all adjacent vertices of s
        neighbour_dict = get_neighbour(state, s)
        for node_dir in neighbour_dict.keys():  # O(E)
            node_coord = neighbour_dict[node_dir]
            if state.hasFood(node_coord[0], node_coord[1]):      #O(1)
                food[list_to_str(node_coord)] = node_coord
            elif (node_coord[0], node_coord[1]) in capsules_pos: #O(C)
                capsule[list_to_str(node_coord)] = node_coord
            if (node_coord[0], node_coord[1]) in ghost_pos:      #O(1)
                ghost[list_to_str(node_coord)] = node_coord
            neigh_node = nodes.get(list_to_str(node_coord), False)
            # If the neighbour is visited
            if neigh_node == False:
                opp_dir = inverse_dir(node_dir)
                new_node = Node(node_coord, {opp_dir: s})
                nodes[list_to_str(node_coord)] = new_node
                stack.append(new_node)
    return food.values(), capsule.values(), ghost.values()

def inverse_dir(direction):
    if direction == "North": return "South"
    if direction == "East": return "West"
    if direction == "South": return "North"
    if direction == "West": return "East"

def get_neighbour(state, node):
    '''
    Returns a dictionary with N,E,S,W keys linked to it's coordinate
    if the coordinate doesn't have a wall.
    '''
    def isWall(direc, coord):
        test_coord = [coord[0]+direc[0], coord[1]+direc[1]]
        try: 
            return state.hasWall(test_coord[0],test_coord[1])
        except:
            return True
    coord = node.coord
    neighbour = {}
    # check N
    next_coord_dir = [0, 1]
    if (not isWall(next_coord_dir, coord)):
        neighbour["North"] = [coord[0]+next_coord_dir[0], coord[1]+next_coord_dir[1]]
    # check E
    next_coord_dir = [1, 0]
    if (not isWall(next_coord_dir, coord)):
        neighbour["East"] = [coord[0]+next_coord_dir[0], coord[1]+next_coord_dir[1]]

    # check S
    next_coord_dir = [0, -1]
    if (not isWall(next_coord_dir, coord)):
        neighbour["South"] = [coord[0]+next_coord_dir[0], coord[1]+next_coord_dir[1]]
    
    # check W
    next_coord_dir = [-1, 0]
    if (not isWall(next_coord_dir, coord)):
        neighbour["West"] = [coord[0]+next_coord_dir[0], coord[1]+next_coord_dir[1]]
    return neighbour

def averageArr(arr):
    sum = 0
    for term in arr:
        sum += term
    return sum/len(arr)

# When are 2 states equal?
def heurisitc(currPos, food_pos, capsule_pos, ghost_pos):
    pass

def list_to_str(l):
    return ",".join(str(r) for r in l)
