'''
[PLAYER CLASS]:
This class models the player.
There can be up to 4 different players on the screen.
'''

# [IMPORTS OF LIBRARIES]
from modules.entities.entity import Entity
from modules.scripts import common_definitions as cmndef
import pygame
import os
from modules.enumerations.direction import Direction                                # Enumeration for the four directions
from modules.player_scorer import PlayerScorer
from modules.scripts.serial_communication import serial_communication as sercom     # For serial communication
import queue
import threading


class Player(Entity):
    #  /----------------\
    # | STATIC CONSTANTS |
    #  \----------------/
    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE
    #  SPRITE RELATIVELY TO THE GRID]
    GRID_X_OFFSET = 2
    GRID_Y_OFFSET = -30

    # [OFFSETS ON THE X AND Y AXIS
    #  FOR THE POSITIONING OF THE HITBOX
    #  RELATIVELY TO THE ENTITY SPRITE]
    HITBOX_X_OFFSET = 7
    HITBOX_Y_OFFSET = 31

    # [ANIMATION SLOWDOWN CONSTANT]
    ANIMATION_SLOWDOWN_CONSTANT = 8         # It expresses the number of game loops in
                                            # which the same animation frame gets repeated

    # [ANIMATION FRAMES SEQUENCE]
    ANIMATION_FRAMES_SEQUENCE = [0,1,2,1]   # Succession of indexes which model the order in
                                            # which the animation frames will be played

    # [SCORE-THRESHOLDS]
    SCORE_THRESHOLDS = [50, 150, 300, 500,       # When the player's score exceeds a threshold,
                       750, 1100, 1500, 1950]   # the corresponding LED gets turned on.

    #  /-------\
    # | METHODS |
    #  \-------/
    # [Class constructor]
    def __init__(self, grid_position, player_id, controller_serial_port):
        '''
        [PARAMETERS]:
        "self"      : reference to the current object.
        "player_id" : it can be "1", "2", "3" or "4"
        
        The here undocumented parameters are
        documented in the upper "Entity" class.
        '''
        # Initialization of the class-specific members
        self.score = 0              # The current score held by the player
        self.player_id = player_id
        self.current_anim_idx = 0   # This attribute specifies which animation frame 
                                    # in the "ANIMATION_FRAMES_SEQUENCE" is being played
                                    # in the current game loop iteration.

        self.current_anim_slowdown_idx = 0  # This attribute specifies how many game loops
                                            # has the current animation frame been played for

        self.animation_matrix = self.compute_animation_matrix(player_id)
        self.direction = Direction.DOWN     # The current direction of the player

        # Number of "Active LEDs" - this is the number of LEDs which have
        # been turned on by increasing the score during the game session. 
        self.active_leds_num = 0            # Initially, no LEDs are turned on

        # Instantiation of the scorer (the reference to the current "Player"
        # object gets passed as a parameter of the "PlayerScorer" constructor)
        self.scorer = PlayerScorer(self)

        #  /---------------------------------------------------------------\
        # | [N.B.] - A number - and NOT a mask - is used to indicate the    |
        # | active LEDs because the LEDs' turning on is "cumulative", which |
        # | means that if a LED in the sequence of LEDs has been turned on, |
        # | all of the previous LEDs in the sequence will have also been    |
        # | previously turned on.                                           |
        #  \---------------------------------------------------------------/ 

        # Object of the "Serial" class which gets instantiated when
        # the Python program opens a COM port towards a BT module
        self.controller_serial_port = controller_serial_port

        # The player does not initially hold a "power up"
        self.has_power_up = False
        self.power_up_initial_validity = 15
        self.power_up_validity = self.power_up_initial_validity
        self.power_up_acquisition_time = 0  # Initially 0, it gets updated when the power up gets acquired
        
        # State of the player with regards to the "power up"
        self.is_powered_up = False
        self.initial_power_up_duration = 5
        self.power_up_duration = self.initial_power_up_duration
        self.power_up_activation_time = 0   # Initially 0, it gets updated when the power activates a power up

        # Queues of messages coming from the board
        self.gyro_msgs = queue.Queue(maxsize=64)
        self.speed_msg = queue.Queue(maxsize=1)

        # [N.B.]: I think having a different "receiver_thread" for each player might be too much, so it will be probabily all
        # handled in a single thread... for now, given that each player has got a "receiver_stop_event" which has to used to
        # terminate the reading loop before closing the virtual serial port
        self.receiver_stop_event = threading.Event()

        # Reading thread
        self.receiver_thread = sercom.start_serial_receiver_thread(self.controller_serial_port, self.gyro_msgs, self.speed_msg, self.receiver_stop_event) if self.controller_serial_port != None else None

        # The constructor of the upper class gets called
        super().__init__(grid_position, surface=self.animation_matrix[Direction.UP.value][0], hitbox_size=(22,22))


    # [Method to compute the matrix whose rows are vectors
    #  containing the surfaces which represent the frames
    #  of animation in a specific direction].
    def compute_animation_matrix(self,player_id):
        '''
        [PARAMETERS]:
        "player_id"        : it will be used to select the animation frames which
                             are correctly related to the player with said ID

        [RETURN]:
        "animation_matrix" : each row of said matrix contains the three surfaces
                             associated with the animation frames in a specific direction
        '''
        # [ROW 0] => UP
        up_direction = [pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/back_animation/back_1.png")),
                        pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/back_animation/back_2.png")),
                        pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/back_animation/back_3.png"))]

        # [ROW 1] => RIGHT
        right_direction = [pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/right_side_animation/right_side_1.png")),
                           pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/right_side_animation/right_side_2.png")),
                           pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/right_side_animation/right_side_3.png"))]

        # [ROW 2] => DOWN
        down_direction = [pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/frontal_animation/frontal_1.png")),
                          pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/frontal_animation/frontal_2.png")),
                          pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/frontal_animation/frontal_3.png"))]
        
        # [ROW 3] => LEFT
        left_direction = [pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/left_side_animation/left_side_1.png")),
                          pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/left_side_animation/left_side_2.png")),
                          pygame.image.load(os.path.join(cmndef.assets_path,f"players/player_{player_id}/left_side_animation/left_side_3.png"))]
        
        return [up_direction, right_direction, down_direction, left_direction]


    # [Method to compute the entity surface at each game loop]
    def compute_surface(self):
        # The surface gets computed before the update
        self.surface = self.animation_matrix[self.direction.value][Player.ANIMATION_FRAMES_SEQUENCE[self.current_anim_idx]]

        # The player animation only gets changed every "ANIMATION_SLOWDOWN_CONSTANT/60"th of a second
        if(self.current_anim_slowdown_idx == Player.ANIMATION_SLOWDOWN_CONSTANT):
            self.current_anim_slowdown_idx = 0
            self.current_anim_idx = (self.current_anim_idx + 1) % len(Player.ANIMATION_FRAMES_SEQUENCE)

        # At each game loop iteration, the slowdown index gets increased
        self.current_anim_slowdown_idx += 1


    # [Method to change the player direction]
    def change_direction(self, direction):
        # It's a simple method, but I deemed it cleaner
        # to set the direction via a method, rather than
        # accessing the object's attribute directly
        self.direction = direction

    
    # [Method to update the position of the player based on
    #  what directional key is being pressed (the function
    #  will be modified accordingly when the angular velocity
    #  readings are used to move a player)]
    def update_position(self, movement_tuple):
        '''
        [PARAMETERS]:
        "self"           : reference to the current object
        "movement_tuple" : 2-elements tuple which indicates the
                           offset - in terms of pixels - that has
                           to be summed to the current player's
                           screen position
        '''
        self.screen_position = (self.screen_position[0] + movement_tuple[0],
                                self.screen_position[1] + movement_tuple[1])

        # The hitbox has to move together with the player's sprite
        self.hitbox.x = self.screen_position[0] + Player.HITBOX_X_OFFSET
        self.hitbox.y = self.screen_position[1] + Player.HITBOX_Y_OFFSET


    # [Method to update the score and the active LEDs number]
    def update_score_and_leds(self, points_to_sum):
        '''
        [PARAMETERS]
        "points_to_sum" : amount of points to sum to the score.
        '''
        self.score += points_to_sum

        # The maximum score is "1950", so if the score exceeds this threshold,
        # the score gets capped at 1950, and the "active_leds_num" gets capped
        # to "8".
        if(self.score >= 1950):
            self.score = 1950
            self.active_leds_num = 8
            return

        # If the next threshold is exceeded, the next LED gets turned on
        if(self.score >= Player.SCORE_THRESHOLDS[self.active_leds_num]):
            self.active_leds_num += 1

            # The corresponding LED gets turned on
            if self.controller_serial_port != None:
                sercom.turn_led_on(self.active_leds_num, self.controller_serial_port)

            # [FOR DEBUGGING PURPOSES]
            #print(f"Player {self.player_id} has exceeded threshold n°{self.active_leds_num}")
