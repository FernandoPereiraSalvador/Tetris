from constants import *


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def clear_line(self, line):
        del self.grid[line]
        self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
