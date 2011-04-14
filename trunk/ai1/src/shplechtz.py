from problem_agent import ProblemAgent
from search.beam_search import BeamSearch
from heuristics import *
from boards import *
import time
from search.beam_search import BeamSearch

print_debug = 1

class RobotsAgent(ProblemAgent):
    def solve(self, problem_state, time_limit):
        #return BeamSearch().find(problem_state, CleanHeuristic())
        return BeamSearch().find(problem_state, ShortestPathHeuristic())
        #return BeamSearch().find(problem_state, IgnoreObstaclesHeuristic())

if __name__ == '__main__': 
    random.seed(time.clock())
    problem = generate_medium_board(10, 10, 1)
    #problem = generate_debug_board()
    print problem
    
    agent = RobotsAgent()
    start = time.clock()
    solution = agent.solve(problem, 17)
    run_time = time.clock() - start
    print 'Solution:', solution
    print 'Solution length:', len(solution)
    print 'Running time:', run_time
