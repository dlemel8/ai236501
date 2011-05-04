from problem_agent import ProblemAgent
from search.beam_search_any_time import BeamSearchAnyTime
from search.astar_any_time import AStarAnyTime
from heuristics import *
from boards import *
from search.utils import time_safty, infinity
import os
import math
import matplotlib.pyplot as plt
from datetime import date
from numpy.numarray.functions import average
from scipy.stats import wilcoxon
import numpy as np

print_debug = 0
log = open('robots.log', 'w')

def create_new_file_name(pattern):
    num = 0
    while os.path.exists(pattern + '.' + str(num)):
        num += 1
    return pattern + '.' + str(num)

def runtime_of_dirts_test():
    width = 20
    height = 20
    robots_num = 3
    log_name = create_new_file_name('.'.join(['runtime_of_dirts', str(date.today()), 'data']))
    log = open(log_name, 'w')
    problem = generate_hard_board(width, height, robots_num)
    problem.dirt_locations = frozenset()
    prevent_list = list(problem.obstacle_locations) + list(problem.robots)
    msg(str(problem), log)
    msg('GOING TO TEST HEURISTICS WITH A-STAR-ALGORITHM AND ALGORITHMS WITH IGNORE-OBSTACLES-HEURISTIC', log)
    d = { OneDirtPerRobotHeuristic.__name__:[], DirtsDivisionHeuristic.__name__:[], 
          BeamSearchAnyTime.__name__:[], AStarAnyTime.__name__:[] }
    for dirt_num in range(3, 100):
        problem.dirt_locations = frozenset(generate_elms(width, height, prevent_list, dirt_num))
        for h in [OneDirtPerRobotHeuristic, DirtsDivisionHeuristic]:
            start = time.clock()
            AStarAnyTime(max_time = 90, max_depth = infinity).find(problem, h())
            runtime = time.clock() - start
            d[h.__name__].append((dirt_num, runtime / dirt_num))
            if h.__name__ == OneDirtPerRobotHeuristic.__name__:
                d[AStarAnyTime.__name__].append((dirt_num, runtime / dirt_num))
        start = time.clock()
        BeamSearchAnyTime(max_time = 90, max_depth = infinity).find(problem, OneDirtPerRobotHeuristic())
        runtime = time.clock() - start
        d[BeamSearchAnyTime.__name__].append((dirt_num, runtime / dirt_num))
    msg('runtime_of_dirts_dict = ' + str(d), log)  
    print 'runtime_of_dirts_test done! see results in log'    

def len_of_robots_test():
    width = 20
    height = 20
    robots_num = 3
    log_name = create_new_file_name('.'.join(['runtime_of_dirts', str(date.today()), 'data']))
    log = open(log_name, 'w')
    problem = generate_easy_board(width, height, robots_num)
    problem.robots = frozenset()
    prevent_list = list(problem.obstacle_locations) + list(problem.dirt_locations)
    msg(str(problem), log)
    msg('GOING TO TEST HEURISTICS WITH A-STAR-ALGORITHM AND ALGORITHMS WITH IGNORE-OBSTACLES-HEURISTIC', log)
    d = { OneDirtPerRobotHeuristic.__name__:[], DirtsDivisionHeuristic.__name__:[], 
          BeamSearchAnyTime.__name__:[], AStarAnyTime.__name__:[] }
    for robots_num in [1, 2, 3]:
        for i in range(1, 30):
            problem.robots = tuple(generate_elms(width, height, prevent_list, robots_num))
            for h in [OneDirtPerRobotHeuristic, DirtsDivisionHeuristic]:
                start = time.clock()
                sol = AStarAnyTime(max_time = 90, max_depth = infinity).find(problem, h())
                runtime = time.clock() - start
                sol_len = sol and len(sol) or  width*height
                d[h.__name__].append((robots_num, sol_len))
                if h.__name__ == OneDirtPerRobotHeuristic.__name__:
                    d[AStarAnyTime.__name__].append((robots_num, sol_len))
            start = time.clock()
            sol = BeamSearchAnyTime(max_time = 90, max_depth = infinity).find(problem, OneDirtPerRobotHeuristic())
            runtime = time.clock() - start
            sol_len = sol and len(sol) or  width*height
            d[BeamSearchAnyTime.__name__].append((robots_num, sol_len))
    msg('len_of_robots_test = ' + str(d), log)  
    print 'len_of_robots_test done! see results in log'    

class RobotsAgent(ProblemAgent):
    def __init__(self, log):
        self.log = log
    
    def solve(self, problem_state, time_limit):
        start_time = time.clock() 
        sols = []
        algo_to_invoke = 4.0
        world = problem_state.height * problem_state.width
        for a, h in itertools.product([BeamSearchAnyTime, AStarAnyTime], [OneDirtPerRobotHeuristic, DirtsDivisionHeuristic]):
            time_remain = time_limit - (time.clock() - start_time)
            sol = a(time_remain, algo_to_invoke).find(problem_state, h())
            if sol:
                sols.append(sol)
            if time_remain < time_safty:
                break
            algo_to_invoke -= 1.0
        if not sols:
            return 0, None
        else:
            return len(sols), min(sols, key = len) 

def agent_test():
    start = time.clock()
    log_name = '.'.join(['agent', str(date.today()), 'data'])
    #log_name = create_new_file_name('.'.join(['agent', str(date.today()), 'data']))
    log = open(log_name, 'w')
    agent = RobotsAgent(log)
    problem = generate_hard_board(20, 20, 3)
    msg(str(problem), log)
    data = []
    for time_limit in range(10, 51, 15):
        sols = []
        for run in range(1):
            start_solve = time.clock()
            num, solution = agent.solve(problem, time_limit)
            runtime_solve = time.clock() - start_solve
            if solution:
                sols.append(len(solution))
                msg(str(time_limit) + ' ' + str(run) + ' ' + str(num), log)
        if len(sols) > 0:
            data.append((time_limit, average(sols)))
    msg('agent_test = ' + str(data), log)
    print 'agent_test done! see results in log. runtime', time.clock() - start
            

if __name__ == '__main__':
    #print wilcoxon(np.random.randn(100), 0.12 + np.random.randn(100))
    #runtime_of_dirts_test()
    #len_of_robots_test()
    agent_test()
    sys.exit(0)
    
    
    problem = generate_medium_board(10, 10, 2)
    #problem = generate_debug_board()
    msg(str(problem))
    
    agent = RobotsAgent()
    start = time.clock()
    solution = agent.solve(problem, 0.1)
    run_time = time.clock() - start
    if solution:
        msg('Solution: ' + str(solution))
        msg('Solution length: ' + str(len(solution)))
        msg('Running time: ' + str(run_time))
    else:
        msg('Could not find a solution')
    print 'done! see results in log'
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.hist()
    #plt.show()
    import matplotlib.mlab as mlab
    
    mu, sigma = 5, 1.5
    x = mu + sigma*np.random.randn(100)
    
    # the histogram of the data
    n, bins, patches = plt.hist(x, 20, normed=1, facecolor='green', alpha=0.75)
    
    # add a 'best fit' line
    y = mlab.normpdf( bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth=1)
    
    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    plt.axis([0, 10, 0, 1])
    plt.grid(True)
    
    plt.show()

    
