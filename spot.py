# from processing_mock import *


class Spot:
    WIDTH = HEIGHT = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.f = 0
        self.g = 0
        self.h = 0

        self.neighbors = []
        
        self.previous = None

    def show(self, col):
        fill(col)
        noStroke()
        rect(self.x * self.WIDTH, self.y * self.HEIGHT, self.WIDTH - 1, self.HEIGHT - 1)

    def add_neighbors(self, grid):
        if self.x < len(grid) - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < len(grid[0]) - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])

    @classmethod
    def set_width_and_height(cls, w, h):
        cls.WIDTH = w
        cls.HEIGHT = h
