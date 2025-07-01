'''
[POGO TILE]:
This class models the tiles on the "pogo board"
'''

# [IMPORT OF LIBRARIES]
from modules.entities.entity import Entity
from modules.scripts import common_definitions as cmndef
import os
import pygame


# "pogoTile" class: each object of this class represents a pogo tile
class PogoTile(Entity):
    #  /----------------\
    # | STATIC CONSTANTS |
    #  \----------------/
    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE
    #  SPRITE RELATIVELY TO THE GRID]
    GRID_X_OFFSET = 8
    GRID_Y_OFFSET = 0

    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE HITBOX
    #  RELATIVELY TO THE ENTITY SPRITE]
    HITBOX_X_OFFSET = 11
    HITBOX_Y_OFFSET = 11

    # [Class constructor]
    def __init__(self, grid_position):
        '''
        [PARAMETERS]:
        The here undocumented parameters are
        documented in the upper "Entity" class.
        '''

        # "surface_vector" is the vector which contains the four
        # different surfaces which can be attributed to the
        # current tile object.
        self.surface_vector = [pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/empty_tile.png")),
                               pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p1_tile.png")),
                               pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p2_tile.png")),
                               pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p3_tile.png")),
                               pygame.image.load(os.path.join(cmndef.assets_path, "tiles/pogo_tiles/p4_tile.png"))]

        #  /--------------------------------------------------------------------\
        # | ID of the player who acquired this cell of the "pogo board".         | 
        # | It can be "0" (the cell is free) or "1, 2, 3, 4", which are          |
        # | the proper values of the "player_id" attribute of the "Player" class |
        #  \--------------------------------------------------------------------/
        self.player_id = 0      # The cell is initially free

        # The constructor of the upper class gets called
        super().__init__(grid_position, surface=self.surface_vector[0], hitbox_size=(2,2))


    # [Method to compute the entity surface at each game loop]
    def compute_surface(self):
        self.surface = self.surface_vector[self.player_id]
    
    # [Method to change the player id relative to
    #  the player who has acquired the tile]
    def change_acquisition(self, player_id):
        # It's a simple method, but I deemed it cleaner
        # to set this information via a method, rather than
        # accessing the object's attribute directly
        self.player_id = player_id