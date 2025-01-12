import time
from pyDatalog import pyDatalog

# Initialize PyDatalog
pyDatalog.clear()

# Declare terms
pyDatalog.create_terms('X, Y, A, B, AX, AY, cell, wumpus, gold, pit, agent, stench, breeze, glitter, safe, move, adjacent, retrieve_gold, known_safe, visited')

# Define grid
cell(X, Y) <= (X.in_([1, 2, 3, 4]) & Y.in_([1, 2, 3, 4]))

# Define Wumpus, Gold, and Pit locations
+ wumpus(2, 3)
+ gold(4, 4)
+ pit(1, 3)
+ pit(2, 2)

# Agent starting position
+ agent(1, 1)

# Define adjacency rules (handling boundaries correctly)
adjacent(X, Y, A, B) <= (A == X + 1) & (B == Y) & cell(A, B)
adjacent(X, Y, A, B) <= (A == X - 1) & (B == Y) & cell(A, B)
adjacent(X, Y, A, B) <= (A == X) & (B == Y + 1) & cell(A, B)
adjacent(X, Y, A, B) <= (A == X) & (B == Y - 1) & cell(A, B)

# Define percepts
stench(X, Y) <= wumpus(A, B) & adjacent(X, Y, A, B)
breeze(X, Y) <= pit(A, B) & adjacent(X, Y, A, B)
glitter(X, Y) <= gold(X, Y)

# Define known safe cells
known_safe(X, Y) <= cell(X, Y) & ~(wumpus(X, Y)) & ~(pit(X, Y))

# Mark initial safe cells
+ known_safe(1, 2)
+ known_safe(1, 3)
+ known_safe(1, 4)
+ known_safe(4, 1)
+ known_safe(4, 2)
+ known_safe(4, 3)

# Safe cells are dynamically updated
safe(X, Y) <= known_safe(X, Y) & ~visited(X, Y)

# Visited cells
visited(X, Y) <= agent(X, Y)

# Gold retrieval
retrieve_gold(X, Y) <= agent(X, Y) & gold(X, Y)

# Define movement rules
move(X, Y) <= safe(X, Y) & adjacent(AX, AY, X, Y) & agent(AX, AY)

# Display the grid
def display_grid():
    grid = [['.' for _ in range(4)] for _ in range(4)]
    for X in range(1, 5):
        for Y in range(1, 5):
            if wumpus(X, Y):
                grid[Y - 1][X - 1] = 'W'
            elif gold(X, Y):
                grid[Y - 1][X - 1] = 'G'
            elif pit(X, Y):
                grid[Y - 1][X - 1] = 'P'
            elif stench(X, Y):
                grid[Y - 1][X - 1] = 'S'
            elif breeze(X, Y):
                grid[Y - 1][X - 1] = 'B'
    for X, Y in [(X, Y) for X in range(1, 5) for Y in range(1, 5)]:
        if agent(X, Y):
            grid[Y - 1][X - 1] = 'A'
    print("Wumpus World Grid:")
    for row in reversed(grid):  # Reverse rows for a better visual representation
        print(' '.join(row))
    print()

# Update safe cells dynamically based on percepts
def update_safe_cells(X, Y):
    for A, B in [(X + 1, Y), (X - 1, Y), (X, Y + 1), (X, Y - 1)]:
        if 1 <= A <= 4 and 1 <= B <= 4:
            if not stench(A, B) and not breeze(A, B):
                pyDatalog.assert_fact('known_safe', A, B)
                print(f"Marked ({A}, {B}) as safe.")

# Simulate agent movement
def simulate_agent_movement():
    print("Simulating agent movement...")
    current_position = (1, 1)
    visited_cells = set()

    start_time = time.time()  # Start timing the simulation

    while True:
        X, Y = current_position
        visited_cells.add((X, Y))

        display_grid()

        # Check if gold is found
        if retrieve_gold(X, Y):
            print(f"Gold found at ({X}, {Y})!")
            break

        # Update safe cells
        update_safe_cells(X, Y)

        # Find safe moves
        safe_moves = []
        for A, B in [(X + 1, Y), (X - 1, Y), (X, Y + 1), (X, Y - 1)]:
            if 1 <= A <= 4 and 1 <= B <= 4:
                if safe(A, B) and (A, B) not in visited_cells:
                    safe_moves.append((A, B))

        print(f"Safe moves: {safe_moves}")

        if safe_moves:
            # Choose the next position (arbitrarily take the first safe move)
            next_position = safe_moves[0]
            pyDatalog.retract_fact('agent', X, Y)
            pyDatalog.assert_fact('agent', next_position[0], next_position[1])
            current_position = next_position
            print(f"Agent moved to {current_position}")
        else:
            print("No safe moves available. Agent is stuck!")
            break

    end_time = time.time()  # End timing the simulation
    print(f"Simulation completed in {end_time - start_time:.4f} seconds.")

