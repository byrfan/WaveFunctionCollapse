# Credit to Original Repo mainainer of WFC -> https://github.com/mxgmn/WaveFunctionCollapse

import random
import time
import os

class Simple_WFC:
    def __init__(self, w, h) -> None: 
        # Define ASCII tiles
        self.tiles = ['#', '.', '~']  # Wall, ground, water

        # Define adjacency rules (what tiles can go next to what)
        self.adjacency_rules = {
            '#': ['#', '.'],     # Walls next to walls or ground
            '.': ['#', '.', '~'],# Ground can go next to anything
            '~': ['.', '~']      # Water next to water or ground
        }

        # Store grid dimensions
        self.width = w
        self.height = h

        # Initialize grid: each cell starts with all tile options (superposition)
        self.grid = [[set(self.tiles) for _ in range(self.width)] for _ in range(self.height)]

    def print_grid(self):
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print each row of the grid
        for row in self.grid:
            line = ''.join(next(iter(cell)) if len(cell) == 1 else '?' for cell in row)
            print(line)
        
        # Wait briefly to simulate animation
        time.sleep(0.2)


    # Return the number of tile options remaining in a cell (used as entropy measure)
    def get_entropy(self, cell):
        return len(cell)

    # Collapse a cell to one random tile from the remaining options
    def collapse(self, cell):
        return set([random.choice(list(cell))])

    # Return valid neighboring tiles based on direction and current tile
    def valid_neighbors(self, tile, direction):
        if direction == 'up' or direction == 'down':
            return self.adjacency_rules[tile]
        elif direction == 'left' or direction == 'right':
            return self.adjacency_rules[tile]
        return self.tiles

    # Propagate constraints from collapsed cells to neighbors recursively
    def propagate(self, row, col):
        changed = True
        while changed:
            changed = False
            for r in range(self.height):
                for c in range(self.width):
                    if len(self.grid[r][c]) == 1:
                        tile = next(iter(self.grid[r][c]))  # Get the only tile
                        neighbors = {
                            'up': (r - 1, c),
                            'down': (r + 1, c),
                            'left': (r, c - 1),
                            'right': (r, c + 1)
                        }
                        # Check each direction
                        for direction, (nr, nc) in neighbors.items():
                            if 0 <= nr < self.height and 0 <= nc < self.width:
                                allowed = set(self.valid_neighbors(tile, direction))
                                new_options = self.grid[nr][nc].intersection(allowed)
                                # If new possibilities have changed, update and flag for further propagation
                                if new_options != self.grid[nr][nc]:
                                    self.grid[nr][nc] = new_options
                                    changed = True

    # Main WFC loop: collapse cells with lowest entropy and propagate constraints
    def do_WFC(self):
        while any(len(cell) > 1 for row in self.grid for cell in row):
            # Get coordinates of all undecided cells
            candidates = [(r, c) for r in range(self.height) for c in range(self.width) if len(self.grid[r][c]) > 1]
            if not candidates:
                break
            # Pick the cell with the lowest entropy
            r, c = min(candidates, key=lambda pos: self.get_entropy(self.grid[pos[0]][pos[1]]))
            self.grid[r][c] = self.collapse(self.grid[r][c])  # Collapse it
            self.propagate(r, c)  # Propagate the result to neighbors
            self.print_grid()

# Create instance and run WFC on a 10x5 grid
example = Simple_WFC(10, 5)
example.do_WFC()
