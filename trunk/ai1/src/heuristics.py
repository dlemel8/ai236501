from search.algorithm import Heuristic
from search.uninformed import BreadthFirstGraphSearch
from search.utils import infinity
from copy import deepcopy
import sys

class CleanHeuristic(Heuristic):
    def evaluate(self, state):
        return len(state.dirt_locations)
    
class BdioHeuristic(Heuristic):
    def evaluate(self, state):
        realDirts = deepcopy(state.dirt_locations)
        minVal = state.width * state.height
        for dirt in realDirts:
            state.dirt_locations = frozenset([dirt])
            solution = BreadthFirstGraphSearch().find(state, 5)
            if not solution:
                print "KOL HABASA"
                sys.exit(0)
            minVal = min(len(solution), minVal)
        
        state.dirt_locations = realDirts 
        return minVal + state.width * state.height * len(state.dirt_locations)

class BlaHeuristic(Heuristic):
    def dist(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def evaluate(self, state):
        
        totalMinVal = state.width * state.height * len(state.dirt_locations) * len(state.robots)
        
        for robot in state.robots:
            minVal = state.width * state.height
            for dirt in state.dirt_locations:
                minVal = min(minVal, self.dist(dirt, robot))
            
            totalMinVal += minVal
            
        return totalMinVal