import time


class SearchAlgorithm:
    def __init__(self, start, goal, flights):
        self.start = start
        self.goal = goal
        self.flights = flights
        self.visited = set()
        self.path = []
        self.time_taken = 0
        self.nodes_explored = 0

    def measure_runtime(self):
        start_time = time.perf_counter()
        self.run_algorithm()
        self.time_taken = time.perf_counter() - start_time
        return self.path, self.time_taken

    def track_nodes(self):
        return self.nodes_explored

    def visualize_path(self):
        pass
