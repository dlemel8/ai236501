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
    
class TimeManager:
    def __init__(self, turn_time):
        self.turn_time = turn_time
        self.time_safty = 0.1
        
    def start(self):
        self.bTimeOver = False
        self.time_left = self.turn_time
        self.end_time = time.clock() + self.turn_time - self.time_safty
        
    def timeOver(self, safty = 0.0):
        if self.bTimeOver:
            return True
        self.time_left = self.end_time - time.clock()
        if self.time_left - safty <= 0:
            self.bTimeOver = True
            return True
        return False
    

class AlphaBetaSearchAnyTime:
    '''
    This search algorithm implements the limited-resource minimax tree search 
    algorithm with alpha-beta pruning for zero-sum games. This version cuts off 
    search by depth alone and uses an evaluation function (utility).
    '''
    
    def __init__(self, player, utility, time_manager, use_extentions, cache_size):
        '''
        Constructor.
        
        @param player: Your player. This search algorithm will choose the best
                       actions for this player.
        @param max_depth: The depth of the search tree.
        @param utility: An evaluation function for states.
        '''
        self.player = player
        self.utility = utility
        self.cache = LRU(cache_size)
        self.time_manager = time_manager
        self.cache_time_safty = 0.1
        self.use_extentions = use_extentions
        self.cache_hit = 0
        self.cache_miss = 0
    
    def getPrioritySucc(self, state):
        items = state.getSuccessors().items()
        if not self.use_extentions[0] or self.time_manager.time_left < 0.3:
            return items
        factor = state.getCurrentPlayer() == self.player and -1 or 1
        pq = PriorityQueue(lambda x : factor * self.utility(x[1]))
        for item in items:
            pq.append(item)
            if self.time_manager.bTimeOver:
                return items
        return pq
    
    def search(self, current_state, max_depth):
        '''
        Search game to determine best action; use alpha-beta pruning.
        
        @param current_state: The current game state to start the search from.
        '''
        best_value = -INFINITY
        self.max_depth = max_depth
        best_action = None
        if self.time_manager.timeOver():
            return (best_action, best_value)
        
        values = self.getPrioritySucc(current_state)
        while values:
            action, state = values.pop()
            value = self.get_value(state, best_value, INFINITY, 1)
            #msg([action, value, "depth = ",self.max_depth])
            if value > best_value:
                best_value = value
                best_action = action
            if self.time_manager.timeOver():
                return (best_action, best_value)
                    
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
        use_cache = self.use_extentions[1] and not self.time_manager.timeOver(self.cache_time_safty)
        if use_cache and cache_key in self.cache:
            cache_value, cache_depth = self.cache[cache_key]
            require_depth = self.max_depth - depth
            if require_depth <= cache_depth:
                self.cache_hit += 1
                value = cache_value
        if not value:
            value = value_fn(successor, alpha, beta, depth)
            self.cache_miss += 1
            if use_cache and not self.time_manager.bTimeOver:
                self.cache[cache_key] = (value, self.max_depth - depth)
        return value
    
    def _maxValue(self, state, alpha, beta, depth):
        value = -INFINITY
        if self.time_manager.timeOver():
            return value
        if self._cutoffTest(state, depth):
            # TODO - think about cache in case of depth == 0
            return self.utility(state)
        
        values = self.getPrioritySucc(state)
        while values:
            _, successor = values.pop()
            if self.time_manager.timeOver():
                return value
            value = max(value, self.get_value(successor, alpha, beta, depth + 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        
        return value
    
    def _minValue(self, state, alpha, beta, depth):
        value = INFINITY
        if self.time_manager.timeOver():
            return value
        if self._cutoffTest(state, depth):
            return self.utility(state)
        values = self.getPrioritySucc(state)
        while values:
            _, successor = values.pop()
            if self.time_manager.timeOver():
                return value
            value = min(value, self.get_value(successor, alpha, beta, depth + 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        
        return value
