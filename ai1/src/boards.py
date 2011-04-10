'''
Created on Apr 10, 2011

@author: dlemel
'''

import multi_robot_problem
import random
import time
import math

random.seed(time.clock())
def generate_elms(width, height, prevent_list, num_to_create):
    res = []
    i = random.randint(0, height - 1)
    while num_to_create > 0:
        n = random.randint(0, width - 1)
        while (n,i) in (prevent_list + res):
            n = random.randint(0, width - 1)
        res.append((n,i))
        num_to_create -= 1
        i = (i + random.randint(1, height - 1)) % height                   
    return res

def generate_eazy_board(width, height, robots_num):
    dirts = generate_elms(width, height, [], height)
    robots = generate_elms(width, height, dirts, robots_num)
    mrs = multi_robot_problem.MultiRobotState(width, height, robots, dirts, [])
    return mrs

def generate_medium_board(width, height, robots_num):
    obstacles = generate_elms(width, height, [], height)
    dirts = generate_elms(width, height, obstacles, height)
    robots = generate_elms(width, height, dirts + obstacles, robots_num)
    mrs = multi_robot_problem.MultiRobotState(width, height, robots, dirts, obstacles)
    return mrs

def generate_hard_board(width, height, robots_num):
    obstacles = generate_elms(width, height, [], height * math.floor(math.sqrt(width)))
    dirts = generate_elms(width, height, obstacles, height)
    robots = generate_elms(width, height, dirts + obstacles, robots_num)
    mrs = multi_robot_problem.MultiRobotState(width, height, robots, dirts, obstacles)
    return mrs


print generate_eazy_board(20, 10, 2)
print generate_medium_board(20, 10, 2)
print generate_hard_board(20, 10, 2)