from problem_agent import ProblemAgent
from search.algorithm import Heuristic
from search.best_first import BestFirstGraphSearch
import boards
import time


class TestAgent(ProblemAgent):
    def solve(self, problem_state, time_limit):
        return BestFirstGraphSearch().find(problem_state, CleanHeuristic())


class CleanHeuristic(Heuristic):
    def evaluate(self, state):
        return len(state.dirt_locations)

if __name__ == '__main__': 
    problem = boards.generate_eazy_board(10, 10, 2)
    print problem
    
    agent = TestAgent()
    start = time.clock()
    solution = agent.solve(problem, 17)
    run_time = time.clock() - start
    print 'Solution:', solution
    print 'Solution length:', len(solution)
    print 'Running time:', run_time
