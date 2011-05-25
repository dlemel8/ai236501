'''
Created on May 25, 2011

@author: ekfir
'''

from game_runner import GameRunner
from loa_game import *
from game_agent import GameAgent
from alpha_beta import AlphaBetaSearch, AlphaBetaSearchAnyTime, INFINITY
from code import interact
import sys
import random

time_safty = 0.1  

def msg(str, file=sys.stdout):
    file.write(str + '\n')
    
def die(str):
    msg('[KOL HABASA] ' + str)
    sys.exit(0)

class AlphaBetaAgent(GameAgent):
    def move(self, game_state):
        return self.alphaBetaAnyTime.search(game_state)
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.player = player
        u = lambda state: self.utility(state)
        self.alphaBetaAnyTime = AlphaBetaSearch(self.player, 3, u)

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
        self.alphaBetaAnyTime = AlphaBetaSearchAnyTime(self.player, 3, u)
        
    def move(self, game_state):
        succ = game_state.getSuccessors()
        randIdx = random.randint(0, len(succ) - 1)
        action = succ.keys()[randIdx]
        if random.random() < 0.1:
            return action
        res = self.alphaBetaAnyTime.search(game_state, self.turn_time_limit-time_safty)
        if not res:
            return action
        return res

    def utility(self, state):
        winner = state.getWinner()
        if winner is None:
            size = state.size
            totalMy = totalOther = (0, 0)
            myLoc = otherLoc = []
            for i in range(0, size):
                for j in range(0, size):
                    if state.board[i][j] == self.player:
                        myLoc.append((i,j))
                        totalMy += (i, j)
                    elif not state.board[i][j] == EMPTY:
                        otherLoc.append((i,j))
                        totalOther += (i, j)
            myCenterMass = (totalMy[0] / len(myLoc), totalMy[1] / len(myLoc))  
            otherCenterMass = (totalOther[0] / len(otherLoc), totalOther[1] / len(otherLoc))
            val = 0
            for loc in myLoc:
                length = (loc[0] - myCenterMass[0], loc[1] - myCenterMass[1])
                val -= (length[0]*length[0] + length[1]*length[1])*2
            for loc in otherLoc:
                length = (loc[0] - otherCenterMass[0], loc[1] - otherCenterMass[1])
                val += (length[0]*length[0] + length[1]*length[1])        
            return val
        
        elif winner == self.player:
            return INFINITY
        else:
            return -INFINITY

agents = {}
agents[WHITE] = AlphaBetaAgent()
agents[BLACK] = SuperMultiFlechtziUltraDNEAgentPlusPlus()

state = LinesOfActionState(8, 100)

winner = GameRunner(state, agents, 2, 1).run()
print 'Winner:', winner
