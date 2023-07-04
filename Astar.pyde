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

    def locate_point(self, x, y):
        i = floor(self.COLS * x / width)
        j = floor(self.ROWS * y / height)
        return i, j


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
        # iteration_saver('Failure', grid, current)
        delay(1000)
        grid.setup_grid(random_end=True)
        return  # Failed

    winner = 0
    for i, spot in enumerate(grid.open_set):
        if spot.f < grid.open_set[winner].f:
            winner = i

    current = grid.open_set[winner]
    if current == grid.end_spot:
        iteration_saver('Success', grid, current)
        delay(1000)
        grid.setup_grid(random_end=True)
        return

    grid.open_set.remove(current)
    grid.closed_set.append(current)

    neighbors = current.neighbors
    for neighbor in neighbors:
        if neighbor in grid.closed_set or neighbor.block:
            continue

        # FIXME : a bit ugly and complex
        if neighbor in current.radial_neighbors:
            temp_g = current.g + 1
        if neighbor in current.diagonal_neighbors:
            temp_g = current.g + 1.41

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


def mouseDragged():
    place_or_remove_wall()


def mouseClicked():
    place_or_remove_wall()


def place_or_remove_wall():
    x, y = grid.locate_point(mouseX, mouseY)
    if mouseButton == LEFT and not grid.grid[x][y].block:
        grid.grid[x][y].block = True
        grid.restart_sim()
    elif mouseButton == RIGHT and grid.grid[x][y].block:
        grid.grid[x][y].block = False
        grid.restart_sim()


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
    return abs(a.x - b.x) + abs(a.y - b.y)


def find_path(spot):
    path = [spot]
    while spot.previous:
        path.append(spot.previous)
        spot = spot.previous
    return path


def iteration_saver(status, grid, current):
    # TODO : create a file per day ?
    # TODO : improve readability
    # FIXME : cols are stored in lines
    # TODO : add game data : algorithm, cols & grids, ...
    with open('./data/games.txt', 'a') as file:
        walls = ''
        for col in grid.grid:
            for spot in col:
                if spot.block:
                    walls += 'x'
                else:
                    walls += ' '
            walls += ', '

        file.write('##################################\n\n')
        file.write(status + ':')
        file.write(str(walls))
        file.write('\nEnd path: ')
        file.write(str([(spot.x, spot.y) for spot in find_path(current)]))
        file.write('\n\n')
