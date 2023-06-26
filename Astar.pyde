# from processing_mock import *
from spot import Spot

COLS = 25
ROWS = 25
grid = []

open_set = []
closed_set = []

start_spot = None
end_spot = None

WHITE = color(255)
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
PURPLE = color(128, 0, 128)

def setup():
    global grid, start_spot, end_spot
    size(400, 400)
    frameRate(24)
    background(0)
    strokeWeight(1)
    print('A*')

    spot_w = int(width / COLS)
    spot_h = int(height / COLS)

    Spot.set_width_and_height(spot_w, spot_h)
    grid = [[Spot(i, j) for j in range(ROWS)] for i in range(COLS)]
    
    for row in grid:
        for spot in row:
            spot.add_neighbors(grid)
    
    start_spot = grid[0][0]
    end_spot = grid[int(random(COLS))][int(random(ROWS))]

    open_set.append(start_spot)

def draw():
    global grid

    if len(open_set) == 0:
        print('Empty open set')
        return  # Failed

    winner = 0
    for i, spot in enumerate(open_set):
        if spot.f < open_set[winner].f:
            winner = i

    current = open_set[winner]
    if current == end_spot:
        noLoop()

    open_set.remove(current)
    closed_set.append(current)
    
    neighbors = current.neighbors
    for neighbor in neighbors:
        if neighbor in closed_set:
            continue

        temp_g = current.g + 1  # no need to caclulate distance because orthogonal grid

        if neighbor in open_set:
            if temp_g < neighbor.g:
                index = open_set.index(neighbor)
                open_set[index].g = temp_g
                open_set[index].h = heuristic(neighbor, end_spot)
                open_set[index].f = open_set[index].g + open_set[index].h
                open_set[index].previous = current
        else:
            neighbor.g = temp_g
            neighbor.h = heuristic(neighbor, end_spot)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.previous = current
            open_set.append(neighbor)

                
        
                
    background(0)

    # Find the path
    path = find_path(current)
    display_grid(grid, path)


def display_grid(grid, path = []):
    global end_spot
    
    for row in grid:
        for spot in row:
            spot.show(WHITE)

    for spot in open_set:
        spot.show(GREEN)

    for spot in closed_set:
        spot.show(RED)
        
    for spot in path:
        spot.show(BLUE)
        
    end_spot.show(PURPLE)
        
def heuristic(a, b):
    return dist(a.x, a.y, b.x, b.y)
    # return abs(a.x-b.x) + abs(a.y-b.y)

def find_path(spot):
    path = []
    path.append(spot)
    while spot.previous:
        path.append(spot.previous)
        spot = spot.previous
    return path
    
