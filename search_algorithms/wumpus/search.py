from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic
        self.total_cost = cost + heuristic

    def __lt__(self, other):
        return self.total_cost < other.total_cost


class SearchProblem:
    def __init__(self, wumpus_world):
        self.wumpus_world = wumpus_world
        self.start_state = (0, 0)
        self.goal_state = wumpus_world.gold_location

    def get_actions(self, state):
        x, y = state
        actions = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.wumpus_world.size and 0 <= ny < self.wumpus_world.size:
                actions.append((nx, ny))
        return actions

    def get_cost(self, current_state, next_state):
        x1, y1 = current_state
        x2, y2 = next_state
        if next_state == self.wumpus_world.wumpus_location:
            return float('inf')
        elif next_state in self.wumpus_world.pit_locations:
            return float('inf')
        else:
            return 1

    def is_goal(self, state):
        return state == self.goal_state


class SearchAlgorithm:
    def __init__(self, problem):
        self.problem = problem

    def search(self):
        raise NotImplementedError("Search method must be implemented in subclass")
