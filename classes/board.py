from constants import *


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def clear_line(self, line):
        del self.grid[line]
        self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

    def check_and_clear_lines(self):
        complete_rows = []
        for y, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                complete_rows.append(y)

        for row in complete_rows:
            self.clear_line(row)

        return len(complete_rows)
