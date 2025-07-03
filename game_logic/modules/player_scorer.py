'''
[PLAYER SCORER]:
This class represents the object associated with the HUD relative to
a specific player. While the information on the score is stored in
the "Player" object, said information gets used to update the surface
of the associated HUD element at every game loop iteration.

 /----------------\
| CODE TO REFACTOR |
 \----------------/
 This class presents a decent amount of workarounds in its methods...
 That is caused by the presence of the "active_leds_num" member of the
 Player class, which has maximum value "8" (said value causes a number
 of "index out of range" errors if not handled separately, given that
 it is often used to access lists which have "7" as the maximum index).

 It would be nice to keep this in mind and make the code cleaner. 
'''

# [IMPORT OF LIBRARIES]
import pygame
import os
from modules.scripts.common_definitions import assets_path
import copy     # Every "score_rect" starts as a "deepcopy" of
                # the static "SCORE_RECT" member of the class

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

    # (74x5) rect which shows the score progression relatively to the current score
    # threshold to exceed (in order to turn on the next LED on the "LED wheel")
    SCORE_RECT = pygame.Rect(50, 40, 74, 5)

    # Colours of the rects defined above
    LED_COLOURS = [(81,210,57), (73,211,239), (213,56,37), (240, 134, 58)]  # These four colours repeat, so there's no
                                                                            # need to repeat them in the list, the
                                                                            # "module" operation will be used to
                                                                            # select the current colour for indeces
                                                                            # greater than 3 (i % 4)
    
    # Surfaces of labels representing the players'IDs and the "next LED to turn on"
    PLAYER_LABELS = [pygame.image.load(os.path.join(assets_path, f"hud/player_labels/p{i+1}_label.png")) for i in range(4)]
    LED_LABELS = [pygame.image.load(os.path.join(assets_path, f"hud/led_labels/led_{i+1}_label.png")) for i in range(8)]    

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

        # The "score rect" gets drawn on the "base surface",
        # and its X-dimension gets made proportional to
        # the difference between the currently reached
        # threshold and the next
        score_rect = copy.deepcopy(PlayerScorer.SCORE_RECT)
    
        # "score_interval" is the difference between the current
        # threshold to exceed and the last threshold that was exceeded
        score_interval = 0

        if self.player_ref.active_leds_num != 0:
            # If the LED number has reached the maximum value (8), the interval between the
            # previously exceeded threshold and the one to currently reach maintains the
            # initialization value "0" (there's no "next threshold" to exceed, the game session is over).
            if not self.player_ref.active_leds_num == 8:
                score_interval = (self.player_ref.__class__.SCORE_THRESHOLDS[self.player_ref.active_leds_num] -
                                  self.player_ref.__class__.SCORE_THRESHOLDS[self.player_ref.active_leds_num - 1])
        else:
            score_interval = 50

        # The previous threshold also has to be retrieved to compute
        # the width of the "score_rect" on the "X" axis
        previous_threshold = self.player_ref.__class__.SCORE_THRESHOLDS[self.player_ref.active_leds_num - 1] if self.player_ref.active_leds_num != 0 else 0

        # The width of the score rect is calculated as a portion of the "74px" maximum width
        # (to be precise, as the currently reached portion ("[current_score - previous_threshold] / score_interval")
        # of the score interval)
        score_rect.width = ((self.player_ref.score - previous_threshold) / score_interval) * 74 if self.player_ref.active_leds_num != 8 else 74

        '''
        # [FOR DEBUGGING PURPOSES]
        if self.player_ref.player_id == 1:
            print(self.player_ref.score - previous_threshold)
        '''

        # The "score_rect" gets drawn on the "scorer_surface"
        #  /-------------------------------------------------------------------------------------------------------\
        # | THIS SOLUTION IS A BIT OF A WORKAROUND - by executing only the "if" branch, when the score reached its  |
        # | maximum value, the displayed colour was the one with index "0". The desired effect was - instead - that |
        # | when the maximum value is reached, the displayed colour is still the one with index "3".                |
        #  \-------------------------------------------------------------------------------------------------------/
        if self.player_ref.active_leds_num != 8:
            pygame.draw.rect(scorer_surface, PlayerScorer.LED_COLOURS[self.player_ref.active_leds_num % 4], score_rect)
        else:
            pygame.draw.rect(scorer_surface, PlayerScorer.LED_COLOURS[3], score_rect)

        # The LEDs' colours get drawn on the "base surface"
        for i in range(self.player_ref.active_leds_num):
            pygame.draw.rect(scorer_surface, PlayerScorer.LED_COLOURS[i % 4], PlayerScorer.LED_RECTS[i])

        # The HUD gets blitted on top of the scorer_surface
        scorer_surface.blit(PlayerScorer.HUD_GRAPHICS)

        # The player's label gets blitted on top of the scorer_surface
        scorer_surface.blit(PlayerScorer.PLAYER_LABELS[self.player_ref.player_id - 1], (53,5))

        # The "target LED" label gets blitted on top of the scorer_surface
        scorer_surface.blit(PlayerScorer.LED_LABELS[self.player_ref.active_leds_num], (70,32))

        # Score string
        score_string = str(self.player_ref.score)

        # If the score string is shorter than "6", padding is added
        score_string = "0"*(6 - len(score_string)) + score_string

        for i in range(6):
            scorer_surface.blit(PlayerScorer.DIGITS_SURFACES[int(score_string[i])],(107 + 11*i,56))

        self.surface = scorer_surface