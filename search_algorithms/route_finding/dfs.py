from search_algorithms.route_finding.search import SearchAlgorithm
import networkx as nx
import matplotlib.pyplot as plt


class DFS(SearchAlgorithm):
    def run_algorithm(self):
        stack = [(self.start, [])]
        self.visited.add(self.start)
        while stack:
            node, path = stack.pop()
            path = path + [node]
            if node == self.goal:
                self.path = path
                break
            for neighbor, weight in self.flights.get(node, {}).items():
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    stack.append((neighbor, path))
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
        plt.title("DFS Path")
        plt.show()
