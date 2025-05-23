from PySide6.QtGui import QColor


EVENT_SPRITES = {
    "1" : "assets/evento_1",
    "2" : "assets/evento_2",
    "3": "assets/evento_3",
    "4": "assets/evento_4",
    "5": "assets/evento_5",
    "6":"assets/evento_6",
    "7": "assets/evento_7",
    "8": "assets/evento_8",
    "9": "assets/evento_9",
    "B": "assets/evento_B",
    "C": "assets/evento_C",
    "D": "assets/evento_D",
    "E": "assets/evento_E",
    "G": "assets/evento_G",
    "H": "assets/evento_H",
    "I": "assets/evento_I",
    "J": "assets/evento_J",
    "K": "assets/evento_K",
    "O": "assets/evento_O"
}

TERRAIN_COSTS = {
    'M': 50,
    'A': 20,
    'N': 15,
    'F': 10,
    'R': 5,
    '.': 1,
    '#': -1,
    "P": 1,
    "0": 1
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
    "O": 100
}

CHARACTER_POWER = {
    "Dragonborn" : 1.8,
    "Ralof" : 1.6,
    "Lydia" : 1.4,
    "Farengar Secret Fire" : 1.3,
    "Balgruuf" : 1.2,
    "Delphine" : 1.0
}
