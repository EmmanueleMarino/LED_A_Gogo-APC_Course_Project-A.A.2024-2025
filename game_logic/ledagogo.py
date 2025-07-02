import pygame
import os

from modules.scripts import common_definitions as cmndef
from modules.scripts import screen_resize as scrsz
from modules.entities.player import Player
from modules.pogo_board import PogoBoard
from modules.enumerations.direction import Direction
from modules.scripts.find_smallest_rectangle import find_smallest_rectangle

screen = pygame.display.set_mode(cmndef.base_game_size)

# The "game_surface" is the surface on which all of the game graphics will be
# rendered on. It gets used in place of the "screen" Surface object, for it
# will be properly resized according to the window size at every game loop cycle.
game_surface = pygame.Surface(cmndef.base_game_size)

# The "playing_surface is the surface underneath the player surface (and other
# "dynamic" surfaces - that is, surfaces upon which several animation frames
# will be drawn).
playing_surface = pygame.Surface(cmndef.base_game_size)

# Starting positions on the grid for each player
players_starting_positions = [(10,6), (15,6), (10,11), (15,11)]

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

# An "8x8" pogo board gets instantiated
# starting from the "(9,5)" tile on the
# 26x15 grid
pogo_board = PogoBoard((8,8), (9,5))

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
    for tile_row in pogo_board.pogo_tiles:
        for tile in tile_row:
            playing_surface.blit(tile.surface, tile.screen_position)
            #pygame.draw.rect(playing_surface, (255,0,0), tile.hitbox) # -> [FOR DEBUGGING PURPOSES]

    # [Rendering of the "pogo board" boarder]
    # Rendering of the side tiles
    for tile_row in pogo_board.board_borders['side_tiles']:
        for side_tile in tile_row:
            playing_surface.blit(side_tile.surface, side_tile.screen_position)
            #pygame.draw.rect(playing_surface, (255,0,0), side_tile.hitbox) # -> [FOR DEBUGGING PURPOSES]

    # Rendering of the angle blocks
    for angle_block in pogo_board.board_borders['angle_blocks']:
        playing_surface.blit(angle_block.surface, angle_block.screen_position)
        
    # Rendering of the board shadows
    playing_surface.blit(board_shadows,(0,0))

    # Rendering the board's upper light
    playing_surface.blit(board_upper_light,(0,0))

    # The playing surface gets blitted on the
    # global game surface.
    game_surface.blit(playing_surface,(0,0))

    # The "colliders" for the current player
    # are computed (on separate lines, simply
    # for the sake of readiblity)
    colliders = players + []
    colliders += pogo_board.board_borders['side_tiles'][Direction.UP.value]
    colliders += pogo_board.board_borders['side_tiles'][Direction.RIGHT.value]
    colliders += pogo_board.board_borders['side_tiles'][Direction.DOWN.value]
    colliders += pogo_board.board_borders['side_tiles'][Direction.LEFT.value]
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

    #  /----------------------------------------------------------------\
    # | CHECK IF THE "CHANGE TILE ACQUISITION" EVENT HAS TO BE TRIGGERED |
    #  \----------------------------------------------------------------/
    for i in range(len(pogo_board.pogo_tiles)):
        for j in range(len(pogo_board.pogo_tiles[0])):
            # [If the player collides with the tile's hitbox]
            if(players[current_player].check_collisions([pogo_board.pogo_tiles[i][j]])):
                # Change the "player_id" for the tile
                pogo_board.pogo_tiles[i][j].change_acquisition(players[current_player].player_id)

                # Update the status of the board: the "i,j" element of the "player_id - 1" matrix
                # of the status will be set to "1", the same element of the two remaining matrices
                # will be set to "0"
                for z in range(1, len(players)+1):
                    if z == players[current_player].player_id:
                        pogo_board.status[z-1][i][j] = 1
                    else:
                        pogo_board.status[z-1][i][j] = 0
                
                # Check if a rectangle has been closed
                closed_rectangle = find_smallest_rectangle(pogo_board.status[players[current_player].player_id - 1],(3,3))

                # If the player has closed a rectangle
                if(closed_rectangle[0] != (-1,-1)):
                    # [PRINT FOR DEBUGGING PURPOSES]
                    #print(f"Player {players[current_player].player_id} closed a {closed_rectangle[1]}x{closed_rectangle[2]} rectangle at the following path: {closed_rectangle[3]}")

                    # The player's score gets updated with the rectangle's area
                    players[current_player].update_score_and_leds(closed_rectangle[1]*closed_rectangle[2])

                    # [PRINT FOR DEBUGGING PURPOSES]
                    #print(f"Player {players[current_player].player_id}'s current score is {players[current_player].score}")

                    # [THE TILES CORRESPONDING TO THE CLOSED RECTANGLE GET "RESET"-TED]
                    for tile_coordinates in closed_rectangle[3]:
                        pogo_board.pogo_tiles[tile_coordinates[0]][tile_coordinates[1]].change_acquisition(0)
                        pogo_board.status[players[current_player].player_id - 1][tile_coordinates[0]][tile_coordinates[1]] = 0
                    

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

    # Rendering the global shadows
    game_surface.blit(global_shadow,(0,0))

    # Rendering the global lights and ambience
    game_surface.blit(lights_and_ambience,(0,0))
    
    # [THE HUD GETS BLITTED ON TOP OF EVERYTHING]
    for i in range(4):
        game_surface.blit(players[i].scorer.surface, players[i].scorer.screen_position)

    screen.blit(game_surface, (0,0))
    pygame.display.flip()

    # The players surfaces get updated
    for i in range(4):
        players[i].compute_surface()
        players[i].scorer.compute_surface()

    # The surfaces for the
    # board's tiles get updated
    pogo_board.compute_surfaces()

    # Wait for 60 ticks
    clock.tick(60)

pygame.quit()