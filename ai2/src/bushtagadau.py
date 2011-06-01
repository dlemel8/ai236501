'''
Created on May 25, 2011

@author: ekfir
'''

from game_runner import GameRunner
from loa_game import *
from game_agent import GameAgent
from alpha_beta import AlphaBetaSearch
from alpha_beta_any_time import AlphaBetaSearchAnyTime, INFINITY, msg
import sys
import random
import time

time_safty = 0.2

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
        u = lambda state: self.utility(state)
        self.alphaBetaAnyTime = AlphaBetaSearchAnyTime(self.player, u)
        
    def move(self, game_state):
        succ = game_state.getSuccessors()
        randIdx = random.randint(0, len(succ) - 1)
        action = succ.keys()[randIdx]
        #if random.random() < 0.1:
        #    return action
        i = 1
        step = 1
        end_time = time.clock() + self.turn_time_limit - time_safty
        max_val = -INFINITY
        while True:
            if time.clock() >= end_time:
                break
            (res, val) = self.alphaBetaAnyTime.search(game_state, end_time, i)
            if max_val < val:
                max_val = val
                action = res
            i += step
            step += 1
        
        return action

    def dist(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def utility(self, state):
        winner = state.getWinner()
        if winner is None or winner == TIE:
            size = state.size
            totalMy = max_box = (0, 0)
            min_box = (INFINITY, INFINITY)
            myLoc = []
            for i in range(0, size):
                for j in range(0, size):
                    if state.board[i][j] == self.player:
                        min_box = min(min_box[0], i), min(min_box[1], j)
                        max_box = max(max_box[0], i), max(max_box[1], j)
                        myLoc.append((i,j))
                        totalMy = totalMy[0] + i, totalMy[1] + j
            centerMass = (round(totalMy[0] / float(len(myLoc))), round(totalMy[1] / float(len(myLoc))))  
            val = 0
            for loc in myLoc:
                length = (loc[0] - centerMass[0], loc[1] - centerMass[1])
                #val -= self.dist(loc, centerMass)# - math.sqrt(length[0]*length[0] + length[1]*length[1])
                val -= (length[0]*length[0] + length[1]*length[1])
            #lx,ly = max_box[0] - min_box[0], max_box[1] - min_box[1] 
            #val -= (lx*ly)        
            return val
        
        elif winner == self.player:
            return INFINITY
        else:
            return -INFINITY
        
        
agents = {}
agents[WHITE] = DummyAgent()
#agents[WHITE] = AlphaBetaAgent()
#agents[WHITE] = SuperMultiFlechtziUltraDNEAgentPlusPlus()
agents[BLACK] = SuperMultiFlechtziUltraDNEAgentPlusPlus()

state = LinesOfActionState(8, 100)

winner = GameRunner(state, agents, 5, 1).run()
msg(['Winner: ', winner])
print 'done'
