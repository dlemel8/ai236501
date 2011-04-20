from search.algorithm import Heuristic
from search.uninformed import BreadthFirstGraphSearch
from copy import deepcopy
import sys

def die(str):
    print '[KOL HABASA] ' + str
    sys.exit(0)

class CleanHeuristic(Heuristic):
    def evaluate(self, state):
        return len(state.dirt_locations)
    
class ShortestPathHeuristic(Heuristic):
    def find_solution(self, state, dirt):
        state.dirt_locations = frozenset([dirt])
        solution = BreadthFirstGraphSearch().find(state, 5)
        if not solution:
            die("BreadthFirstGraphSearch didn't found solution")
        return solution
    
    def evaluate(self, state):
        realDirts = deepcopy(state.dirt_locations)
        sols = [len(self.find_solution(state, dirt)) for dirt in realDirts]
        minVal = reduce(min, sols, state.width * state.height)
        state.dirt_locations = realDirts
        return minVal + state.width * state.height * len(state.dirt_locations)

class IgnoreObstaclesHeuristic(Heuristic):
    def dist(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def evaluate(self, state):
        totalMinVal = state.width * state.height * len(state.dirt_locations) * len(state.robots)
        for robot in state.robots:
            dists = [self.dist(dirt, robot) for dirt in state.dirt_locations]
            totalMinVal += reduce(min, dists, state.width * state.height)
        return totalMinVal