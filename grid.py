from processing_mock import *
from spot import Spot
from utils import WHITE, RED, GREEN, BLUE, PURPLE, width_, heuristic


class Grid:
    COLS = 50
    ROWS = 50

    def __init__(self):
        self.grid = []

        self.open_set = []
        self.closed_set = []

        self.start_spot = None
        self.end_spot = None

        self.tries = 0
        self.pause = False

    def setup_grid(self, random_end=False):
        self.grid = [[Spot(i, j) for j in range(self.ROWS)] for i in range(self.COLS)]

        self.open_set = []
        self.closed_set = []
        self.tries = 0

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
        self.open_set = [self.grid[0][0]]
        self.closed_set = []

        for col in self.grid:
            for spot in col:
                spot.f = 0
                spot.g = 0
                spot.h = 0

                spot.previous = None
        self.display_grid()

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
                    val = noise(i * 0.8, j * 0.8)
                else:
                    raise NotImplementedError('Only pure random and perlin noise are implemented for now')
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
        if mouseButton == LEFT and not self.grid[x][y].block and not self.grid[x][y] == self.end_spot:
            self.grid[x][y].block = True
        elif mouseButton == RIGHT and self.grid[x][y].block:
            self.grid[x][y].block = False
        elif mouseButton == CENTER and not self.grid[x][y].block:
            self.end_spot = self.grid[x][y]
        else:
            return
        self.restart_sim()

    def find_winner_index(self):
        winner = 0
        for i, spot in enumerate(self.open_set):
            if spot.f < self.open_set[winner].f:
                winner = i
        return winner

    def discover_neighbors(self, current):
        neighbors = current.neighbors
        for neighbor in neighbors:
            if neighbor in self.closed_set or neighbor.block:
                continue

            if neighbor in current.radial_neighbors:
                temp_g = current.g + 1
            if neighbor in current.diagonal_neighbors:
                temp_g = current.g + 1.41

            if neighbor in self.open_set and not temp_g < neighbor.g:
                continue

            neighbor.g = temp_g
            neighbor.h = heuristic(neighbor, self.end_spot)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.previous = current
            if neighbor in self.open_set:
                if temp_g < neighbor.g:
                    index = self.open_set.index(neighbor)
                    self.open_set[index] = neighbor
            else:
                self.open_set.append(neighbor)

    def display_grid(self, path=None):
        background(0)
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

    def clear_entrance(self):
        self.tries = self.tries + 1
        self.grid[self.tries][self.tries].block = False
        self.restart_sim()
