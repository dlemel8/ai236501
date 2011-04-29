from problem_agent import ProblemAgent
from search.beam_search_any_time import BeamSearchAnyTime
from search.astar_any_time import AStarAnyTime
from heuristics import *
from boards import *
from search.utils import time_safty
import time

print_debug = 0

class RobotsAgent(ProblemAgent):
    def solve(self, problem_state, time_limit):
        sols = []
        estimated_time = None
        for a, h in itertools.product([BeamSearchAnyTime, AStarAnyTime],[IgnoreObstaclesHeuristic, DirtsDivisionHeuristic]):
            start_time = time.clock() 
            sol = a(time_limit).find(problem_state, h())
            if sol:
                sols.append(sol)
                print a, h, 'solution len:', len(sol)
            run_time = time.clock() - start_time
            time_limit -= run_time
            estimated_time = estimated_time and (estimated_time + run_time)/2 or run_time
            if estimated_time > time_limit + time_safty:
                break
        if not sols:
            return None
        else:
            return min(sols, key = len) 

if __name__ == '__main__': 
    problem = generate_medium_board(50, 10, 2)
    #problem = generate_debug_board()
    print problem
    
    agent = RobotsAgent()
    start = time.clock()
    solution = agent.solve(problem, 4)
    run_time = time.clock() - start
    if solution:
        print 'Solution:', solution
        print 'Solution length:', len(solution)
        print 'Running time:', run_time
    else:
        print 'Could not find a solution'
    
    
