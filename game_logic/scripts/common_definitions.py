# [IMPORT OF LIBRARIES]
import os

# [COMMON PATHS]
game_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Absolute path of the "game_logic" folder
assets_path = os.path.join(game_path,"assets")                          # Absolute path of the "assets" folder

# [Base width and height for the game]
base_game_width, base_game_height = 640, 360

# [GRID POSITIONING]
x_offset = 8    # 8 pixels of offset (the "0,0" tile will be placed at (8,0) coordinates)

# Function which calculates the coordinates of a given 24x24 tile
def get_tile_coords(tile_idxs):
    '''
    [ARGUMENT]:
    "tile_idxs": 2-elements tuple which represents the indexes of a tile in a 26x15 grid
    
    [RETURN]:
    "tile_coordinates": 2-elements tuple which represents the "on-screen" coordinates of the tile
    '''
    return (x_offset + tile_idxs[0]*24, tile_idxs[1]*24)

# "pogoTile" class: each object of this class represents a pogo tile
class PogoTile:
    def __init__(self, tiletype):
        self.tiletype = tiletype
    def get_tiletype(self):
        return self.tiletype