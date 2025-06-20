import pygame
import os
from itertools import product

from scripts import common_definitions as cmndef
from scripts import screen_resize as scrsz

pygame.init()

screen = pygame.display.set_mode(cmndef.base_game_size)
grey_tile = pygame.image.load(os.path.join(cmndef.assets_path, "pogo_tile.png"))
blue_tile = pygame.image.load(os.path.join(cmndef.assets_path, "blue_tile.png"))
green_tile = pygame.image.load(os.path.join(cmndef.assets_path, "green_tile.png"))

# The "game_surface" is the surface on which all of the game graphics will be
# rendered on. It gets used in place of the "screen" Surface object, for it
# will be properly resized according to the window size at every game loop cycle.
game_surface = game_surface = pygame.Surface(cmndef.base_game_size)

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
        row.append(cmndef.PogoTile(green_tile))
    for j in range(5,8):
        row.append(cmndef.PogoTile(blue_tile))
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

    # Rendering of the "pogo" tiles matrix
    for x_tile, y_tile in product(range(9,17), range(4,12)):
        game_surface.blit(tile_matrix[x_tile-9][y_tile-4].get_tiletype(),cmndef.get_tile_coords((x_tile,y_tile)))

    # Event detection in the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen, game_surface, screen = scrsz.toggle_fullscreen(fullscreen,scaled,game_surface,screen)

            elif event.key == pygame.K_F10:
                scaled, game_surface, screen = scrsz.toggle_scaled_2x(fullscreen, scaled, game_surface, screen)

    screen.blit(game_surface, (0,0))
    pygame.display.flip()        

pygame.quit()