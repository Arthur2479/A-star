from processing_mock import *
from grid import Grid
from spot import Spot
from utils import width_, height_, END_DELAY, heuristic

grid = Grid()


def setup():
    size(width_, height_)
    frameRate(24)
    background(0)
    print('A*')

    spot_w = int(width / Grid.COLS)
    spot_h = int(height / Grid.COLS)

    Spot.set_width_and_height(spot_w, spot_h)

    grid.setup_grid(random_end=True)


def draw():
    if len(grid.open_set) == 0:
        # iteration_saver('Failure', grid, current)
        delay(END_DELAY)
        grid.setup_grid(random_end=True)
        return  # No possible path

    winner = find_winner_index(grid)
    current = grid.open_set[winner]
    if current == grid.end_spot:
        iteration_saver('Success', grid, current)
        delay(END_DELAY)
        grid.setup_grid(random_end=True)
        return

    grid.open_set.remove(current)
    grid.closed_set.append(current)

    discover_neighbors(current)

    background(0)
    # Find the path
    path = grid.find_path(current)
    grid.display_grid(path)


def mouseDragged():
    grid.place_or_remove_wall()


def mouseClicked():
    grid.place_or_remove_wall()


def keyPressed():
    if key == "r" or key == "R":
        grid.restart_sim()


def iteration_saver(status, grid, current):
    # TODO : create a file per day ?
    # TODO : improve readability
    # FIXME : cols are stored in lines
    # TODO : add game games : algorithm, cols & grids, ...
    with open('./games/games.txt', 'a') as file:
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
        file.write(str([(spot.x, spot.y) for spot in grid.find_path(current)]))
        file.write('\n\n')


def find_winner_index(grid_):
    winner = 0
    for i, spot in enumerate(grid_.open_set):
        if spot.f < grid_.open_set[winner].f:
            winner = i
    return winner


def discover_neighbors(current):
    neighbors = current.neighbors
    for neighbor in neighbors:
        if neighbor in grid.closed_set or neighbor.block:
            continue

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
