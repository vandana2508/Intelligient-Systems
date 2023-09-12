# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** CS3568 YOUR CODE HERE ***"
        "Decribe your function:"
        # Finds the closest food or it sets the foodValue high if there is no food or on food.
        # Finds the closest ghost using manhattan distance.
        # The priority is given to ghost avoidance over acquiring the closest food.
        
        newFoodList = newFood.asList()
        foodCount = len(currentGameState.getFood().asList())
        newFoodCount = len(newFoodList)
        
        food = [util.manhattanDistance(newPos, food) for food in newFoodList]
        if len(food):
            foodValue = min(food)
        else:
            foodValue = 100

        ghostPosition = []
        for ghost in newGhostStates:
            ghostPosition.append(ghost.getPosition())
        ghosts = [util.manhattanDistance(newPos, ghost) for ghost in ghostPosition]
        ghostValue = min(ghosts)

        returnValue = 0
        if ghostValue < 3: returnValue = -100
        elif foodCount != newFoodCount: returnValue = 100
        else: returnValue = foodValue**-1
        return returnValue

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** CS3568 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        
        agents = gameState.getNumAgents()
        depth = self.depth * agents

        LegalActions = gameState.getLegalActions(0)
        if Directions.STOP in LegalActions: LegalActions.remove(Directions.STOP)
        successors = []
        for action in LegalActions:
            successors.append(gameState.generateSuccessor(0,action))

        valueSuccessor = []
        for state in successors:
            valueSuccessor.append(self.valueFunction(1, state, depth-1))
        maxValue = max(valueSuccessor)

        maxIndex = []
        for i in range(0,len(valueSuccessor)):
            if valueSuccessor[i] == maxValue: maxIndex.append(i)
        return LegalActions[random.choice(maxIndex)]
        util.raiseNotDefined()

    def valueFunction(self, agentIndex, gameState, depth):
        agents = gameState.getNumAgents()
        # if endstate or depth reached
        if (gameState.isWin() or gameState.isLose() or depth==0):
              return self.evaluationFunction(gameState)
        LegalActions = gameState.getLegalActions(agentIndex)
        if Directions.STOP in LegalActions: LegalActions.remove(Directions.STOP)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in LegalActions]

        # maximum-value
        if agentIndex == 0:
            return max([self.valueFunction((agentIndex+1)%agents, state, depth-1) for state in successors])
        # minimum-value
        else :
            return min([self.valueFunction((agentIndex+1)%agents, state, depth-1) for state in successors])


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** CS3568 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        alpha, beta = float("-inf"), float("inf")
        agents = gameState.getNumAgents()
        depth = self.depth * agents

        if (gameState.isWin() or gameState.isLose() or depth==0):
              return self.evaluationFunction(gameState)

        LegalActions = gameState.getLegalActions(0)
        if Directions.STOP in LegalActions: LegalActions.remove(Directions.STOP)
        bestAction = None
        bestValue = float("-inf")

        for action in LegalActions:
            successor = gameState.generateSuccessor(0, action)
            value = self.valueFunction((1)%agents, successor, depth-1, alpha, beta)
            if value > bestValue: bestValue, bestAction = value, action
            alpha = max(alpha, value)
        return bestAction


    def valueFunction(self, agentIndex, gameState, depth, a = float("-inf"), b = float("inf")):
        agents = gameState.getNumAgents()
        # if endstate or depth reached
        if (gameState.isWin() or gameState.isLose() or depth==0):
              return self.evaluationFunction(gameState)
        LegalActions = gameState.getLegalActions(agentIndex)
        if Directions.STOP in LegalActions: LegalActions.remove(Directions.STOP)
        # maximum-value
        if agentIndex == 0:
            value = float("-inf")
            for action in LegalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = max(value, self.valueFunction((agentIndex+1)%agents, successor, depth-1, a, b))
                if value > b: return value
                a = max(a, value)
            return value
        # minimum-value
        else :
            value = float("inf")
            for action in LegalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = min(value, self.valueFunction((agentIndex+1)%agents, successor, depth-1, a, b))
                if value < a: return value
                b = min(b, value)
            return value
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** CS3568 YOUR CODE HERE ***"
        "PS. It is okay to define your own new functions. For example, value, min_function,max_function"
        agents = gameState.getNumAgents() 
        depth = self.depth * agents
        
        LegalActions = gameState.getLegalActions(0)
        if Directions.STOP in LegalActions: LegalActions.remove(Directions.STOP)
        successors = []
        for action in LegalActions:
            successors.append(gameState.generateSuccessor(0,action))

        values = []
        for state in successors:
            values.append(self.valueFunction(1, state, depth-1))
        maxValue = max(values)

        maxIndices = []
        for i in range(0,len(values)):
            if values[i] == maxValue: maxIndices.append(i)
        return LegalActions[random.choice(maxIndices)]


    def valueFunction(self, agentIndex, gameState, depth):
        agents = gameState.getNumAgents()
        # if endstate or depth reached
        if (gameState.isWin() or gameState.isLose() or depth==0):
              return self.evaluationFunction(gameState)
        LegalActions = gameState.getLegalActions(agentIndex)
        if Directions.STOP in LegalActions: LegalActions.remove(Directions.STOP)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in LegalActions]

        # maximum-value
        if agentIndex == 0:
            return max([self.valueFunction((agentIndex+1)%agents, state, depth-1) for state in successors])
        # expexted-value
        else :
            values = [self.valueFunction((agentIndex+1)%agents, state, depth-1) for state in successors]
            return float(sum(values))/len(values)


        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Find the distance to all the foods from the current state using manhattan distance.
                 Find the distance to each ghost from the current state using manhattan distance.
                 Calculate the capsules count in the current game state.
                 Find the closest food distance
                 If the ghost is too close to pacman(<4) prioritize escaping rather than eating the food
                 Calculate the score from
                     score from current state
                     capsules left
                     closest food
                     food left
                     scared times
                     ghost distance
    """
    "*** CS3568 YOUR CODE HERE ***"
    # Setup information to be used as arguments in evaluation function
    pacmanPosition = currentGameState.getPacmanPosition()
    ghostPositions = currentGameState.getGhostPositions()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    foodList = currentGameState.getFood().asList()
    foodCount = len(foodList)
    capsuleCount = len(currentGameState.getCapsules())
    closestFood = 1

    gameScore = currentGameState.getScore()
    
    foodDistances = [manhattanDistance(pacmanPosition, food_position) for food_position in foodList]

    if foodCount > 0:
        closestFood = min(foodDistances)

    ghostDistance = [0]
    for ghostPosition in ghostPositions:
        ghost = manhattanDistance(pacmanPosition, ghostPosition)
        ghostDistance.append(ghost)
        if ghost < 4:
            closestFood = 99999
            
    sumScaredTimes = sum(newScaredTimes)
    sumGhostDistance = sum (ghostDistance)
    score = 0
    if sumScaredTimes > 0:    
        score +=   sumScaredTimes + (-1 * capsuleCount) + (-1 * sumGhostDistance)

    score += (10 * (1.0 / closestFood)) + (200 * gameScore) + (-100 * foodCount) + (-10 * capsuleCount)
    return score

    util.raiseNotDefined()
    

# Abbreviation
better = betterEvaluationFunction
