import pygame
import os
from itertools import product

from scripts import common_definitions as cmndef
from scripts import screen_resize as scrsz

pygame.init()

screen = pygame.display.set_mode(cmndef.base_game_size)
grey_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/empty_tile.png"))
blue_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p2_tile.png"))
green_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p1_tile.png"))
red_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p3_tile.png"))
yellow_tile = pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p4_tile.png"))

# The "game_surface" is the surface on which all of the game graphics will be
# rendered on. It gets used in place of the "screen" Surface object, for it
# will be properly resized according to the window size at every game loop cycle.
game_surface = pygame.Surface(cmndef.base_game_size)

# The "playing_surface is the surface underneath the player surface (and other
# "dynamic" surfaces - that is, surfaces upon which several animation frames
# will be drawn).
playing_surface = pygame.Surface(cmndef.base_game_size)

p1_surface = [pygame.image.load(os.path.join(cmndef.assets_path,"players/player_1/frontal_animation/p1_frontal_1.png")),
              pygame.image.load(os.path.join(cmndef.assets_path,"players/player_1/frontal_animation/p1_frontal_2.png")),
              pygame.image.load(os.path.join(cmndef.assets_path,"players/player_1/frontal_animation/p1_frontal_3.png"))]

# The sequence in which the animation frames get played
animation_frames_sequence = [0,1,2,1]

# Which of said frame is being played in
# the current game loop iteration.
current_animation_idx = 0

# The player's position on the screen 
player_position = cmndef.get_tile_related_screen_coords((10,6),cmndef.player_x_offset,cmndef.player_y_offset)

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

# Player animation slowdown index => the game loop gets repeated 60 times a second,
# but the player's animation is made up of three frames only, so the same frame
# has to be repeated multiple times in order for the animation to have the right speed
player_anim_slowdown_idx = 0


#  /---------\
# | Game loop |
#  \---------/
while running:

    # Rendering of the "pogo" tiles matrix
    for x_tile, y_tile in product(range(9,17), range(4,12)):
        playing_surface.blit(tile_matrix[x_tile-9][y_tile-4].get_tiletype(),cmndef.get_tile_related_screen_coords((x_tile,y_tile), cmndef.grid_x_offset, 0))

    game_surface.blit(playing_surface,(0,0))

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

    # Detection of what keys are being
    # continuosly pressed at the moment   
    cont_pressed_keys = pygame.key.get_pressed()
    if cont_pressed_keys[pygame.K_UP]:
        player_position = (player_position[0], player_position[1] - 1)
    if cont_pressed_keys[pygame.K_RIGHT]:
        player_position = (player_position[0] + 1, player_position[1])
    if cont_pressed_keys[pygame.K_DOWN]:
        player_position = (player_position[0], player_position[1] + 1)
    if cont_pressed_keys[pygame.K_LEFT]:
        player_position = (player_position[0] - 1, player_position[1])


    # Blitting the player on the game surface (not on the playing surface, given that
    # the back of the player's sprite will be cut out off of said surface)
    game_surface.blit(p1_surface[animation_frames_sequence[current_animation_idx]],
                      player_position)
    
    # The player animation only gets changed every "player_slowdown_constant/60"th of a second
    if(player_anim_slowdown_idx == cmndef.player_slowdown_constant):
        player_anim_slowdown_idx = 0
        current_animation_idx = (current_animation_idx + 1) % 4

    # At each game loop iteration, the slowdown index gets increased
    player_anim_slowdown_idx += 1

    screen.blit(game_surface, (0,0))
    pygame.display.flip()

    # Wait for 60 ticks
    clock.tick(60)

pygame.quit()