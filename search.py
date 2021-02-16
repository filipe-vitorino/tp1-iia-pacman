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
    return [s, s, w, s, w, w, s, w]


def dfsUtil(problem, visitados, atual, caminho):
    
    termiei = False
    if (problem.isGoalState(atual)):
        return True

    visitados.add(atual)     
    vizinhos = problem.getSuccessors(atual)
    
    for no in vizinhos:
        if (no[0] not in visitados):
            caminho.push(no)
            termiei = dfsUtil(problem, visitados , no[0], caminho)            
            
            if (termiei):
                return True


    if (not termiei):
        caminho.pop()

    return False    


#https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
#https://pt.wikipedia.org/wiki/Busca_em_profundidade
#https://www.geeksforgeeks.org/iterative-depth-first-traversal/?ref=leftbar-rightbar
def depthFirstSearch(problem):
    
    """
    
    Search the deepest nodes in the search tree first. ''
    
    """
    
    visitados = set()
    atual = problem.getStartState()
    caminho  = util.Stack()
    result = []
    
    dfsUtil(problem, visitados, atual, caminho)
    
    while(not caminho.isEmpty()):
        x =  caminho.pop()
        result.append(x[1]) 
        """ 
        if (x[1] == 'South'):
            result.append(s)
        if (x[1] == 'West'):
            result.append(w)
        if (x[1] == 'East'):
            result.append(e)
        if (x[1] == 'Noth'):
            result.append(n)
        """
    result.reverse()
    return result

#https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
#https://en.wikipedia.org/wiki/Breadth-first_search
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    fila = util.Queue()
    visitados = set()
    caminho = {}
    result = []

    fila.push( (problem.getStartState(), "") )
    visitados.add(problem.getStartState())

    #Visita todos os nos por bfs
    while (not fila.isEmpty()):
        
        atual, x = fila.pop()
        caminho[atual] = x 
        
        if(problem.isGoalState(atual)):
            break
        
        vizinhos = problem.getSuccessors(atual)
        
        for no in vizinhos:
            #if (problem.isGoalState(no[0])):
                #caminho[no[0]] = (atual, no[1])   
                #break
            if (no[0] not in visitados):
                fila.push( (no[0], (atual,no[1])) ) 
                visitados.add(no[0])
                
    

    #backtrack para montar o caminho da solucao
    ite = list(caminho.keys())[-1]
    while ite != problem.getStartState(): 
        result.append(caminho[ite][1])
        #print(ite, caminho[ite])
        ite = caminho[ite][0]
  
    #solucao   
    result.reverse()
    return result

   

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    fila = util.PriorityQueue()
    visitados = set()
    caminho = {}
    result = []
    fila.push( (problem.getStartState() ,"", 0), 0 )
    visitados.add(problem.getStartState())
    
    #Visita todos os nos por bfs
    while  (not fila.isEmpty()):    

        atual, x, custo = fila.pop()
        caminho[atual] = x 
        
        if(problem.isGoalState(atual)):
            break
        
        vizinhos = problem.getSuccessors(atual)
        
        for no in vizinhos:
            if (no[0] not in visitados):
                fila.update( (no[0], (atual,no[1]), custo + no[2]), custo + no[2]) 
                if (not problem.isGoalState(no[0])):
                    visitados.add(no[0])
        
        #caminho[atual] = x 
   
    ite = list(caminho.keys())[-1]
    while ite != problem.getStartState(): 
        result.append(caminho[ite][1])
        ite = caminho[ite][0]
    
    #solucao
    result.reverse()
    #print(result)

    return result

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

#https://en.wikipedia.org/wiki/Maze_solving_algorithm
#http://bryukh.com/labyrinth-algorithms
def greedySearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest heuristic first."""

    atual = problem.getStartState()
    fila = util.PriorityQueue()
    visitados = set()
    caminho = {}
    result = []    
    heurist_value = heuristic(problem.getStartState(), problem)
    
    fila.push( (problem.getStartState() ,""), heurist_value) 
    visitados.add(problem.getStartState())  
    
    #Visita todos os nos por bfs
    while  (not fila.isEmpty()):             

        atual, x = fila.pop()
        caminho[atual] = x 

        if(problem.isGoalState(atual)):
            break
        
        vizinhos = problem.getSuccessors(atual)

        for no in vizinhos:
            if (no[0] not in visitados):
                heurist_value = heuristic(no[0], problem)
                fila.push( (no[0], (atual,no[1])), heurist_value) 
                visitados.add(no[0])
                
                
    #backtrack para montar o caminho da solucao
    ite = list(caminho.keys())[-1]
    
    while ite != problem.getStartState(): 
        result.append(caminho[ite][1])
        ite = caminho[ite][0]
    
    result.reverse()

    return result

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"


    open_list = util.PriorityQueue()
    close_list = set()

    caminho = {}
    g_cost = {}    

    result = []    

    atual = problem.getStartState()
    #heurist_value = heuristic(atual, problem)
    
    open_list.push(atual, 0) 
    caminho[atual] = ("", "")
    g_cost[atual] = 0

    while(not open_list.isEmpty()):             
        
      #  open_list.printa()
        atual = open_list.pop()        
        #print(g_cost[atual] + heuristic(atual, problem))
        #caminho[atual] = x 
        if(problem.isGoalState(atual)):
            final = atual
            break
        
        close_list.add(atual)
        vizinhos = problem.getSuccessors(atual)
        
        for no in vizinhos:
            tentative_gCost = g_cost[atual] + no[2] 
            #
            if no[0] in close_list and tentative_gCost >= g_cost[no[0]]:
                continue
            if (no[0] not in g_cost or tentative_gCost < g_cost[no[0]]):
                caminho[no[0]] = (atual, no[1])
                g_cost[no[0]] = tentative_gCost
                h_cost = heuristic(no[0], problem)
                f_cost = g_cost[no[0]] + h_cost
                open_list.update(no[0], f_cost) 
            #if( no[0] not in close_list or tentative_gCost < g_cost[no[0]]):


    itr = caminho[final] 
    while(itr[0] != "" ):
       # print("to em :", itr[1])
        result.append(itr[1] )
        itr = caminho[itr[0]]
        #result.append(caminho[itr[0]][1])

    result.reverse()
    #print(result)
    #backtrack para montar o caminho da solucao
    """
    https://www.redblobgames.com/pathfinding/a-star/introduction.html
    https://www.youtube.com/watch?v=-L-WgKMFuhE
    https://en.wikipedia.org/wiki/A*_search_algorithm
"""
    return result


def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    print (foodGrid.asList())
    
    "*** YOUR CODE HERE ***"
    return 1


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
gs = greedySearch
astar = aStarSearch
