from processing_mock import *
from spot import Spot
from utils import WHITE, RED, GREEN, BLUE, PURPLE, width_


class Grid:
    COLS = 50
    ROWS = 50

    def __init__(self):
        self.grid = []

        self.open_set = []
        self.closed_set = []

        self.start_spot = None
        self.end_spot = None

    def setup_grid(self, random_end=False):
        self.grid = [[Spot(i, j) for j in range(self.ROWS)] for i in range(self.COLS)]
        self.open_set = []
        self.closed_set = []

        self.start_spot = self.grid[0][0]
        if random_end:
            end_col = int(random(self.COLS))
            end_row = int(random(self.ROWS))
        else:
            end_col = self.COLS - 1
            end_row = self.ROWS - 1
        self.end_spot = self.grid[end_col][end_row]

        if random(1) < 0.5:
            self.add_blocks('perlin', 0.45)
        else:
            self.add_blocks('random')
        self.add_neighbors()

        self.grid[0][0].block = False
        self.grid[end_col][end_row].block = False

        self.open_set.append(self.start_spot)

    def restart_sim(self):
        # TODO : clean this
        self.open_set = [self.grid[0][0]]
        self.closed_set = []

        for col in self.grid:
            for spot in col:
                spot.f = 0
                spot.g = 0
                spot.h = 0

                spot.previous = None

    def add_neighbors(self):
        for row in self.grid:
            for spot in row:
                spot.add_neighbors(self.grid, self.COLS, self.ROWS)

    def add_blocks(self, distribution, threshold=0.3):
        noiseSeed(int(random(1000)))
        for i, row in enumerate(self.grid):
            for j, spot in enumerate(row):
                if distribution == 'random':
                    val = random(1)
                elif distribution == 'perlin':
                    val = noise(i * 0.9, j * 0.8)
                if val < threshold:
                    spot.block = True

    def _locate_point(self, x, y):
        i = floor(self.COLS * x / width)
        j = floor(self.ROWS * y / height)
        return i, j

    def place_or_remove_wall(self):
        x, y = self._locate_point(mouseX, mouseY)
        if min(x, y) < 0 or max(x, y) > width_:  # Outside of screen
            return
        if mouseButton == LEFT and not self.grid[x][y].block:
            self.grid[x][y].block = True
        elif mouseButton == RIGHT and self.grid[x][y].block:
            self.grid[x][y].block = False
        elif mouseButton == CENTER and not self.grid[x][y].block:
            self.end_spot = self.grid[x][y]
        else:
            return
        self.restart_sim()

    def display_grid(self, path=None):
        if path is None:
            path = []

        for row in self.grid:
            for spot in row:
                spot.show(WHITE)

        for spot in self.open_set:
            spot.show(GREEN)

        for spot in self.closed_set:
            spot.show(RED)

        for spot in path:
            spot.show(BLUE)

        self.end_spot.show(PURPLE)

    def find_path(self, spot):
        path = [spot]
        while spot.previous:
            path.append(spot.previous)
            spot = spot.previous
        return path
