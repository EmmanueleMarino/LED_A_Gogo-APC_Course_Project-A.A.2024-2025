# [IMPORT OF LIBRARIES]
import pygame
from scripts import common_definitions as cmndef

# Various functions to resize the screen after the press of a button


# Toggle fullscreen mode
def toggle_fullscreen(fullscreen,scaled,game_surface,screen):
    '''
    [PARAMETERS]:
    "fullscreen": boolean variable which indicates whether the game is currently in the "pygame.FULLSCREEN" mode or not
    "scaled": boolean variable which indicates whether the game is currently in the "pygame.SCALED" mode or not
    "game_surface": the surface on which every game graphics gets drawn
    "screen": the "screen" surface which represents the Pygame application window

    [RETURN]:
    This function returns a modified version of the input parameters, minus "scaled" - which is left untouched
    '''
    if not fullscreen:
        game_surface = pygame.transform.scale(game_surface, cmndef.fullscreen_game_size)
        screen = pygame.display.set_mode(cmndef.fullscreen_game_size,pygame.FULLSCREEN)
    else:
        game_surface = pygame.transform.scale(game_surface, cmndef.base_game_size)
        if scaled:
            screen = pygame.display.set_mode(cmndef.base_game_size, pygame.SCALED)
        else:
            screen = pygame.display.set_mode(cmndef.base_game_size)
    fullscreen = not fullscreen

    return fullscreen, game_surface, screen


# Toggle scaled (2x) mode
def toggle_scaled_2x(fullscreen,scaled,game_surface,screen):
    '''
    [PARAMETERS]:
    "fullscreen": boolean variable which indicates whether the game is currently in the "pygame.FULLSCREEN" mode or not
    "scaled": boolean variable which indicates whether the game is currently in the "pygame.SCALED" mode or not
    "game_surface": the surface on which every game graphics gets drawn
    "screen": the "screen" surface which represents the Pygame application window

    [RETURN]:
    This function returns a modified version of the input parameters - minus "fullscreen" - which is left untouched
    '''
    if not fullscreen:
        if not scaled:
            screen = pygame.display.set_mode(cmndef.base_game_size,pygame.SCALED) 
        else:
            screen = pygame.display.set_mode(cmndef.base_game_size)
        scaled = not scaled
    
    return scaled, game_surface, screen