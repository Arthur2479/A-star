from processing_mock import *


class Spot:
    WIDTH = HEIGHT = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.f = 0
        self.g = 0
        self.h = 0

        self.radial_neighbors = []
        self.diagonal_neighbors = []

        self.previous = None
        self.wall = False

        if random(1) < 0.3:
            self.wall = True

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def show(self, col):
        fill(col)
        if self.wall:
            fill(0)
        noStroke()
        rect(self.x * self.WIDTH, self.y * self.HEIGHT, self.WIDTH - 1, self.HEIGHT - 1)

    def add_neighbors(self, grid, cols, rows):
        # TODO : maybe only store indexes directing to the grid table to save space ?
        # Radial neighbors
        if self.x < cols - 1:
            self.radial_neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.radial_neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.radial_neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.radial_neighbors.append(grid[self.x][self.y - 1])

        # Diagonal neighbors
        if self.x > 0 and self.y > 0:
            self.diagonal_neighbors.append(grid[self.x - 1][self.y - 1])
        if self.x < cols - 1 and self.y > 0:
            self.diagonal_neighbors.append(grid[self.x + 1][self.y - 1])
        if self.x > 0 and self.y < rows - 1:
            self.diagonal_neighbors.append(grid[self.x - 1][self.y + 1])
        if self.x < cols - 1 and self.y < rows - 1:
            self.diagonal_neighbors.append(grid[self.x + 1][self.y + 1])

    @classmethod
    def set_width_and_height(cls, w, h):
        cls.WIDTH = w
        cls.HEIGHT = h

    @property
    def neighbors(self):
        return self.radial_neighbors + self.diagonal_neighbors
