from problem_agent import ProblemAgent
from search.beam_search_any_time import BeamSearchAnyTime
from search.astar_any_time import AStarAnyTime
from heuristics import *
from boards import *
import time

print_debug = 1

class RobotsAgent(ProblemAgent):
    def solve(self, problem_state, time_limit):
        #return BeamSearch().find(problem_state, CleanHeuristic())
        #return BeamSearchAnyTime(time_limit).find(problem_state, ShortestPathHeuristic())
        #return BeamSearchAnyTime(time_limit).find(problem_state, IgnoreObstaclesHeuristic())
        #return AStarAnyTime(time_limit).find(problem_state, IgnoreObstaclesHeuristic())
        return AStarAnyTime(time_limit).find(problem_state, ShortestPathHeuristic())

if __name__ == '__main__': 
    random.seed(time.clock())
    problem = generate_medium_board(10, 10, 2)
    #problem = generate_debug_board()
    print problem
    
    agent = RobotsAgent()
    start = time.clock()
    solution = agent.solve(problem, 4)
    run_time = time.clock() - start
    print 'Solution:', solution
    print 'Solution length:', len(solution)
    print 'Running time:', run_time
