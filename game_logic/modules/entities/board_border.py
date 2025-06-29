'''
[BOARD BORDER]:
This class models the borders of the "pogo board".
This kind of object will be "collidable" with the players
(the board's border will -in fact - prevent the players from
"falling off" of the playing platform).

Such an entity can be:
    1) A "side tile", which is positioned on the side of a tile of the "pogo board"
    2) An "angle block", which is positioned a the intersection of two differently
       angled "side tiles", and connects said tiles in a schema such as the following:

       [ ]--     OR    --[ ]     OR     |        OR        |
        |                 |            [ ]--            --[ ]
'''

# [IMPORTS OF LIBRARIES]
from modules.entities.entity import Entity
from modules.scripts import common_definitions as cmndef
import pygame
import os
from modules.enumerations.border_type import BorderType     # Enumeration for the two different
                                                            # types of board border.

from modules.enumerations.direction import Direction        # Enumeration for the four different
                                                            # positionings of the tile.


class BoardBorder(Entity):
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
    HITBOX_X_OFFSET = 0
    HITBOX_Y_OFFSET = 0

    #  /-------\
    # | METHODS |
    #  \-------/
    # [Class constructor]
    def __init__(self, grid_position, border_type, positioning):
        '''
        [PARAMETERS]:
        "self"        : reference to the current object.
        "border_type" : identifies whether the object is a "side tile" or an
                        "angle block" according to the definitions given at
                        the top of this module.

        "positioning" : it can be either a single element of the "Directions"
                        enumeration [UP, RIGHT, DOWN, LEFT] - in case the
                        border_type is "side tile" - or a 2-elements tuple
                        of directions, in case the border type is "angle block"

                        (UP, LEFT); (DOWN, LEFT); (UP, RIGHT); (DOWN, RIGHT)

        The here undocumented parameters are
        documented in the upper "Entity" class.
        '''

        # Initialization of the class-specific members
        self.border_type = border_type
        self.positioning = positioning

        # The constructor of the upper class gets called
        super().__init__(grid_position, surface=self.compute_surface(), hitbox_size=self.compute_hitbox_size())

        # The screen position gets updated on the basis of what kind of "boarder tile"
        # the current object represents => [I THINK THIS IS KIND OF A "WORKAROUND", BUT IT WILL PROBABLY
        # BE CONFINED TO THIS CLASS ONLY] => If there's enough time on our hands, another refactoring
        # to achieve a cleaner solution could be a good idea.
        screen_position_offset = self.compute_screen_position_offset()

        self.screen_position = (self.screen_position[0] + screen_position_offset[0],
                                self.screen_position[1] + screen_position_offset[1])

        # The same offsets get used to update the hitbox's screen position
        self.hitbox.x += screen_position_offset[0]
        self.hitbox.y += screen_position_offset[1]


    # [Method to compute the entity surface at each game loop]
    def compute_surface(self):
        '''This function might be expanded if we decide to implement the "player area rotation"
           feature - in which each 4x4 submatrix (those are positioned in the four corners of the
           "pogo board") gets dedicated to a single player, so they can achieve points just by
           closing rectangles in said area; and the player assigned to each submatrix changes every
           set amount of time according to a "rotational" scheme.
           
           In that case, the computed surface will be recalculated at every game loop iteration,
           on the basis of the value of an attribute of the "BoardBorder" object which will indicate
           the current player associated with that corner of the board.
           
           [AS OF NOW, THIS FUNCTION GETS CALLED SOLELY IN THE CONSTRUCTOR - GIVEN THAT
            THE SURFACE OF THE OBJECT GETS DETERMINED JUST ONCE WHEN THE OBJECT GETS INSTANTIATED]
        '''
        if(self.border_type == BorderType.SIDE_TILE):
            surface = pygame.image.load(os.path.join(cmndef.assets_path,"tiles/border_tiles/grey_side.png"))
            # Evaluate whether the surface has to be rotated or not
            if(self.positioning == Direction.UP or self.positioning == Direction.DOWN):
                surface = pygame.transform.rotate(surface, 90)
            return surface
        elif(self.border_type == BorderType.ANGLE_BLOCK):
            return pygame.image.load(os.path.join(cmndef.assets_path,"tiles/border_tiles/grey_angle.png"))


    # [Method to compute the hitbox's size accordingly to the BorderType]
    def compute_hitbox_size(self):
        if(self.border_type == BorderType.SIDE_TILE):
            if(self.positioning == Direction.LEFT or self.positioning == Direction.RIGHT):
                return((12,24))
            else:
                return((24,12))
        elif(self.border_type == BorderType.ANGLE_BLOCK):
            return((12,12)) 
    

    # [Method to compute the screen position offset accordingly to the BorderType and the orientation]
    def compute_screen_position_offset(self):
        if(self.border_type == BorderType.SIDE_TILE):
            if(self.positioning == Direction.UP):
                return((0,12))
            if(self.positioning == Direction.RIGHT):
                return((0,0))
            if(self.positioning == Direction.DOWN):
                return((0,0))
            if(self.positioning == Direction.LEFT):
                return((12,0))
        elif(self.border_type == BorderType.ANGLE_BLOCK):
            if(self.positioning == (Direction.UP, Direction.LEFT)):
                return((12,12))
            if(self.positioning == (Direction.UP, Direction.RIGHT)):
                return((0, 12))
            if(self.positioning == (Direction.DOWN, Direction.LEFT)):
                return((12,0))
            if(self.positioning == (Direction.DOWN, Direction.RIGHT)):
                return((0,0))