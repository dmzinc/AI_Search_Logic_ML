from search_algorithms.route_finding.search import SearchAlgorithm
import heapq
import networkx as nx
import matplotlib.pyplot as plt


class AStar(SearchAlgorithm):
    def __init__(self, start, goal, flights, heuristic):
        super().__init__(start, goal, flights)
        self.heuristic = heuristic

    def run_algorithm(self):
        open_list = []
        heapq.heappush(open_list, (0 + self.heuristic(self.start), 0, self.start, []))
        g_costs = {self.start: 0}
        self.visited.add(self.start)

        while open_list:
            _, cost, node, path = heapq.heappop(open_list)
            path = path + [node]
            if node == self.goal:
                self.path = path
                break

            for neighbor, weight in self.flights.get(node, {}).items():
                new_cost = cost + weight
                if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_cost
                    total_cost = new_cost + self.heuristic(neighbor)
                    heapq.heappush(open_list, (total_cost, new_cost, neighbor, path))
            self.nodes_explored += 1

    def visualize_path(self):
        G = nx.Graph()
        for city, neighbors in self.flights.items():
            for neighbor, time in neighbors.items():
                G.add_edge(city, neighbor, weight=time)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
        path_edges = [(self.path[i], self.path[i + 1]) for i in range(len(self.path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=self.path, node_color="yellow", node_size=2000)
        nx.draw_networkx_nodes(G, pos, nodelist=[self.goal], node_color="green", node_size=2000)
        plt.title("A* Path")
        plt.show()
