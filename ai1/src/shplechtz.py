from problem_agent import ProblemAgent
from search.best_first import BestFirstGraphSearch
from heuristics import *
from boards import *
import time

class RobotsAgent(ProblemAgent):
    def solve(self, problem_state, time_limit):
        return BestFirstGraphSearch().find(problem_state, CleanHeuristic())

if __name__ == '__main__': 
    problem = generate_medium_board(10, 10, 2)
    print problem
    
    agent = RobotsAgent()
    start = time.clock()
    solution = agent.solve(problem, 17)
    run_time = time.clock() - start
    print 'Solution:', solution
    print 'Solution length:', len(solution)
    print 'Running time:', run_time
