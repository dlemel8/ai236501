# A bloody large number.
import time
from cache import LRU
INFINITY = 1.0e400
import sys
from utils import PriorityQueue
#log = open("bla.log", "w")
log = sys.stdout

def msg(objs, file=log):
    file.write(" ".join([str(obj) for obj in objs]) + '\n')
    

class AlphaBetaSearchAnyTime:
    '''
    This search algorithm implements the limited-resource minimax tree search 
    algorithm with alpha-beta pruning for zero-sum games. This version cuts off 
    search by depth alone and uses an evaluation function (utility).
    '''
    
    def __init__(self, player, utility, turn_time):
        '''
        Constructor.
        
        @param player: Your player. This search algorithm will choose the best
                       actions for this player.
        @param max_depth: The depth of the search tree.
        @param utility: An evaluation function for states.
        '''
        self.player = player
        self.utility = utility
        self.cache = LRU(100000)
        self.turn_time = turn_time
        self.cache_time_safty = 0.1
    
    def timeOver(self):
        self.time_left = self.end_time - time.clock()
        if self.time_left <= 0:
            self.bTimeOver = True
            return True
        return False
    
    def getPrioritySucc(self, state):
        items = state.getSuccessors().items()
        t = time.clock()
        if self.end_time - t < 0.1*self.turn_time:
            return items
        pq = PriorityQueue(lambda x : -self.utility(x[1]))
        pq.extend(items)
        l = [pq.pop() for _ in items] 
        return l
    
    def search(self, current_state, end_time, max_depth):
        '''
        Search game to determine best action; use alpha-beta pruning.
        
        @param current_state: The current game state to start the search from.
        '''
        best_value = -INFINITY
        self.end_time = end_time
        self.max_depth = max_depth
        best_action = None
        self.bTimeOver = False
        self.timeOver()
        
        for action, state in self.getPrioritySucc(current_state):
            if self.timeOver():
                return (best_action, best_value)
            value = self.get_value(state, best_value, INFINITY, 1)
            #msg([action, value, "depth = ",self.max_depth])
            if value > best_value:
                best_value = value
                best_action = action
                    
        return (best_action, best_value)
    
    def _getValueFn(self, state):
        if state.getCurrentPlayer() == self.player:
            return self._maxValue
        else:
            return self._minValue
    
    def _cutoffTest(self, state, depth):
        return depth >= self.max_depth or (state.getWinner() is not None)
    
    def get_value(self, successor, alpha, beta, depth):
        value_fn = self._getValueFn(successor)
        cache_key = (successor, value_fn)
        value = None
        use_cache = (self.time_left - self.cache_time_safty > 0)
        if use_cache and cache_key in self.cache:
            cache_value, cache_depth = self.cache[cache_key]
            require_depth = self.max_depth - depth
            if require_depth <= cache_depth:
                value = cache_value
        if not value:
            value = value_fn(successor, alpha, beta, depth)
            if use_cache and not self.bTimeOver:
                self.cache[cache_key] = (value, self.max_depth - depth)
        return value
    
    def _maxValue(self, state, alpha, beta, depth):
        if self._cutoffTest(state, depth):
            # TODO - think about cache in case of depth == 0
            return self.utility(state)
        
        value = -INFINITY
        for _, successor in self.getPrioritySucc(state):
            if self.timeOver():
                return value
            value = max(value, self.get_value(successor, alpha, beta, depth + 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        
        return value
    
    def _minValue(self, state, alpha, beta, depth):
        if self._cutoffTest(state, depth):
            return self.utility(state)
        
        value = INFINITY
        for _, successor in self.getPrioritySucc(state):
            if self.timeOver():
                return value
            value = min(value, self.get_value(successor, alpha, beta, depth + 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        
        return value
