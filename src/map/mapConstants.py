from PySide6.QtGui import QColor


TERRAIN_COSTS = {
    'M': 50,
    'A': 20,
    'N': 15,
    'F': 10,
    'R': 5,
    '.': 1,
    '#': -1
}

COLORS = {
    'M': QColor(139, 69, 19),
    'A': QColor(30, 144, 255),
    'N': QColor(34, 139, 34),
    'F': QColor(34, 139, 34),
    'R': QColor(128, 128, 128),
    '.': QColor(255, 255, 255),
    '#': QColor(0, 0, 0)
}

EVENT_COSTS = {
    "0": 1,
    "1": 55,
    "2": 60,
    "3": 65,
    "4": 70,
    "5": 75,
    "6": 80,
    "7": 85,
    "8": 90,
    "9": 95,
    "B": 120,
    "C": 125,
    "D": 130,
    "E": 135,
    "G": 150,
    "H": 155,
    "I": 160,
    "J": 170,
    "K": 180,
    "O": 100,
    "P": 1
}

CHARACTER_POWER = {
    "Dragonborn" : 1.8,
    "Ralof" : 1.6,
    "Lydia" : 1.4,
    "Farengar Secret Fire" : 1.3,
    "Balgruuf" : 1.2,
    "Delphine" : 1.0
}
