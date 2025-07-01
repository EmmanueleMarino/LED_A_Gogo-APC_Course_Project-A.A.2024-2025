'''
Each element of this enumeration indicates whether a tile has been "acquired"
by one of the players by stepping over it and whether 
'''

from enum import Enum


class TileAcquisition(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3