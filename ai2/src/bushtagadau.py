'''
Created on May 25, 2011

@author: ekfir
'''

from game_runner import GameRunner
from loa_game import LinesOfActionState, WHITE, BLACK, TIE
from game_agent import GameAgent
from alpha_beta import AlphaBetaSearch
from alpha_beta_any_time import AlphaBetaSearchAnyTime, INFINITY, msg
import sys
import random
import time

def die(objs):
    msg(['[KOL HABASA] '] + str)
    sys.exit(0)

class DummyAgent(GameAgent):
    def move(self, game_state):
        succ = game_state.getSuccessors()
        randIdx = random.randint(0, len(succ) - 1)
        action = succ.keys()[randIdx]
        return action
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        return
    
class AlphaBetaAgent(GameAgent):
    def move(self, game_state):
        return self.alphaBeta.search(game_state)
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.player = player
        u = lambda state: self.utility(state)
        self.alphaBeta = AlphaBetaSearch(self.player, 3, u)

    def utility(self, state):
        winner = state.getWinner()
        if winner is None:
            return 0
        elif winner == self.player:
            return 1
        else:
            return -1


class SuperMultiFlechtziUltraDNEAgentPlusPlus(GameAgent):
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.turn_time_limit = turn_time_limit
        self.player = player
        self.cache_time_safty = 0.1
        u = lambda state: self.utility(state)
        self.alphaBetaAnyTime = AlphaBetaSearchAnyTime(self.player, u, turn_time_limit)
    
    def timeOver(self):
        if self.bTimeOver:
            return True
        if time.clock() >= self.end_time:
            self.bTimeOver = True
            return True
        return False
        
    def move(self, game_state):
        self.bTimeOver = False
        succ = game_state.getSuccessors()
        randIdx = random.randint(0, len(succ) - 1)
        action = succ.keys()[randIdx]
        depth = 1
        step = 1
        self.end_time = time.clock() + self.turn_time_limit - self.cache_time_safty
        max_val = -INFINITY
        while True:
            if self.timeOver():
                break
            (res, val) = self.alphaBetaAnyTime.search(game_state, self.end_time, depth)
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
            if self.bTimeOver:
                return -INFINITY
            size = state.size
            total = (0, 0)
            locations = []
            for i in range(0, size):
                for j in range(0, size):
                    if ((i*size+j) % 25) == 0 and self.timeOver():
                        return -INFINITY
                    if state.board[i][j] == self.player:
                        locations.append((i,j))
                        total = total[0] + i, total[1] + j
            
            if self.timeOver():
                return -INFINITY
             
            centerMass = (int(round(total[0] / float(len(locations)))), 
                          int(round(total[1] / float(len(locations)))))  
            
            sum_dist = sum([-self.dist(loc, centerMass) for loc in locations])
            return sum_dist
        
        elif winner == self.player:
            return INFINITY
        else:
            return -INFINITY
        
        
agents = {}
#agents[WHITE] = DummyAgent()
#agents[WHITE] = AlphaBetaAgent()
agents[WHITE] = SuperMultiFlechtziUltraDNEAgentPlusPlus()
agents[BLACK] = SuperMultiFlechtziUltraDNEAgentPlusPlus()

state = LinesOfActionState(25, 1000)

winner = GameRunner(state, agents, 1, 1).run()
msg(['Winner: ', winner])
print 'done'
