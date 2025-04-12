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

EVENT_SYMBOLS = list('0123456789BCDEGHIJKOP')