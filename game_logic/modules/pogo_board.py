'''
[POGO BOARD]:
This class models the whole pogo board, which includes both the "pogo tiles"
and the borders of the board. By implementing this class, all of the "pogo board"
entities will be instantiated - in the main program - by simply instantiating a
"PogoBoard" object (this will also allow for boards of varying dimensions, although
we'll probably stick to the "8x8" board as initially intended).

 /--------------------------------------------------------------------------\
| [N.B.] I didn't know where to put this class, if in the "entities" package |
| or if creating a whole new package was desirable... we'll probably move it |
| if we deem it a more elegant disposition.                                  |
 \--------------------------------------------------------------------------/

'''


# [IMPORT OF LIBRARIES]
from modules.entities.pogo_tile import PogoTile
from modules.entities.board_border import BoardBorder
from modules.enumerations.direction import Direction
from modules.enumerations.border_type import BorderType


class PogoBoard():
    def __init__(self, board_dimensions, grid_position):
        '''
        [PARAMETERS]:
        "self"             : reference to the current object
        "board_dimensions" : 2-elements tuple which represents how many tiles the board
                             should extend for on the "X" and "Y" axis of the 26x15 of
                             24x24 tiles in which the game surface is (virtually) divided
                            
        "grid_position"    : 2-elements tuple which indicates the position of the top-left
                             cell of the board on the previously described 26x15 grid 
        '''
        # The dimensions of the board and the grid position are stored as
        # attributes of the current "PogoBoard" object
        self.board_dimensions = board_dimensions
        self.grid_position = grid_position

        # Instantiating the "pogo tiles" and the "board borders"
        self.pogo_tiles = self.instantiate_pogo_tiles()
        self.board_borders = self.instantiate_board_borders()

        '''
        Evaluate whether having a separate "status_matrix" - such a matrix is a "board_dimensions[0] X board_dimensions[1]"
        matrix whose every element indicates the "tile acquisition" of each tile by a certain player among the four.
        '''


    # [Private method to instantiate the matrix of pogo tiles]
    def instantiate_pogo_tiles(self):
        pogo_tiles = []

        for i in range(self.board_dimensions[0]):
            row = []
            for j in range(self.board_dimensions[1]):
                row.append(PogoTile((self.grid_position[0] + i, self.grid_position[1] + j)))
            pogo_tiles.append(row)
        
        return pogo_tiles


    # [Private methond to instantiate the borders of the board]
    def instantiate_board_borders(self):
        board_borders = {}

        # The "angles" field will be a list of BoardBorder
        # objects of the "ANGLE_BLOCK" type
        angle_blocks = []
        angle_blocks.append(BoardBorder((self.grid_position[0]-1,self.grid_position[1]-1), BorderType.ANGLE_BLOCK, (Direction.UP,Direction.LEFT)))
        angle_blocks.append(BoardBorder((self.grid_position[0]+self.board_dimensions[0],self.grid_position[1]-1), BorderType.ANGLE_BLOCK, (Direction.UP,Direction.RIGHT)))
        angle_blocks.append(BoardBorder((self.grid_position[0]+self.board_dimensions[0],self.grid_position[1]+self.board_dimensions[1]), BorderType.ANGLE_BLOCK, (Direction.DOWN,Direction.RIGHT)))
        angle_blocks.append(BoardBorder((self.grid_position[0]-1,self.grid_position[1]+self.board_dimensions[1]), BorderType.ANGLE_BLOCK, (Direction.DOWN,Direction.LEFT)))

        # The "sides" field will be a matrix of BoardBorder
        # objects of the "SIDE_TILE" type, where each row
        # will represent a different orientation of the
        # tile objects it contains
        side_tiles = []

        # [ROW 0] = "UP" -> Upper border
        upper_border = []
        for i in range(self.board_dimensions[0]):
            upper_border.append(BoardBorder((self.grid_position[0]+i,self.grid_position[1]-1), BorderType.SIDE_TILE, Direction.UP))
        side_tiles.append(upper_border)

        # [ROW 1] = "RIGHT" -> Right border
        right_border = []
        for i in range(self.board_dimensions[1]):
            right_border.append(BoardBorder((self.grid_position[0]+self.board_dimensions[0],self.grid_position[1]+i), BorderType.SIDE_TILE, Direction.RIGHT))
        side_tiles.append(right_border)

        # [ROW 2] = "DOWN" -> Lower border
        lower_border = []
        for i in range(8):
            lower_border.append(BoardBorder((self.grid_position[0]+i,self.grid_position[1]+self.board_dimensions[1]), BorderType.SIDE_TILE, Direction.DOWN))
        side_tiles.append(lower_border)

        # [ROW 3] = "LEFT" -> Left border
        left_border = []
        for i in range(8):
            left_border.append(BoardBorder((self.grid_position[0]-1,self.grid_position[1]+i), BorderType.SIDE_TILE, Direction.LEFT))
        side_tiles.append(left_border)

        board_borders['angle_blocks'] = angle_blocks
        board_borders['side_tiles'] = side_tiles

        return board_borders


    # [Method to compute the surfaces for all the tiles in the board]
    def compute_surfaces(self):
        for tile_row in self.pogo_tiles:
            for tile in tile_row:
                tile.compute_surface()