from problem_agent import ProblemAgent
from search.beam_search_any_time import BeamSearchAnyTime
from search.astar_any_time import AStarAnyTime
from search.astar import AStar
from search.beam_search import BeamSearch
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
    print 'GOING TO TEST HEURISTICS WITH A-STAR-ALGORITHM AND ALGORITHMS WITH IGNORE-OBSTACLES-HEURISTIC'
    d = { OneDirtPerRobotHeuristic.__name__:[], DirtsDivisionHeuristic.__name__:[], 
          BeamSearch.__name__:[], AStar.__name__:[] }
    for dirt_num in range(3, 100):
        problem.dirt_locations = frozenset(generate_elms(width, height, prevent_list, dirt_num))
        for h in [OneDirtPerRobotHeuristic, DirtsDivisionHeuristic]:
            start = time.clock()
            AStar(max_depth = infinity).find(problem, h())
            runtime = time.clock() - start
            d[h.__name__].append((dirt_num, runtime / dirt_num))
            if h.__name__ == OneDirtPerRobotHeuristic.__name__:
                d[AStar.__name__].append((dirt_num, runtime / dirt_num))
        start = time.clock()
        BeamSearch(max_depth = infinity, beam_width=15).find(problem, OneDirtPerRobotHeuristic())
        runtime = time.clock() - start
        d[BeamSearch.__name__].append((dirt_num, runtime / dirt_num))
    msg('runtime_of_dirts_dict = ' + str(d), log)  
    print 'runtime_of_dirts_test done! see results in log'    

def len_of_robots_test():
    width = 20
    height = 20
    robots_num = 3
    log_name = create_new_file_name('.'.join(['len_of_robots', str(date.today()), 'data']))
    log = open(log_name, 'w')
    problem = generate_easy_board(width, height, robots_num)
    problem.robots = frozenset()
    prevent_list = list(problem.obstacle_locations) + list(problem.dirt_locations)
    msg(str(problem), log)
    print 'GOING TO TEST HEURISTICS WITH A-STAR-ALGORITHM AND ALGORITHMS WITH IGNORE-OBSTACLES-HEURISTIC'
    d = { OneDirtPerRobotHeuristic.__name__:[], DirtsDivisionHeuristic.__name__:[], 
          BeamSearchAnyTime.__name__:[], AStarAnyTime.__name__:[] }
    for robots_num in [1, 2, 3]:
        for i in range(1, 20):
            problem.robots = tuple(generate_elms(width, height, prevent_list, robots_num))
            for h in [OneDirtPerRobotHeuristic, DirtsDivisionHeuristic]:
                sol = AStarAnyTime(max_time = 60, algo_to_invoke = 1, max_depth = infinity).find(problem, h())
                sol_len = sol and len(sol) or  width*height
                d[h.__name__].append((robots_num, sol_len))
                if h.__name__ == OneDirtPerRobotHeuristic.__name__:
                    d[AStarAnyTime.__name__].append((robots_num, sol_len))
            sol = BeamSearchAnyTime(max_time = 60, algo_to_invoke = 1, max_depth = infinity).find(problem, OneDirtPerRobotHeuristic())
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
        for a, h in itertools.product([BeamSearchAnyTime, AStarAnyTime], [OneDirtPerRobotHeuristic, DirtsDivisionHeuristic]):
            time_remain = time_limit - (time.clock() - start_time)
            sol = a(time_remain, algo_to_invoke, beam_width = 15).find(problem_state, h())
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
    log_name = create_new_file_name('.'.join(['agent', str(date.today()), 'data']))
    log = open(log_name, 'w')
    print 'GOING TO TEST AGENT'
    agent = RobotsAgent(log)
    problem = generate_hard_board(20, 20, 3)
    msg(str(problem), log)
    data = []
    for time_limit in range(10, 300, 15):
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
    runtime_of_dirts_test()
    #len_of_robots_test()
    #agent_test()    
