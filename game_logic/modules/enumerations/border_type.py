from enum import Enum

class BorderType(Enum):
    SIDE_TILE = 0       # The "border" object is positioned on the side of a tile of the "pogo board"
    ANGLE_BLOCK = 1     # The "angle block" object connects two "side tiles" with different angulation:

                        #  [ ]--
                        #   |