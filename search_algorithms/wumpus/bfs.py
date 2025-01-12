from collections import deque
from search_algorithms.wumpus.search import SearchAlgorithm, Node

class BFS(SearchAlgorithm):
    def search(self):
        frontier = deque([Node(self.problem.start_state)])  # FIFO queue
        explored = set()

        while frontier:
            node = frontier.popleft()

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
