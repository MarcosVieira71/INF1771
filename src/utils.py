from map.mapConstants import CHARACTER_POWER, EVENT_COSTS

def find_char(map, char):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == char:
                return (x, y)
            
def manhattan_distance(_from, to):
    # |x2 - x1| + |y2 - y1|
    return abs(to[0] - _from[0]) + abs(to[1] - _from[1])

def is_valid_coord(x, y, width, height):
    return 0 <= x < width and 0 <= y < height

def event_cost(event, characters):
    sum = 0
    for i in characters:
        sum += CHARACTER_POWER[i]

    cost = EVENT_COSTS[event] / sum

    return cost