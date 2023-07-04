from processing_mock import *

WHITE = color(255)
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)
PURPLE = color(128, 0, 128)

width_ = height_ = 800

END_DELAY = 1000


def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)
