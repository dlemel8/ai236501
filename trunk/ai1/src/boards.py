'''
Created on Apr 10, 2011

@author: dlemel
'''

import multi_robot_problem
import random
import math

def generate_elms(width, height, prevent_list, num_to_create):
    res = []
    i = 0
    while num_to_create > 0:
        n = random.randint(0, width - 1)
        while (n,i) in prevent_list:
            n = random.randint(0, width - 1)
        res.append((n,i))
        num_to_create -= 1
        i = (i + 1) % height   
                
    return res

def generate_easy_board(width, height, robots_num):
    dirts = frozenset(generate_elms(width, height, [], height))
    robots = tuple(generate_elms(width, height, dirts, robots_num))
    mrs = multi_robot_problem.MultiRobotState(width, height, robots, dirts, frozenset([]))
    return mrs

def generate_medium_board(width, height, robots_num):
    obstacles = frozenset(generate_elms(width, height, [], height))
    dirts = frozenset(generate_elms(width, height, obstacles, height))
    robots = tuple(generate_elms(width, height, dirts | obstacles, robots_num))
    mrs = multi_robot_problem.MultiRobotState(width, height, robots, dirts, obstacles)
    return mrs

def generate_hard_board(width, height, robots_num):
    obstacles = frozenset(generate_elms(width, height, [], height * math.floor(math.sqrt(width))))
    dirts = frozenset(generate_elms(width, height, obstacles, height))
    robots = tuple(generate_elms(width, height, dirts | obstacles, robots_num))
    mrs = multi_robot_problem.MultiRobotState(width, height, robots, dirts, obstacles)
    return mrs

def generate_debug_board():
    dirts = frozenset([(4,2)])
    obstacles = frozenset([(1,3),(2,3),(3,3),(4,3)])
    robots = tuple([(3,4)])
    mrs = multi_robot_problem.MultiRobotState(5, 5, robots, dirts, obstacles)
    return mrs