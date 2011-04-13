from search.algorithm import Heuristic

class CleanHeuristic(Heuristic):
    def evaluate(self, state):
        return len(state.dirt_locations)
