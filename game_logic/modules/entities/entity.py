'''
[GENERIC ENTITY]:
This class models the generic "entity" which can get positioned
on the 26x15 grid in which the playing surface is divided.
'''

# [IMPORT OF LIBRARIES]
from modules.scripts import common_definitions as cmndef
import pygame
from abc import ABC, abstractmethod     # "Entity" is an abstract class, so it has to
                                        # inherit from the "ABC" class.

class Entity(ABC):
    #  /----------------\
    # | STATIC CONSTANTS |
    #  \----------------/
    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE
    #  SPRITE RELATIVELY TO THE GRID]
    GRID_X_OFFSET = 0
    GRID_Y_OFFSET = 0

    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE HITBOX
    #  RELATIVELY TO THE ENTITY SPRITE]
    HITBOX_X_OFFSET = 0
    HITBOX_Y_OFFSET = 0

    # [Class constructor]
    def __init__(self, grid_position, surface, hitbox_size):
        '''
        [PARAMETERS]:
        "self"          : reference to the current object.
        "grid_position" : 2-elements tuple which indicates the position of the entity on the grid
        "surface"       : the surface representing the entity on screen
        "hitbox_size"   : 2-elements tuple which indicates the size of the entity's hitbox                 
        '''
        self.grid_position = grid_position

        # The (initial) on-screen position of the entity gets calculated on the basis of the "X_OFFSET"
        # and "Y_OFFSET" constants relative to the "specialized" class, not to the abstract one
        self.screen_position = cmndef.get_tile_related_screen_coords(grid_position,
                                                                     self.__class__.GRID_X_OFFSET,
                                                                     self.__class__.GRID_Y_OFFSET)

        self.surface = surface
        self.hitbox = pygame.Rect(self.screen_position[0] + self.__class__.HITBOX_X_OFFSET,
                                  self.screen_position[1] + self.__class__.HITBOX_Y_OFFSET,
                                  hitbox_size[0], hitbox_size[1])

    # [Method to compute the entity surface at each game loop]
    @abstractmethod
    def compute_surface(self):
        '''
        This is an abstract method, so it will get overridden in
        the specialized classes which inherit from "Entity".
        
        It gets called for every entity at every iteration of
        the game loop, and its purpose is to determine which
        will be the entity's surface which will blitted in
        the next loop.
        '''
        pass    # No implementation

     # [Method to verify if the ]
    def check_collisions(self, colliders_list):
        '''
        [PARAMETERS]:
        "self"           : reference to the current object.
        "colliders_list" : list of entities whose collision with the
                           current object we want to test

        [RETURNS]:
        "True" => if this object collides with any of the colliders in the list
        "False" => if this object does not collide with any of the colliders in the list
        
        At the moment, I've chosen to let this method be NOT
        an abstract method: if the need arises for the specialized
        classes to process 
        '''
        collision_detected = False
        for elem in colliders_list:
            collision_detected = collision_detected or self.hitbox.colliderect(elem.hitbox)
        return collision_detected