'''
Created on May 25, 2011

@author: ekfir
'''

from game_runner import GameRunner
from loa_game import LinesOfActionState, WHITE, BLACK, TIE
from game_agent import GameAgent
from alpha_beta_any_time import AlphaBetaSearchAnyTime, INFINITY, msg, TimeManager
import sys
import random
import os
from datetime import date

def die(objs):
    msg(['[KOL HABASA] '] + str)
    sys.exit(0)

class LoaDEAgent(GameAgent):
    def pre_pre_pre_setup(self, bIgnore, cache_size):
        self.use_extentions = bIgnore
        self.cache_size = cache_size
        
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.turn_time_limit = turn_time_limit
        self.player = player
        u = lambda state: self.utility(state)
        self.time_manager = TimeManager(turn_time_limit)
        if not ("use_extentions" in self.__dict__):
            self.use_extentions = (True, True)
        if not ("cache_size" in self.__dict__):
            self.cache_size = 1000
        self.alphaBetaAnyTime = AlphaBetaSearchAnyTime(self.player, u, self.time_manager, self.use_extentions, self.cache_size)
        
    def move(self, game_state):
        self.time_manager.start()
        succ = game_state.getSuccessors()
        randIdx = random.randint(0, len(succ) - 1)
        action = succ.keys()[randIdx]
        depth = 1
        step = 1
        max_val = -INFINITY
        while True:
            if self.time_manager.timeOver():
                break
            (res, val) = self.alphaBetaAnyTime.search(game_state, depth)
            if max_val < val:
                max_val = val
                action = res
            depth += step
            step += 1
        
        return action

    def dist(self, p1, p2):
        x = abs(p1[0] - p2[0])
        y = abs(p1[1] - p2[1])
        dis = min(x, y) + abs(x - y)
        return dis * dis
    
    def utility(self, state):
        winner = state.getWinner()
        if winner is None or winner == TIE:
            if self.time_manager.bTimeOver:
                return -INFINITY
            size = state.size
            total = (0, 0)
            locations = []
            for i in range(0, size):
                for j in range(0, size):
                    if ((i*size+j) % 25) == 0 and self.time_manager.timeOver():
                        return -INFINITY
                    if state.board[i][j] == self.player:
                        locations.append((i,j))
                        total = total[0] + i, total[1] + j
            
            if self.time_manager.timeOver():
                return -INFINITY
             
            centerMass = (int(round(total[0] / float(len(locations)))), 
                          int(round(total[1] / float(len(locations)))))  
            
            sum_dist = sum([-self.dist(loc, centerMass) for loc in locations])
            return sum_dist
        
        elif winner == self.player:
            return INFINITY
        else:
            return -INFINITY


#################################################################################################

def create_new_file_name(pattern):
    num = 0
    while os.path.exists(pattern + '.' + str(num)):
        num += 1
    return pattern + '.' + str(num)

def cache_size_dict_test():
    log_name = create_new_file_name('.'.join(['cache_size_dict_test', str(date.today()), 'data']))
    log = open(log_name, 'w')
    d = {}
    agents = {}
    regular = LoaDEAgent()
    opt = LoaDEAgent()
    
    regular.pre_pre_pre_setup((False, False), 0)
    
    
    for cache_size in [10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000]:
        total = 0
        opt.pre_pre_pre_setup((False, True), cache_size)
        state = LinesOfActionState(8, 100000)
        
        agents[WHITE] = opt
        agents[BLACK] = regular
        
        winner = GameRunner(state, agents, 5, 1).run()
        if winner == WHITE:
            total += 1
        
        winner = GameRunner(state, agents, 5, 1).run()
        if winner == WHITE:
            total += 1
        
        agents[BLACK] = opt
        agents[WHITE] = regular
        
        winner = GameRunner(state, agents, 5, 1).run()
        if winner == BLACK:
            total += 1
        
        winner = GameRunner(state, agents, 5, 1).run()
        if winner == BLACK:
            total += 1
            
        d[cache_size] = total
        
        print 'total: ', total

    msg('cache_size_dict = ' + str(d), log)  
    print 'cache_size_dict_test done! see results in log'    


def cache_time_dict_test():
    log_name = create_new_file_name('.'.join(['cache_time_dict_test', str(date.today()), 'data']))
    log = open(log_name, 'w')
    d = {}
    agents = {}
    regular = LoaDEAgent()
    opt = LoaDEAgent()
    opt.pre_pre_pre_setup((False, True), 1000)
    regular.pre_pre_pre_setup((False, False), 0)
    state = LinesOfActionState(8, 100000)
    
    for cache_time in range(1,10,2):
        total = 0
        
        agents[WHITE] = opt
        agents[BLACK] = regular
        
        winner = GameRunner(state, agents, cache_time, 1).run()
        if winner == WHITE:
            total += 1
        
        winner = GameRunner(state, agents, cache_time, 1).run()
        if winner == WHITE:
            total += 1
        
        agents[BLACK] = opt
        agents[WHITE] = regular
        
        winner = GameRunner(state, agents, cache_time, 1).run()
        if winner == BLACK:
            total += 1
        
        winner = GameRunner(state, agents, cache_time, 1).run()
        if winner == BLACK:
            total += 1
            
        d[cache_time] = total
        
        print 'total: ', total

    msg('cache_time_dict = ' + str(d), log)  
    print 'cache_time_dict_test done! see results in log'    


def cache__borad_size_dict_test():
    log_name = create_new_file_name('.'.join(['cache__borad_size_dict_test', str(date.today()), 'data']))
    log = open(log_name, 'w')
    d = {}
    agents = {}
    regular = LoaDEAgent()
    opt = LoaDEAgent()
    
    regular.pre_pre_pre_setup((False, False), 0)
    opt.pre_pre_pre_setup((False, True), 1000)
    
    for board_size in range(8,12):
        total = 0
        state = LinesOfActionState(board_size, 100000)
        
        agents[WHITE] = opt
        agents[BLACK] = regular
        
        winner = GameRunner(state, agents, 3, 1).run()
        if winner == WHITE:
            total += 1
        
        winner = GameRunner(state, agents, 3, 1).run()
        if winner == WHITE:
            total += 1
        
        agents[BLACK] = opt
        agents[WHITE] = regular
        
        winner = GameRunner(state, agents, 3, 1).run()
        if winner == BLACK:
            total += 1
        
        winner = GameRunner(state, agents, 3, 1).run()
        if winner == BLACK:
            total += 1
            
        d[board_size] = total
        
        print 'total: ', total

    msg('cache__borad_size_dict = ' + str(d), log)  
    print 'cache__borad_size_dict_test done! see results in log'    


def reordering_time_dict_test():
    log_name = create_new_file_name('.'.join(['reordering_time_dict_test', str(date.today()), 'data']))
    log = open(log_name, 'w')
    d = {}
    agents = {}
    regular = LoaDEAgent()
    opt = LoaDEAgent()
    opt.pre_pre_pre_setup((True, False), 0)
    regular.pre_pre_pre_setup((False, False), 0)
    state = LinesOfActionState(8, 100000)
    
    for cache_time in range(1,10,2):
        total = 0
        
        agents[WHITE] = opt
        agents[BLACK] = regular
        
        winner = GameRunner(state, agents, cache_time, 1).run()
        if winner == WHITE:
            total += 1
        
        winner = GameRunner(state, agents, cache_time, 1).run()
        if winner == WHITE:
            total += 1
        
        agents[BLACK] = opt
        agents[WHITE] = regular
        
        winner = GameRunner(state, agents, cache_time, 1).run()
        if winner == BLACK:
            total += 1
        
        winner = GameRunner(state, agents, cache_time, 1).run()
        if winner == BLACK:
            total += 1
            
        d[cache_time] = total
        
        print 'total: ', total

    msg('reordering_time_dict = ' + str(d), log)  
    print 'reordering_time_dict_test done! see results in log'    


def reordering__borad_size_dict_test():
    log_name = create_new_file_name('.'.join(['reordering__borad_size_dict_test', str(date.today()), 'data']))
    log = open(log_name, 'w')
    d = {}
    agents = {}
    regular = LoaDEAgent()
    opt = LoaDEAgent()
    
    regular.pre_pre_pre_setup((False, False), 0)
    opt.pre_pre_pre_setup((True, False), 0)
    
    for board_size in range(8,12):
        total = 0
        state = LinesOfActionState(board_size, 100000)
        
        agents[WHITE] = opt
        agents[BLACK] = regular
        
        winner = GameRunner(state, agents, 3, 1).run()
        if winner == WHITE:
            total += 1
        
        winner = GameRunner(state, agents, 3, 1).run()
        if winner == WHITE:
            total += 1
        
        agents[BLACK] = opt
        agents[WHITE] = regular
        
        winner = GameRunner(state, agents, 3, 1).run()
        if winner == BLACK:
            total += 1
        
        winner = GameRunner(state, agents, 3, 1).run()
        if winner == BLACK:
            total += 1
            
        d[board_size] = total
        
        print 'total: ', total

    msg('reordering__borad_size_dict = ' + str(d), log)  
    print 'reordering__borad_size_dict_test done! see results in log'    
        
        
if __name__ == '__main__':
    cache_size_dict_test()
    cache_size_dict_test()
    cache_time_dict_test()
    cache_time_dict_test()
    cache__borad_size_dict_test()
    cache__borad_size_dict_test()
    cache_size_dict_test()
    cache_size_dict_test()
    cache_time_dict_test()
    cache_time_dict_test()
    cache__borad_size_dict_test()
    cache__borad_size_dict_test()
    print 'done'
