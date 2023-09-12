import util

class DFS(object):
    def depthFirstSearch(self, problem):
        """
        Search the deepest nodes in the search tree first
        [2nd Edition: p 75, 3rd Edition: p 87]

        Your search algorithm needs to return a list of actions that reaches
        the goal.  Make sure to implement a graph search algorithm
        [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:

        print "Start:", problem.getStartState()
        print "Is the start a goal?", problem.isGoalState(problem.getStartState())
        print "Start's successors:", problem.getSuccessors(problem.getStartState())
        """
        "*** TTU CS3568 YOUR CODE HERE ***"
        visitedStates = set()
        stack = util.Stack()
        startState = (problem.getStartState(), [])
        stack.push(startState)
        while True:
            if stack.isEmpty():
                return Failure
            node = stack.pop()
            state, path = node[0], node[1]
            if problem.isGoalState(state):
                return path
            if state not in visitedStates:
                visitedStates.add(state)
                for cState in problem.getSuccessors(state):
                    newState = cState[0]
                    newPath = node[1] + [cState[1]]
                    stack.push((newState, newPath))
        util.raiseNotDefined()

class BFS(object):
    def breadthFirstSearch(self, problem):
        "*** TTU CS3568 YOUR CODE HERE ***"
        visitedStates = set()
        queue = util.Queue()
        startState = (problem.getStartState(), [])
        queue.push(startState)
        while True:
            if queue.isEmpty():
                return Failure
            node = queue.pop()
            state, path = node[0], node[1]
            if problem.isGoalState(state):
                return path
            if state not in visitedStates:
                visitedStates.add(state)
                for cState in problem.getSuccessors(state):
                    newState = cState[0]
                    newPath = node[1] + [cState[1]]
                    queue.push((newState, newPath))
        util.raiseNotDefined()

class UCS(object):
    def uniformCostSearch(self, problem):
        "*** TTU CS3568 YOUR CODE HERE ***"
        visitedStates = set()
        priorityQueue = util.PriorityQueue()
        startState = (problem.getStartState(), [])
        priorityQueue.push(startState, 0)
        while True:
            if priorityQueue.isEmpty():
                return Failure
            node = priorityQueue.pop()
            state, path = node[0], node[1]
            if problem.isGoalState(state):
                return path
            if state not in visitedStates:
                visitedStates.add(state)
                for cState in problem.getSuccessors(state):
                    newState = cState[0]
                    newPath = node[1] + [cState[1]]
                    cost = cState[2]
                    priorityQueue.push((newState, newPath), cost + problem.getCostOfActions(newPath))
        util.raiseNotDefined()
        
class aSearch (object):
    def nullHeuristic( state, problem=None):
        """
        A heuristic function estimates the cost from the current state to the nearest goal in the provided SearchProblem.  This heuristic is trivial.
        """
        return 0
    def aStarSearch(self,problem, heuristic=nullHeuristic):
        "Search the node that has the lowest combined cost and heuristic first."
        "*** TTU CS3568 YOUR CODE HERE ***"
        visitedStates = set()
        priorityQueue = util.PriorityQueue()
        # startNode = (state, pathList, g-cost, h-cost, f-cost)
        h = heuristic(problem.getStartState(), problem)
        startState = (problem.getStartState(), [], 0, h, h)
        priorityQueue.push(startState, heuristic)
        while True:
            if priorityQueue.isEmpty():
                return Failure
            node = priorityQueue.pop()
            state, path, g, h, f = node
            if problem.isGoalState(state):
                return path
            if state not in visitedStates:
                visitedStates.add(state)
                for cState in problem.getSuccessors(state):
                    newState, newPath, newG = cState[0], (node[1] + [cState[1]]), (node[2] + cState[2])
                    newH = heuristic(newState, problem)
                    newF = newG + newH
                    priorityQueue.push((newState, newPath, newG, newH, newF), newF)
        
        util.raiseNotDefined()

