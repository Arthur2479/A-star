from processing_mock import *
from grid import Grid
from spot import Spot
from utils import width_, height_, END_DELAY

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
    if grid.pause:
        return

    if len(grid.open_set) == 0:
        # If stuck at the beginning because of random generation, clear the path a bit
        if len(grid.closed_set) < 10 and grid.tries < 5:
            grid.clear_entrance()
            return

        delay(END_DELAY)
        grid.setup_grid(random_end=True)
        return  # No possible path

    winner = grid.find_winner_index()
    current = grid.open_set[winner]
    if current == grid.end_spot:
        delay(END_DELAY)
        grid.setup_grid(random_end=True)
        return

    grid.open_set.remove(current)
    grid.closed_set.append(current)

    grid.discover_neighbors(current)

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
    elif key == "p" or key == "P":
        grid.pause = not grid.pause
    elif key == "n" or key == "N":  # Next
        grid.setup_grid(random_end=True)
