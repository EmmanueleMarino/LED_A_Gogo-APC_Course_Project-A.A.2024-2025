'''
[PLAYER SCORER]:
This class represents the object associated with the HUD relative to
a specific player. While the information on the score is stored in
the "Player" object, said information gets used to update the surface
of the associated HUD element at every game loop iteration.
'''

# [IMPORT OF LIBRARIES]
import pygame
import os
from modules.scripts.common_definitions import assets_path

# LEDs offsets (relatively to the HUD graphics)
LED_OFFSETS = [(147,10), (156,14), (160,23), (156,32), (147,36), (138,32), (134,24), (138,14)]

#  /-----------------------------------------------------------------------------------------------------\
# | [N.B.]: I tried to declare "LED_OFFSETS" as a static member of the class, but it wasn't recognized as |
# | "PlayerScorer.LED_OFFSETS" in the "LED_RECTS" declaration... it's a minor issue, but I'll probably    |
# | try to fix it, nonetheless.                                                                           |
#  \-----------------------------------------------------------------------------------------------------/

class PlayerScorer():
    # Static member of the class: each of these surfaces is a digit
    DIGITS_SURFACES = [pygame.image.load(os.path.join(assets_path, f"hud/digits/{i}.png")) for i in range(10)]
    SCREEN_POSITIONS = [(5,35),(455,35),(5,245),(455,245)]    # Screen position of the scorer associated with each
                                                                # player. The HUD does not follow the grid-based logic
                                                                # which is followed by the "Entity" subclasses

    # [PLACEHOLDER] => In the final project, it will be a list of surfaces, each surface corresponding
    # to the HUD graphics relative to the player associated with the current PlayerScorer object
    HUD_GRAPHICS = pygame.image.load(os.path.join(assets_path, "hud/hud_placeholder.png"))

    # 6x6 rects which will be displayed when the corresponding led is turned on on the board
    LED_RECTS = [pygame.Rect(LED_OFFSETS[i][0], LED_OFFSETS[i][1], 8, 8) for i in range(8)]

    # Colours of the rects defined above
    LED_COLOURS = [(81,210,57), (73,211,239), (213,56,37), (240, 134, 58)]  # These four colours repeat, so there's no
                                                                            # need to repeat them in the list, the
                                                                            # "module" operation will be used to
                                                                            # select the current colour for indeces
                                                                            # greater than 3 (i % 4)

    # [CLASS CONSTRUCTOR]
    def __init__(self, player_ref):
        '''
        [PARAMETERS]:
        "self"       : reference to the current object
        "player_ref" : reference to the player associated with the current scorer
        '''
        self.player_ref = player_ref
        self.screen_position = PlayerScorer.SCREEN_POSITIONS[player_ref.player_id - 1]
        self.surface = None
        self.compute_surface()


    # [Method to compute the entity surface at each game loop]
    def compute_surface(self):
        #  /-----------------------------------------------------------------\
        # | The scorer's surface is composed by multiple overlapped surfaces. | 
        # | For now, we'll simply blit the "DIGIT_SURFACES" on top of the     |
        # | placeholder surface                                               |
        #  \-----------------------------------------------------------------/
        # A transparent "base surface" gets created
        scorer_surface =  pygame.Surface((180, 80), pygame.SRCALPHA)

        # The LEDs' colours get drawn on the "base surface"
        for i in range(self.player_ref.active_leds_num):
            pygame.draw.rect(scorer_surface, PlayerScorer.LED_COLOURS[i % 4], PlayerScorer.LED_RECTS[i])

        # The HUD gets blitted on top of the scorer_surface
        scorer_surface.blit(PlayerScorer.HUD_GRAPHICS)

        # Score string
        score_string = str(self.player_ref.score)

        # If the score string is shorter than "6", padding is added
        score_string = "0"*(6 - len(score_string)) + score_string

        for i in range(6):
            scorer_surface.blit(PlayerScorer.DIGITS_SURFACES[int(score_string[i])],(107 + 11*i,56))

        self.surface = scorer_surface