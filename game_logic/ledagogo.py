import pygame
import os
from itertools import product

from modules.scripts import common_definitions as cmndef
from modules.scripts import screen_resize as scrsz
from modules.entities.player import Player
from modules.entities.board_border import BoardBorder
from modules.enumerations.border_type import BorderType
from modules.enumerations.direction import Direction

screen = pygame.display.set_mode(cmndef.base_game_size)
grey_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/empty_tile.png"))
blue_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p2_tile.png"))
green_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p1_tile.png"))
red_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p3_tile.png"))
yellow_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p4_tile.png"))

board_border_side = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/border_tiles/grey_side.png"))
board_border_angle = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/border_tiles/grey_angle.png"))

# The "game_surface" is the surface on which all of the game graphics will be
# rendered on. It gets used in place of the "screen" Surface object, for it
# will be properly resized according to the window size at every game loop cycle.
game_surface = pygame.Surface(cmndef.base_game_size)

# The "playing_surface is the surface underneath the player surface (and other
# "dynamic" surfaces - that is, surfaces upon which several animation frames
# will be drawn).
playing_surface = pygame.Surface(cmndef.base_game_size)

# Starting positions on the grid for each player
players_starting_positions = [(10,5), (15,5), (10,10), (15,10)]

#  /----------------------------------------------\
# | SURFACES OF THE VARIOUS GAME SCENARIO ELEMENTS |
#  \----------------------------------------------/
underneath_the_board = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/underneath_the_board.png"))
background_surface = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/background.png"))
board_shadows = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/board_shadows.png")).convert_alpha()
global_shadow = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/global_shadow.png")).convert_alpha()
board_upper_light = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/board_upper_light.png")).convert_alpha()
shadows_under_the_board = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/shadows_under_the_board.png")).convert_alpha()
lights_and_ambience = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/lights_and_ambience.png")).convert_alpha()


# The players get instantiated
players = []
for i in range(4):
    players.append(Player(players_starting_positions[i],i+1))

# [FOR DEBUGGING PURPOSES] - Index of the currently controlled player
current_player = 0

# "Clock" object to ensure the game loop gets played every 1/60th of a second
# (The game gets capped at 60FPS)
clock = pygame.time.Clock()

pygame.display.set_caption("LED-A-Gogo (APC Project - A.A. 2024/2025)")

icon_surface = pygame.image.load(os.path.join(cmndef.assets_path, "logo_redux.png")).convert_alpha()
pygame.display.set_icon(icon_surface)

# Pogo tiles matrix (maybe I'll create a more structured data structure, this matrix
# of tiles is only for tests)
tile_matrix = []

# Instantiation of the matrix of "pogo" tiles (it's an 8x8 square grid, but
# we'll probably decide on a different size)... it depends on future implementation decisions
for i in range(8):
    row = []
    row.append(cmndef.PogoTile(grey_tile))
    for j in range(1,4):
        if(j % 2 == 0):
            row.append(cmndef.PogoTile(green_tile))
        else:
            row.append(cmndef.PogoTile(red_tile))
    for j in range(5,8):
        if(j % 2 == 0):
            row.append(cmndef.PogoTile(blue_tile))
        else:
            row.append(cmndef.PogoTile(yellow_tile))
    row.append(cmndef.PogoTile(grey_tile))

    tile_matrix.append(row)


# Building a dictionary of "BoardBorder" objects
board_borders = {}

# The "angles" field will be a list of BoardBorder
# objects of the "ANGLE_BLOCK" type
angle_blocks = []
angle_blocks.append(BoardBorder((8,4), BorderType.ANGLE_BLOCK, (Direction.UP,Direction.LEFT)))
angle_blocks.append(BoardBorder((17,4), BorderType.ANGLE_BLOCK, (Direction.UP,Direction.RIGHT)))
angle_blocks.append(BoardBorder((17,13), BorderType.ANGLE_BLOCK, (Direction.DOWN,Direction.RIGHT)))
angle_blocks.append(BoardBorder((8,13), BorderType.ANGLE_BLOCK, (Direction.DOWN,Direction.LEFT)))

# The "sides" field will be a matrix of BoardBorder
# objects of the "SIDE_TILE" type, where each row
# will represent a different orientation of the
# tile objects it contains
side_tiles = []

# [ROW 0] = "UP" -> Upper border
upper_border = []
for i in range(8):
    upper_border.append(BoardBorder((9+i,4), BorderType.SIDE_TILE, Direction.UP))
side_tiles.append(upper_border)

# [ROW 1] = "RIGHT" -> Right border
right_border = []
for i in range(8):
    right_border.append(BoardBorder((17,5+i), BorderType.SIDE_TILE, Direction.RIGHT))
side_tiles.append(right_border)

# [ROW 2] = "DOWN" -> Lower border
lower_border = []
for i in range(8):
    lower_border.append(BoardBorder((9+i,13), BorderType.SIDE_TILE, Direction.DOWN))
side_tiles.append(lower_border)

# [ROW 3] = "LEFT" -> Left border
left_border = []
for i in range(8):
    left_border.append(BoardBorder((8,5+i), BorderType.SIDE_TILE, Direction.LEFT))
side_tiles.append(left_border)

board_borders['angle_blocks'] = angle_blocks
board_borders['side_tiles'] = side_tiles

# Game loop running state
running = True

# Fullscreen state
fullscreen = False

# Scaled state
scaled = False

#  /---------\
# | Game loop |
#  \---------/
while running:
    # Rendering of the game scenario backgrond
    playing_surface.blit(background_surface,(0,0))

    # Rendering the shadows underneath the board
    playing_surface.blit(shadows_under_the_board,(0,0))

    # Rendering of the "underneath part" of the board
    playing_surface.blit(underneath_the_board,(0,0))

    # Rendering of the "pogo" tiles matrix
    for x_tile, y_tile in product(range(9,17), range(5,13)):
        playing_surface.blit(tile_matrix[x_tile-9][y_tile-5].get_tiletype(),cmndef.get_tile_related_screen_coords((x_tile,y_tile), cmndef.grid_x_offset, 0))

    # [Rendering of the "pogo" board border]
    # Rendering of the side tiles
    for tile_row in board_borders['side_tiles']:
        for side_tile in tile_row:
            playing_surface.blit(side_tile.surface, side_tile.screen_position)
            #pygame.draw.rect(playing_surface, (255,0,0), side_tile.hitbox) # -> [FOR DEBUGGING PURPOSES]

    # Rendering of the angle blocks
    for angle_block in board_borders["angle_blocks"]:
        playing_surface.blit(angle_block.surface, angle_block.screen_position)
        #pygame.draw.rect(playing_surface, (255,0,0), angle_block.hitbox) # -> [FOR DEBUGGING PURPOSES]

    # Rendering of the board shadows
    playing_surface.blit(board_shadows,(0,0))

    # Rendering the board's upper light
    playing_surface.blit(board_upper_light,(0,0))

    # The playing surface gets blitted on the
    # global game surface.
    game_surface.blit(playing_surface,(0,0))

    # The "colliders" for the current player
    # are computed (on two separate lines, simply
    # for the sake of readiblity)
    colliders = players + board_borders['side_tiles'][Direction.UP.value] + board_borders['side_tiles'][Direction.RIGHT.value]
    colliders = colliders + board_borders['side_tiles'][Direction.DOWN.value] + board_borders['side_tiles'][Direction.LEFT.value]
    del colliders[current_player]

    # Event detection in the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detection of a single key pressing 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen, game_surface, screen = scrsz.toggle_fullscreen(fullscreen,scaled,game_surface,screen)

            elif event.key == pygame.K_F10:
                scaled, game_surface, screen = scrsz.toggle_scaled_2x(fullscreen, scaled, game_surface, screen)

            elif event.key == pygame.K_UP:
                players[current_player].change_direction(Direction.UP)
            elif event.key == pygame.K_RIGHT:
                players[current_player].change_direction(Direction.RIGHT)
            elif event.key == pygame.K_DOWN:
                players[current_player].change_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT:
                players[current_player].change_direction(Direction.LEFT)

            # [FOR DEBUGGING PURPOSES] - Change the currently controlled player
            elif event.key == pygame.K_TAB:
                current_player = (current_player + 1) % 4

    # [LAST POSITION UPDATE]
    last_position_update = (0,0)

    # Detection of what keys are being
    # continuosly pressed at the moment   
    cont_pressed_keys = pygame.key.get_pressed()
    if cont_pressed_keys[pygame.K_UP]:
        last_position_update = ((0,-1))
        players[current_player].update_position((0,-1))
    elif cont_pressed_keys[pygame.K_RIGHT]:
        last_position_update = ((1,0))
        players[current_player].update_position((1,0))
    elif cont_pressed_keys[pygame.K_DOWN]:
        last_position_update = ((0,1))
        players[current_player].update_position((0,1))
    elif cont_pressed_keys[pygame.K_LEFT]:
        last_position_update = ((-1,0))
        players[current_player].update_position((-1,0))

    # If the movement has caused the current player to collide,
    # the position update gets reverted before the actual blitting.
    # By doing so, the player's hitbox won't get stuck into other
    # player's (or entity's) hitboxes.
    if(players[current_player].check_collisions(colliders)):
        players[current_player].update_position((last_position_update[0] * -1,
                                                 last_position_update[1] * -1))

    #  /-----------------------------------------------------------------------------\
    # | Blitting the player(s) on the game surface (not on the playing surface, given | 
    # | that the back of the player's sprite will be cut out off of said surface)     |
    #  \-----------------------------------------------------------------------------/
    # The order in which the players get blitted is ascending with the "Y" screen
    # coordinate (if a player has got a bigger "Y" screen coordinate, said player is
    # positioned closer to the camera)
    sorted_players = sorted(players, key=lambda p: p.screen_position[1])
    for i in range(4):
        #pygame.draw.rect(game_surface, (255,0,0), sorted_players[i].hitbox) # -> [FOR DEBUGGING PURPOSES]
        game_surface.blit(sorted_players[i].surface,
                          sorted_players[i].screen_position)
    
    # The players surfaces get updated
    for i in range(4):
        players[i].compute_surface()

    # Rendering the global shadows
    game_surface.blit(global_shadow,(0,0))

    # Rendering the global lights and ambience
    game_surface.blit(lights_and_ambience,(0,0))

    screen.blit(game_surface, (0,0))
    pygame.display.flip()

    # Wait for 60 ticks
    clock.tick(60)

pygame.quit()