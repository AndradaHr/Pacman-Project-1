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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    visited = set() #ca sa nu avem duplicate
    stack = util.Stack() #dfs foloseste stiva
    stack.push((problem.getStartState(), []))

    while not stack.isEmpty(): #cat timp stiva nu e goala,
        current_state, actions = stack.pop()  #procesam urmatoarea stare din stiva
        if problem.isGoalState(current_state): #daca e starea finala, returnam lista de actiuni pana in acel punct
            return actions
        if current_state not in visited:
            visited.add(current_state)
            successors = problem.getSuccessors(current_state)
            for successor, action, stepCost in successors:
                new_actions = actions + [action]
                stack.push((successor, new_actions))
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    visited = set()  #folosim set ca sa nu revizitam noduri( un nod apare o singura data in visited )
    queue = util.Queue() #bfs foloseste coada
    queue.push((problem.getStartState(), [])) #incepem parcurgerea cu starea initiala, nu avem nicio actiune
    # in start state, deci al doilea parametru e o lista goala

    while not queue.isEmpty(): #cat timp coada nu e goala,
        current_state, actions = queue.pop() #procesam urmatoarea stare din coada
        if problem.isGoalState(current_state): #daca starea curenta procesata e starea finala
            #returnam lista de actiuni care ne-a adus in acest punct
            return actions
        if current_state not in visited:
            visited.add(current_state) #daca starea curenta nu a fost deja vizitata, o adaugam in lista visited
            successors = problem.getSuccessors(current_state)
            for succesor, action, stepCost in successors: #procesam succesorii starii curente
                #fiecare succesor e o tupla de 3 elemente (successor, action, stepCost)
                new_actions = actions + [action] #extindem lista de actiuni cu noua actiune necesara pt a
                #ajunge in punctul curent
                queue.push((succesor, new_actions)) #adaugam succesorul cu lista updatata de actiuni in coada
                #pentru a-l procesa ulterior
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    #initializam priority queue, adaugam starea initiala in coada,impreuna cu o lista goala de actiuni si costul
    priorityQueue = util.PriorityQueue()
    priorityQueue.push((problem.getStartState(), [], 0), 0)  # (state, actions, cost)
    visited = set() #cream un set pt evidenta nodurilor vizitate

    #cat timp avem elemente in coada
    while not priorityQueue.isEmpty():
        # extragem nodul curent, actiunile efectuate pana la acesta si costul acumulat
        current_state, actions, current_cost = priorityQueue.pop()
        # verificam daca am ajuns la starea scop
        if problem.isGoalState(current_state):
            return actions
        # daca nodul nu a fost vizitat
        if current_state not in visited:
            """marcam nodul ca fiind vizitat si examinam succesorii nodului curent
                la fiecare pas cream o lista noua de actiuni,
                  adaugam actiunea curenta,
                  calculam noul cost cumulativ
                  si adaugam succesorul in coada de prioritate cu noul cost"""
            visited.add(current_state)
            for successor, action, nextCost in problem.getSuccessors(current_state):
                new_actions = actions + [action]
                new_cost = current_cost + nextCost
                priorityQueue.push((successor, new_actions, new_cost), new_cost)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    visited = set() #cream un set pt evidenta nodurilor vizitate
    # initializam priority queue, adaugam starea initiala in coada,impreuna cu o lista goala de actiuni si costul
    priorityQueue = util.PriorityQueue()
    start_state = problem.getStartState()
    # (state, actions, cost), priority
    priorityQueue.push((start_state, [], 0), 0)

    # cat timp avem elemente in coada
    while not priorityQueue.isEmpty():
        # extragem nodul curent, actiunile efectuate pana la acesta si costul acumulat
        current_state, actions, current_cost = priorityQueue.pop()
        # verificam daca am ajuns la starea scop
        if problem.isGoalState(current_state):
            return actions
        # daca nodul nu a fost vizitat
        if current_state not in visited:
            """marcam nodul ca fiind vizitat si examinam succesorii nodului curent
                 la fiecare pas cream o lista noua de actiuni,
                    cream o noua lista de actiuni,
                    calculam noul cost total,
                    adaugam costul euristic la costul total,
                    si adaugam succesorul in coada cu noul cost total, incluzand costul euristic"""

            visited.add(current_state)
            for successor, action, nextCost in problem.getSuccessors(current_state):
                new_actions = actions + [action]
                new_cost = current_cost + nextCost
                heuristic_cost = new_cost + heuristic(successor, problem)
                priorityQueue.push((successor, new_actions, new_cost), heuristic_cost)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
