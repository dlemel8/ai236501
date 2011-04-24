###############################
##                           ##
##   Beam Search Algorithm   ##
##                           ##
###############################

# This is an implementation of the SearchAlgorithm interface for the following
# search algorithms:
# - BeamSearch

from algorithm import Heuristic, SearchAlgorithm
from graph import GraphSearchAnyTime
from utils import *
import time

class BeamSearchAnyTime (SearchAlgorithm):
    '''
    Implementation of the beam search algorithm for the Problem.
    It takes the beam width as a parameter, and it may also take a maximum depth
    at which to stop, if needed.
    '''

    def __init__(self, max_time, beam_width=infinity, max_depth=infinity):
        '''
        Constructs the beam search from the beam width. 
        Optionally, a maximum depth may be provided at which to stop looking for
        the goal state.
        '''
        self.start_time = time.clock()
        self.max_time = max_time
        self.beam_width = beam_width
        self.max_depth = max_depth

    def find(self, problem_state, heuristic):
        '''
        Beam search is best-first graph search with a beam width that determines
        how many states are in the open states. This conserves memory and
        focuses the search path on the short-term most likely candidates.

        @param problem_state: The initial state to start the search from.
        @param heuristic: A heuristic function that scores the Problem states.
        '''
        # This is the node evaluation function for the given heuristic.
        def evaluator(node):
            if (self.start_time + self.max_time) < (time.clock() + time_safty):
                return 0
            return heuristic.evaluate(node.state)
    
        # This is a generator for the LimitedPriorityQueue we need.
        def queue_generator():
            return LimitedPriorityQueue(evaluator, self.beam_width)

        # Use a graph search with a minimum priority queue to conduct the search.
        search = GraphSearchAnyTime(self.start_time, self.max_time, queue_generator, self.max_depth)
        return search.find(problem_state)
