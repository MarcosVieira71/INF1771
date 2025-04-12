def find_char(mapa, caractere):
    for y, linha in enumerate(mapa):
        for x, celula in enumerate(linha):
            if celula == caractere:
                return (x, y)
            
def manhattan_distance(_from, to):
    # |x2 - x1| + |y2 - y1|
    return abs(to[0] - _from[0]) + abs(to[1] - _from[1])

def is_valid_coord(x, y, width, height):
    return 0 <= x < width and 0 <= y < height