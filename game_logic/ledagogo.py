import pygame
import os
from itertools import product

from modules.scripts import common_definitions as cmndef
from modules.scripts import screen_resize as scrsz
from modules.entities.player import Player
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

    # Rendering of the "pogo" tiles matrix (CODE TO REFACTOR)
    for x_tile, y_tile in product(range(9,17), range(4,12)):
        #  /------------------------------------\
        # | RENDERING OF THE "POGO BOARD" BORDER |
        #  \------------------------------------/
        if x_tile == 9:
            playing_surface.blit(board_border_side,cmndef.get_tile_related_screen_coords((x_tile-1,y_tile),cmndef.grid_x_offset+12,0))
        if x_tile == 16:
            playing_surface.blit(board_border_side,cmndef.get_tile_related_screen_coords((x_tile+1,y_tile),cmndef.grid_x_offset,0))
        if y_tile == 4:
            playing_surface.blit(pygame.transform.rotate(board_border_side, 90),cmndef.get_tile_related_screen_coords((x_tile,y_tile-1),cmndef.grid_x_offset,+12))
        if y_tile == 11:
            playing_surface.blit(pygame.transform.rotate(board_border_side, 90),cmndef.get_tile_related_screen_coords((x_tile,y_tile+1),cmndef.grid_x_offset,0))
        if x_tile == 9 and y_tile == 4:
            playing_surface.blit(board_border_angle,cmndef.get_tile_related_screen_coords((x_tile-1,y_tile-1),cmndef.grid_x_offset+12,12))
        if x_tile == 16 and y_tile == 4:
            playing_surface.blit(board_border_angle,cmndef.get_tile_related_screen_coords((x_tile+1,y_tile-1),cmndef.grid_x_offset,12))
        if x_tile == 9 and y_tile == 11:
            playing_surface.blit(board_border_angle,cmndef.get_tile_related_screen_coords((x_tile-1,y_tile+1),cmndef.grid_x_offset+12,0))
        if x_tile == 16 and y_tile == 11:
            playing_surface.blit(board_border_angle,cmndef.get_tile_related_screen_coords((x_tile+1,y_tile+1),cmndef.grid_x_offset,0))

        #  /-----------------------------\
        # | RENDERING OF THE BOARD ITSELF |
        #  \-----------------------------/ 
        playing_surface.blit(tile_matrix[x_tile-9][y_tile-4].get_tiletype(),cmndef.get_tile_related_screen_coords((x_tile,y_tile), cmndef.grid_x_offset, 0))

    game_surface.blit(playing_surface,(0,0))

    # The "colliders" for the current player
    # are computed 
    colliders = players + []
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

    screen.blit(game_surface, (0,0))
    pygame.display.flip()

    # Wait for 60 ticks
    clock.tick(60)

pygame.quit()