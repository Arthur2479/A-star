from processing_mock import *
from spot import Spot


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

        for row in self.grid:
            for spot in row:
                spot.add_neighbors(self.grid)

        self.grid[0][0].wall = False
        self.grid[end_col][end_row].wall = False

        self.open_set.append(self.start_spot)


WHITE = color(255)
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
PURPLE = color(128, 0, 128)

grid = Grid()


def setup():
    size(800, 800)
    frameRate(24)
    background(0)
    strokeWeight(1)
    print('A*')

    spot_w = int(width / Grid.COLS)
    spot_h = int(height / Grid.COLS)

    Spot.set_width_and_height(spot_w, spot_h)

    grid.setup_grid(random_end=True)


def draw():
    if len(grid.open_set) == 0:
        print('Empty open set')
        delay(1000)
        grid.setup_grid(random_end=True)
        return  # Failed

    winner = 0
    for i, spot in enumerate(grid.open_set):
        if spot.f < grid.open_set[winner].f:
            winner = i

    current = grid.open_set[winner]
    if current == grid.end_spot:
        delay(1000)
        grid.setup_grid(random_end=True)
        return

    grid.open_set.remove(current)
    grid.closed_set.append(current)

    neighbors = current.neighbors
    for neighbor in neighbors:
        if neighbor in grid.closed_set or neighbor.wall:
            continue

        temp_g = current.g + 1  # no need to caclulate distance because orthogonal grid
        # TODO : add a supplement if diagonal

        if neighbor in grid.open_set and not temp_g < neighbor.g:
            continue

        neighbor.g = temp_g
        neighbor.h = heuristic(neighbor, grid.end_spot)
        neighbor.f = neighbor.g + neighbor.h
        neighbor.previous = current
        if neighbor in grid.open_set:
            if temp_g < neighbor.g:
                index = grid.open_set.index(neighbor)
                grid.open_set[index] = neighbor
        else:
            grid.open_set.append(neighbor)

    background(0)
    # Find the path
    path = find_path(current)
    display_grid(grid, path)


def display_grid(grid, path=None):
    if path is None:
        path = []

    for row in grid.grid:
        for spot in row:
            spot.show(WHITE)

    for spot in grid.open_set:
        spot.show(GREEN)

    for spot in grid.closed_set:
        spot.show(RED)

    for spot in path:
        spot.show(BLUE)

    grid.end_spot.show(PURPLE)


def heuristic(a, b):
    return dist(a.x, a.y, b.x, b.y)  # Both heuristic causes somr end path bugs
    # return abs(a.x-b.x) + abs(a.y-b.y)


def find_path(spot):
    path = []
    path.append(spot)
    while spot.previous:
        path.append(spot.previous)
        spot = spot.previous
    return path
