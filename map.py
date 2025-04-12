from PySide6.QtGui import QColor
from utils import find_char

def loadMap(nome_arquivo):
    map = []
    with open(nome_arquivo, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                map.append(list(line))
    return map

map = loadMap("mapa_skyrim.txt")

colors = {
    'M': QColor(139, 69, 19),   
    'A': QColor(30, 144, 255),  
    'N': QColor(34, 139, 34),   
    'F': QColor(34, 139, 34),   
    'R': QColor(128, 128, 128), 
    '.': QColor(255, 255, 255), 
    '#': QColor(0, 0, 0)      
}

time = {
    'M': 50,   
    'A': 20,  
    'N': 15,   
    'F': 10,   
    'R': 5, 
    '.': 1,
    '#': -1       
}


events = {
    '0': find_char(map,'0'),
    '1': find_char(map,'1'),
    '2': find_char(map,'2'),
    '3': find_char(map,'3'),
    '4': find_char(map,'4'),
    '5': find_char(map,'5'),
    '6': find_char(map,'6'),
    '7': find_char(map,'7'),
    '8': find_char(map,'8'),
    '9': find_char(map,'9'),
    'B': find_char(map,'B'),
    'C': find_char(map,'C'),
    'D': find_char(map,'D'),
    'E': find_char(map,'E'),
    'G': find_char(map,'G'),
    'H': find_char(map,'H'),
    'I': find_char(map,'I'),
    'J': find_char(map,'J'),
    'K': find_char(map,'K'),
    'O': find_char(map,'O'),
    'P': find_char(map,'P')
}