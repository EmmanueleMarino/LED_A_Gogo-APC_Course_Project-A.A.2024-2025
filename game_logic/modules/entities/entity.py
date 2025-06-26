'''
[GENERIC ENTITY]:
This class models the generic "entity" which can get positioned
on the 26x15 grid in which the playing surface is divided.
'''

# [IMPORT OF LIBRARIES]
from modules.scripts import common_definitions as cmndef
from abc import ABC, abstractmethod     # "Entity" is an abstract class, so it has to
                                        # inherit from the "ABC" class.

class Entity(ABC):
    #  /----------------\
    # | STATIC CONSTANTS |
    #  \----------------/
    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE
    #  SPRITE RELATIVELY TO THE GRID]
    X_OFFSET = 0
    Y_OFFSET = 0

    # [Class constructor]
    def __init__(self, grid_position, surface):
        '''
        [PARAMETERS]:
        "self"          : reference to the current object.
        "grid_position" : 2-elements tuple which indicates the position of the entity on the grid
        "surface"       : the surface representing the entity on screen                  
        '''
        self.grid_position = grid_position

        # The (initial) on-screen position of the entity gets calculated on the basis of the "X_OFFSET"
        # and "Y_OFFSET" constants relative to the "specialized" class, not to the abstract one
        self.screen_position = cmndef.get_tile_related_screen_coords(grid_position,
                                                                     self.__class__.X_OFFSET,
                                                                     self.__class__.Y_OFFSET)

        self.surface = surface

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