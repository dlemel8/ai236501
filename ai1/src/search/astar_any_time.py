#############################
##                         ##
##   A* Search Algorithm   ##
##                         ##
#############################

# This is an implementation of the SearchAlgorithm interface for the following
# search algorithms:
# - A*
# - IterativeDeepeningAStar
#
# The IterativeDeepeningAStar variant allows you to search with A* using layers
# of depth in the graph, with each search increasing the maximum depth.

from algorithm import Heuristic, SearchAlgorithm
from graph import GraphSearchAnyTime
from utils import *
import time

class AStarAnyTime (SearchAlgorithm):
    '''
    Implementation of the A* search algorithm for the Problem.
    It may also take a maximum depth at which to stop, if needed.
    '''

    def __init__(self, max_time, algo_to_invoke, max_depth=infinity, beam_width=infinity):
        '''
        Constructs the A* search.
        Optionally, a maximum depth may be provided at which to stop looking for
        the goal state.
        '''
        self.start_time = time.clock()
        self.max_time = max_time
        self.algo_to_invoke = algo_to_invoke
        self.max_depth = max_depth

    def find(self, problem_state, heuristic):
        '''
        A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search.
        Uses the pathmax trick: f(n) = max(f(n), g(n)+h(n)).

        @param problem_state: The initial state to start the search from.
        @param heuristic: A heuristic function that scores the Problem states.
        '''
        # This is the node evaluation function for the given heuristic.
        def evaluator(node):
            if (self.start_time + self.max_time) < (time.clock() + time_safty):
                return 0
            return node.path_cost + heuristic.evaluate(node.state)
    
        # This is a generator for the PriorityQueue we need.
        def queue_generator():
            return PriorityQueue(evaluator)

        # Use a graph search with a minimum priority queue to conduct the search.
        search = GraphSearchAnyTime(self.start_time, self.max_time, self.algo_to_invoke, queue_generator, self.max_depth)
        return search.find(problem_state)

class IterativeDeepeningAStar (SearchAlgorithm):
    '''
    Implementation of the A* search algorithm for the Problem.
    This implementation limits the depth of each of the searches performed by
    the AStar algorithm, and iteratively increases this depth up to an optional
    limit that is supplied at construction (or to infinity if unspecified).
    '''

    def __init__(self, max_depth=sys.maxint):
        '''
        Constructs the search algorithm with an optional max depth.
        '''
        self.max_depth = max_depth

    def find(self, problem_state, heuristic):
        '''
        A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search.
        Uses the pathmax trick: f(n) = max(f(n), g(n)+h(n)).
        
        @param problem_state: The initial state to start the search from.
        @param heuristic: A heuristic function that scores the Problem states.
        '''
        for depth in xrange(1, self.max_depth):
            search = AStarAnyTime(self.time, depth)
            solution = search.find(problem_state, heuristic)
            if solution:
                return solution
        return None
