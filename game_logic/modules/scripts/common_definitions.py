# [IMPORT OF LIBRARIES]
import os
import pygame
from math import floor

# [COMMON PATHS]
game_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Absolute path of the "game_logic" folder
assets_path = os.path.join(game_path,"assets")                          # Absolute path of the "assets" folder

# [TIMER SURFACES]
TIMER_DIGITS_SURFACES = [pygame.image.load(os.path.join(assets_path, f"hud/timer_digits/timer_digit_{i}.png")) for i in range(10)]
TIMER_DIGITS_SHADOWS = [pygame.image.load(os.path.join(assets_path, f"hud/timer_digits/shadows/timer_digit_{i}.png")) for i in range(10)]
TIMER_COLON_SURFACE = pygame.image.load(os.path.join(assets_path, f"hud/timer_digits/colon.png"))
TIMER_COLON_SHADOW = pygame.image.load(os.path.join(assets_path, f"hud/timer_digits/shadows/colon.png"))

# [Base width and height for the game]
base_game_size = (640, 360)

# [Fullscreen width and height]
fullscreen_game_size = (1280, 720)

# [OFFSETS FOR THE POSITIONING OF SPRITES ON THE GRID]
grid_x_offset = 8

# [MAXIMUM SCORE]
MAX_SCORE = 1950

# [MAXIMUM DURATION OF A GAME SESSION (in seconds)]
MAX_TIME = 120

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

# Function which updates the timer's surface
# (Should we define a "Timer" class? I don't think it's necessary, tbh)
def update_timer_surface(time_in_sec):
    '''
    [PARAMETER]:
        "time_in_sec" : the time which has to be displayed on the surface.
    [RETURN]:
        "updated_surface" : the surface which has been
                            updated in the current game loop
    '''
    # A transparent "base surface" gets created
    digits_surface =  pygame.Surface((120, 40), pygame.SRCALPHA)

    # The minutes get computed by dividing the
    # seconds by 60 and applying the "floor" function
    # (the division's result gets approximated to the
    # immediately lower integer)
    minutes = floor(time_in_sec/60)
    seconds = time_in_sec - (minutes * 60)

    # "String" versions of minutes and seconds
    # (A padding gets added if necessary)
    minutes_string = (2-len(str(minutes)))*"0" + str(minutes)
    seconds_string = (2-len(str(seconds)))*"0" + str(seconds)

    #  /--------------------------------------------------------------------------\
    # | The surface gets constructed by blitting on the transparent "base surface" |
    #  \--------------------------------------------------------------------------/
    digits_surface.blit(TIMER_DIGITS_SURFACES[int(minutes_string[0])],(0,0))
    digits_surface.blit(TIMER_DIGITS_SURFACES[int(minutes_string[1])],(24,0))
    digits_surface.blit(TIMER_COLON_SURFACE,(48,0))
    digits_surface.blit(TIMER_DIGITS_SURFACES[int(seconds_string[0])],(72,0))
    digits_surface.blit(TIMER_DIGITS_SURFACES[int(seconds_string[1])],(96,0))

    # A new bigger surface gets created and shadows get blitted on it
    shadows_surface =  pygame.Surface((176, 100), pygame.SRCALPHA)

    for i in range(2):
        shadows_surface.blit(TIMER_DIGITS_SHADOWS[int(minutes_string[0])],(0,0))
        shadows_surface.blit(TIMER_DIGITS_SHADOWS[int(minutes_string[1])],(24,0))
        shadows_surface.blit(TIMER_COLON_SHADOW,(48,0))
        shadows_surface.blit(TIMER_DIGITS_SHADOWS[int(seconds_string[0])],(72,0))
        shadows_surface.blit(TIMER_DIGITS_SHADOWS[int(seconds_string[1])],(96,0))

    # The complete shadow gets computed by blitting the digits_surface on the
    # "shadows_surface" (so that the shadows are displayed underneath the digits)

    shadows_surface.blit(digits_surface,(38,30))

    return shadows_surface