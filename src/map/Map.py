from utils import find_char, is_valid_coord
from .mapConstants import *



class Map:
    def __init__(self, filename):
        self.grid = self.load_map_from_file(filename)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.events = self._find_all_events()

    def load_map_from_file(self, filename):
        with open(filename, 'r') as f:
            return [list(line.strip()) for line in f]

    def _find_all_events(self):
        events = {}
        for symbol in EVENT_SYMBOLS:
            pos = find_char(self.grid, symbol)
            if pos:
                events[symbol] = pos
        return events

    def get_value(self, coord):
        x, y = coord
        cell = self.grid[y][x]
        if cell in TERRAIN_COSTS:
            return TERRAIN_COSTS.get(cell)
        else:
            return 0
        

    def get_neighbors(self, coord):
        x, y = coord
        candidates = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [
            (nx, ny)
            for nx, ny in candidates
            if is_valid_coord(nx, ny, self.width, self.height) and self.get_value((nx, ny)) > -1
        ]

