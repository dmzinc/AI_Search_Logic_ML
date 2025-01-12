from collections import deque
from search_algorithms.wumpus.search import SearchAlgorithm, Node

class DFS(SearchAlgorithm):
    def search(self):
        frontier = [Node(self.problem.start_state)]  # LIFO stack
        explored = set()

        while frontier:
            node = frontier.pop()

            if self.problem.is_goal(node.state):
                return self.reconstruct_path(node)

            explored.add(node.state)

            for action in self.problem.get_actions(node.state):
                if action not in explored:
                    new_node = Node(action, parent=node, cost=node.cost + 1)
                    frontier.append(new_node)

        return None

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]