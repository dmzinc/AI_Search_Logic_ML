from collections import deque
import heapq
from search_algorithms.wumpus.search import SearchAlgorithm, Node

class AStar(SearchAlgorithm):
    def __init__(self, problem, heuristic_func):
        super().__init__(problem)
        self.heuristic_func = heuristic_func

    def search(self):
        frontier = []
        start_node = Node(self.problem.start_state, heuristic=self.heuristic_func(self.problem.start_state))
        heapq.heappush(frontier, start_node)
        explored = set()

        while frontier:
            node = heapq.heappop(frontier)

            if self.problem.is_goal(node.state):
                return self.reconstruct_path(node)

            explored.add(node.state)

            for action in self.problem.get_actions(node.state):
                if action not in explored:
                    new_cost = node.cost + self.problem.get_cost(node.state, action)
                    new_heuristic = self.heuristic_func(action)
                    new_node = Node(action, parent=node, cost=new_cost, heuristic=new_heuristic)
                    heapq.heappush(frontier, new_node)

        return None

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]  # Reverse the path


#heuristic: Manhattan distance
def manhattan_heuristic(state):
    goal = (2, 2)  # The location of the gold
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])
