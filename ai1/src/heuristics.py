from search.algorithm import Heuristic
from search.uninformed import BreadthFirstGraphSearch
from search.beam_search import BeamSearch
from copy import deepcopy
from search.utils import infinity
import sys
import itertools

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
            # fix it !!!!
            die("BreadthFirstGraphSearch didn't found solution")
        return solution
    
    def evaluate(self, state):
        realDirts = deepcopy(state.dirt_locations)
        sols = [len(self.find_solution(state, dirt)) for dirt in realDirts]
        minVal = reduce(min, sols, state.width * state.height)
        state.dirt_locations = realDirts
        return minVal + state.width * state.height * len(state.dirt_locations)
    
class AllmostShortestPathHeuristic(Heuristic):
    def dist(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def find_solution(self, state, dirt, robot):
        realDirts = deepcopy(state.dirt_locations)
        realRobots = deepcopy(state.robots)
        state.dirt_locations = frozenset([dirt])
        state.robots = tuple([robot])
        #solution = BreadthFirstGraphSearch().find(state, 5)
        solution = BeamSearch().find(state, IgnoreObstaclesHeuristic())
        state.dirt_locations = realDirts
        state.robots = realRobots
        if not solution:
            # fix it !!!!
            die("BreadthFirstGraphSearch didn't found solution")
        return solution
    
    def evaluate(self, state):
        firstMinVal = infinity
        for (dirt, robot) in itertools.product(state.dirt_locations, state.robots):
            tmpVal = self.dist(dirt, robot)
            if (tmpVal < firstMinVal):
                firstMinVal = tmpVal
                minDirt = dirt
                minRobot = robot
        minVal = state.width * state.height                
        if firstMinVal < infinity: 
            minVal = len(self.find_solution(state, minDirt, minRobot))
            minVal += IgnoreObstaclesHeuristic().evaluate(state)
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
    
class OneDirtPerRobotHeuristic(Heuristic):
    def dist(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def evaluate(self, state):
        totalMinVal = state.width * state.height * len(state.dirt_locations) * len(state.robots)
        robots = list(deepcopy(state.robots))
        dirts = list(deepcopy(state.dirt_locations))
        while len(dirts) and len(robots):
            firstMinVal = infinity
            for (dirt, robot) in itertools.product(dirts, robots):
                tmpVal = self.dist(dirt, robot)
                if (tmpVal < firstMinVal):
                    firstMinVal = tmpVal
                    minDirt = dirt
                    minRobot = robot
            robots.remove(minRobot)
            dirts.remove(minDirt)
            totalMinVal += self.dist(minDirt, minRobot)
        return totalMinVal
    
class OneDirtPerRobotShortestHeuristic(Heuristic):
    def dist(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def find_solution(self, state, dirt, robot):
        realDirts = deepcopy(state.dirt_locations)
        realRobots = deepcopy(state.robots)
        state.dirt_locations = frozenset([dirt])
        state.robots = tuple([robot])
        #solution = BreadthFirstGraphSearch().find(state, 5)
        solution = BeamSearch().find(state, IgnoreObstaclesHeuristic())
        state.dirt_locations = realDirts
        state.robots = realRobots
        if not solution:
            # fix it !!!!
            die("BreadthFirstGraphSearch didn't found solution")
        return solution
    
    def evaluate(self, state):
        totalMinVal = state.width * state.height * len(state.dirt_locations) * len(state.robots)
        robots = list(deepcopy(state.robots))
        dirts = list(deepcopy(state.dirt_locations))
        while len(dirts) and len(robots):
            firstMinVal = infinity
            for (dirt, robot) in itertools.product(dirts, robots):
                tmpVal = self.dist(dirt, robot)
                if (tmpVal < firstMinVal):
                    firstMinVal = tmpVal
                    minDirt = dirt
                    minRobot = robot
            robots.remove(minRobot)
            dirts.remove(minDirt)
            totalMinVal += len(self.find_solution(state, minDirt, minRobot))
        return totalMinVal