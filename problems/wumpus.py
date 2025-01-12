import random


class WumpusWorld:
    def __init__(self, size=4, pit_location=None, wumpus_location=None, gold_location=None):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]


        self.pit_locations = pit_location if pit_location else []
        self.wumpus_location = wumpus_location if wumpus_location else self.generate_random_location()
        self.gold_location = gold_location if gold_location else self.generate_random_location()

        # Place Wumpus, Gold, and Pits
        self.place_wumpus()
        self.place_gold()
        self.place_pits()
        self.add_breeze_and_stench()

    def generate_random_location(self):
        return (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

    def place_wumpus(self):
        if self.wumpus_location != self.gold_location:
            self.grid[self.wumpus_location[0]][self.wumpus_location[1]] = 'W'

    def place_gold(self):
        self.grid[self.gold_location[0]][self.gold_location[1]] = 'G'

    def place_pits(self):
        if not self.pit_locations:
            for _ in range(random.randint(1, self.size)):
                pit_pos = self.generate_random_location()
                while pit_pos == self.wumpus_location or pit_pos == self.gold_location or pit_pos in self.pit_locations:
                    pit_pos = self.generate_random_location()
                self.pit_locations.append(pit_pos)
                self.grid[pit_pos[0]][pit_pos[1]] = 'P'
        else:
            for pit_pos in self.pit_locations:
                self.grid[pit_pos[0]][pit_pos[1]] = 'P'

    def add_breeze_and_stench(self):
        # Add Breeze and Stench around the pits and Wumpus
        for x in range(self.size):
            for y in range(self.size):
                # Check for breeze near pits
                if (x, y) in self.pit_locations:
                    for nx, ny in self.get_neighbors(x, y):
                        if self.grid[nx][ny] == '':
                            self.grid[nx][ny] = 'B'  # Breeze

                # Check for stench near Wumpus
                if (x, y) == self.wumpus_location:
                    for nx, ny in self.get_neighbors(x, y):
                        if self.grid[nx][ny] == '':
                            self.grid[nx][ny] = 'S'  # Stench

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbors.append((nx, ny))
        return neighbors

    def display(self):
        for row in self.grid:
            print(" ".join([str(cell) if cell != '' else '.' for cell in row]))
