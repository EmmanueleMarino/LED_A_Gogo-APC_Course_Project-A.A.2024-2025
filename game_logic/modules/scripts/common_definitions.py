# [IMPORT OF LIBRARIES]
import os

# [COMMON PATHS]
game_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Absolute path of the "game_logic" folder
assets_path = os.path.join(game_path,"assets")                          # Absolute path of the "assets" folder

# [Base width and height for the game]
base_game_size = (640, 360)

# [Fullscreen width and height]
fullscreen_game_size = (1280, 720)

# [OFFSETS FOR THE POSITIONING OF SPRITES ON THE GRID]
grid_x_offset = 8

# [MAXIMUM SCORE]
MAX_SCORE = 1950

# Function which calculates the screen coordinates of a sprite relatively to a 26x15 grid of 24x24 tiles
def get_tile_related_screen_coords(tile_idxs, x_offset, y_offset):
    '''
    [ARGUMENT]:
    "tile_idxs": 2-elements tuple which represents the indexes of a tile in a 26x15 grid
    "x_offset" : Offset (in pixels) on the x-axis
    "y_offset" : Offset (in pixels) on the y-axis
    
    [RETURN]:
    "tile_coordinates": 2-elements tuple which represents the "on-screen" coordinates of the tile
    '''
    return (x_offset + tile_idxs[0]*24, y_offset + tile_idxs[1]*24)