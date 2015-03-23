# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import time
from game import Agent

#global nodeCount

#nodeCount = 0
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
#        print(nodeCount)
#        print(time.time())
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
#        global nodeCount
#        nodeCount += 1

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
        oldFood = currentGameState.getFood();
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        totalScore = 0.0

        #counting score for ghosts in scaredtimer as well as normal state
        #   if scared we add +2000 else we add -1000, so that we move away
        #Also we are doing that for distance 0-2 so that we go closer
        #   to scared ghosts and away when they are closer
        #Also dividing by distance so that if we are closer, we get more points

        for ghost in newGhostStates:
            dist = manhattanDistance(ghost.getPosition(), newPos)
            if dist < 1:
                totalScore += 750*(-1+2*ghost.scaredTimer)/(dist+1)

        #if capsule is closer we get more value else less
        for capsule in currentGameState.getCapsules():
            dist = manhattanDistance(capsule,newPos)
            totalScore+=1000/(dist+1)

        #we check and add value of food we have eaten and also if food is closer
        # we add the value so that we get closer.
        for x in xrange(oldFood.width):
            for y in xrange(oldFood.height):
                if oldFood[x][y]:
                    d=manhattanDistance((x,y),newPos)
                    if(d==0):
                        totalScore += 750
                    else:
                        totalScore += 50/(d*d)
        return totalScore

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

#nodeCount=0

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def miniMax(self, gameState, depth, agentIndex=0):
#        global nodeCount
#        nodeCount += 1

        #check for game ending
        if gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState),None)

        #check for end of tree
        if depth == 0:
            return (self.evaluationFunction(gameState),None)

        numAgents = gameState.getNumAgents()
        #check current agent is the last agent and decrement the depth
        if agentIndex == numAgents-1:
            depth -= 1

        newAgentIndex = agentIndex + 1
        if newAgentIndex == numAgents:
            newAgentIndex = 0

        actionList = []
        for legalAction in gameState.getLegalActions(agentIndex):
            actionList.append(\
                (self.miniMax(gameState.generateSuccessor(agentIndex,legalAction),\
                              depth,\
                              newAgentIndex)[0],legalAction\
                )\
            )

        if(agentIndex == 0):    #: max node
            return max(actionList) #: return action that gives max score
        else:                   #: min node
            return min(actionList)  #: return action that gives min score

    def getAction(self, gameState):

        """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
#        print(nodeCount)
        #print(time.time())
        return self.miniMax(gameState, self.depth)[1]

#nodeCount = 0

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxPrune(self, gameState, depth, agentIndex, alpha, beta):
#        global nodeCount
#        nodeCount += 1
        # init the variables
        maxVal = float("-inf")

        #if it is the final state return
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        #find legal actions for pacman and try to get the minimum value and compare against beta to prune
        for action in gameState.getLegalActions(0):

            temp = self.minPrune(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)

            # prune because pacman is not going to choose anything less than temp
            if temp > beta:
                return temp

            if temp > maxVal:
                maxVal = temp
                maxAction = action

            #reassign alpha
            alpha = max(alpha, maxVal)

        # if this is the first depth, then we're trying to return an ACTION to take. otherwise, we're returning a number
        if depth == 1:
            return maxAction
        else:
            return maxVal


    def minPrune(self, gameState, depth, agentIndex, alpha, beta):
#        global nodeCount
#        nodeCount += 1

        minVal = float("inf")
        numAgents = gameState.getNumAgents()

        #if its the leaf node, we return
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        #we run Minimax algorithm where in we explore all the legal moves
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)

            if agentIndex == numAgents - 1:
                if depth == self.depth:
                    temp = self.evaluationFunction(successor)
                else:
                    temp = self.maxPrune(successor, depth + 1, 0, alpha, beta)

            # pass this state on to the next ghost
            else:
                temp = self.minPrune(successor, depth, agentIndex + 1, alpha, beta)

            #prune as ghost will not want to take values less than alpha

            if temp < minVal:
                minVal = temp
                minAction = action
            if temp < alpha:
                return temp
            #update beta
            beta = min(beta, minVal)
        return minVal

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        maxAction = self.maxPrune(gameState, 1, 0, float("-inf"), float("inf"))
        global nodeCount
 #       print(nodeCount)
        return maxAction


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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

