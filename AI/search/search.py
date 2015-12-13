# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import pdb

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def yy_dfs(state,problem,ans,mydict):
    mydict[state] = True
    if problem.isGoalState(state):
        return True
    nextstates = problem.getSuccessors(state)
    nextstates = nextstates[::-1]
    for nstate in nextstates:
        if nstate[0] in mydict : continue
        ans.append(nstate[1])
        if yy_dfs(nstate[0],problem,ans,mydict):
            return True
        else:
            ans.pop()
    return False

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    ans = []
    mydict = { }
    yy_dfs(problem.getStartState(),problem,ans,mydict)
    return ans
    #util.raiseNotDefined()

# bfs yy
def yy_bfs(problem):
    start_node = problem.getStartState()
    _queue = util.Queue()
    _queue.push(start_node)
    _dict = { }
    _path = { }
    _goalnode = None
    _dict[start_node] = True
    while _queue.isEmpty() == False:
        now_node = _queue.pop()
        #pdb.set_trace()
        if(problem.isGoalState(now_node)):
            _goalnode = now_node
            break
        next_nodes = problem.getSuccessors(now_node)
        for next_node in next_nodes:
            if next_node[0] not in _dict:
                _queue.push(next_node[0]) 
                _dict[next_node[0]] = True
                _path[next_node[0]] = now_node,next_node[1]
    ans = []
    tr = _goalnode
    while tr in _path:
        ans.append(_path[tr][1])
        tr = _path[tr][0]
    return ans[::-1]

    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    ans = yy_bfs(problem)
    return ans
    #util.raiseNotDefined()

def yy_ucs(problem):
    start_node = problem.getStartState()
    _queue = util.PriorityQueue()
    _queue.push(start_node,0)
    _dis = { }
    _visted = set()
    _path = { }
    _goalnode = None
    _dis[start_node] = 0
    while _queue.isEmpty() == False:
        now_node = _queue.pop()
        if now_node in _visted: continue
        else : _visted.add(now_node)
        #pdb.set_trace()
        if(problem.isGoalState(now_node)):
            _goalnode = now_node
            break
        next_nodes = problem.getSuccessors(now_node)
        for next_node in next_nodes:
            nextcost = _dis[now_node] + next_node[2]
            if next_node[0] not in _dis or _dis[next_node[0]] > nextcost:
                _dis[next_node[0]] = nextcost
                _queue.push(next_node[0],nextcost) 
                _path[next_node[0]] = now_node,next_node[1]
    ans = []
    tr = _goalnode
    while tr in _path:
        ans.append(_path[tr][1])
        tr = _path[tr][0]
    return ans[::-1]

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    ans = yy_ucs(problem)
    return ans
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def yy_astar(problem,heuristic):
    _queue = util.PriorityQueue()
    start_node = problem.getStartState()
    is_visited = set()
    _path = {}
    _dis = {}
    _dis[start_node] = 0
    flag = 0
    _queue.push(start_node,0)
    _my_goal = ""
    while _queue.isEmpty != False:
        now_node = _queue.pop()
        if problem.isGoalState(now_node) == True:
            flag =1
            _my_goal = now_node
            break
        if now_node in is_visited: continue
        else:is_visited.add(now_node)
        for next_node,action,cost in problem.getSuccessors(now_node):
            next_cost = _dis[now_node] + cost
            if next_node not in _dis or next_cost < _dis[next_node]:
                _dis[next_node] =  next_cost
                _queue.push(next_node,_dis[next_node] + heuristic(next_node,problem))
                _path[next_node] = now_node,action

    ans = []
    if flag:
        tr = _my_goal
        while tr in _path:
            ans.append(_path[tr][1])
            tr = _path[tr][0]
        return ans[::-1]
    raise "not find solution in astar"
        
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ans = yy_astar(problem,heuristic)
    return ans
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
