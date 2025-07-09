'''
[POWER UP]:
This class models the "lightning" power up which gets positioned on
the map at regular time intervals and at random positions on the board.
'''

# [IMPORT OF LIBRARIES]
from modules.scripts import common_definitions as cmndef
from modules.entities.entity import Entity
import pygame
import os


class PowerUp(Entity):
    #  /----------------\
    # | STATIC CONSTANTS |
    #  \----------------/
    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE
    #  SPRITE RELATIVELY TO THE GRID]
    GRID_X_OFFSET = 5
    GRID_Y_OFFSET = -3

    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE HITBOX
    #  RELATIVELY TO THE ENTITY SPRITE]
    HITBOX_X_OFFSET = 14
    HITBOX_Y_OFFSET = 14

    # [Class constructor]
    def __init__(self, grid_position, instantiation_time):
        self.grid_position = grid_position
        
        self.instantiation_time = instantiation_time    # The second at which the
                                                        # power up gets instantiated

        # Validity (in seconds) of the power up.
        self.initial_validity = 7          
        self.validity = self.initial_validity           # After this time elapses, the power up
                                                        # gets removed from the board.

        # "validity" is the attribute which gets updated at every second
        # "initial_validity" is the constant initial value of said
        # attribute (its value is now predetermined at "7", but it could
        # be changed if we deem it too short or too long).

        # The constructor of the upper class gets called
        super().__init__(grid_position,
                         surface=pygame.image.load(os.path.join(cmndef.assets_path,"tiles/power_up_tile_shining.png")),
                         hitbox_size=(2,2))


    # [Method to compute the entity surface at each game loop]
    def compute_surface(self):
        # [FOR NOW, THE POWER UP SPRITE IS NOT ANIMATED, SO
        #  THERE'S JUST A SINGLE UNCHANGING SURFACE FOR IT]
        pass    # No implementation