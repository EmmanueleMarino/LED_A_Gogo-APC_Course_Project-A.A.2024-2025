import pygame
import os

from modules.scripts import common_definitions as cmndef
from modules.entities.power_up import PowerUp
from modules.pogo_board import PogoBoard
from modules.enumerations.direction import Direction
from modules.enumerations.game_phase import GamePhase
from modules.scripts.find_smallest_rectangle import find_smallest_rectangle
from modules.scripts.serial_communication import serial_communication as sercom
from modules.scripts.serial_communication import spawn_players as spwpl
import random
import threading


screen = pygame.display.set_mode(cmndef.base_game_size)

# [GAME PHASE]
# 0 -> Player spawning phase
# 1 -> Game session
game_phase = GamePhase.PLAYER_SPAWNING  # Before the game session can start, the players have
                                        # to spawn first (which happens by connecting with the
                                        # several STM32F3DISCOVERY boards).

# The "game_surface" is the surface on which all of the game graphics will be
# rendered on. It gets used in place of the "screen" Surface object, for it
# will be properly resized according to the window size at every game loop cycle.
game_surface = pygame.Surface(cmndef.base_game_size)

# The "playing_surface is the surface underneath the player surface (and other
# "dynamic" surfaces - that is, surfaces upon which several animation frames
# will be drawn).
playing_surface = pygame.Surface(cmndef.base_game_size)

#  /-----------------------------\
# | "WAITING FOR PLAYERS" SURFACE |
#  \-----------------------------/
wait_players_surface = pygame.image.load(os.path.join(cmndef.assets_path, "hud/waiting_for_players_placeholder.png")).convert_alpha()

#  /----------------------------------------------\
# | SURFACES OF THE VARIOUS GAME SCENARIO ELEMENTS |
#  \----------------------------------------------/
underneath_the_board = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/underneath_the_board.png"))
background_surface = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/background.png"))
board_shadows = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/board_shadows.png")).convert_alpha()
global_shadow = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/global_shadow.png")).convert_alpha()
board_upper_light = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/board_upper_light.png")).convert_alpha()
shadows_under_the_board = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/shadows_under_the_board.png")).convert_alpha()
lights_and_ambience = pygame.image.load(os.path.join(cmndef.assets_path, "game_scenario/lights_and_ambience.png")).convert_alpha()

# Apparently, when the "game_surface" gets
# resized, the reference to the resized
# surface has to be assigned to yet
# another surface
fullscreen_surface = None

# The players get instantiated
players = []    # Initially, there are no players instantiated:
                # each player will get spawned if a board gets
                # connected to the game

# Generating a "stopping event" for the player spawning thread
player_spawning_stop_event = threading.Event()

# Starting the players spawning thread
player_spawning_thread = spwpl.start_players_detecting_thread(players, player_spawning_stop_event)

# "Clock" object to ensure the game loop gets played every 1/60th of a second
# (The game gets capped at 60FPS)
clock = pygame.time.Clock()

pygame.display.set_caption("LED-A-Gogo (APC Project - A.A. 2024/2025)")

icon_surface = pygame.image.load(os.path.join(cmndef.assets_path, "logo_redux.png")).convert_alpha()
pygame.display.set_icon(icon_surface)

# An "8x8" pogo board gets instantiated
# starting from the "(9,5)" tile on the
# 26x15 grid
pogo_board = PogoBoard((8,8), (9,5))

# Game loop running state
running = True

# Fullscreen state
fullscreen = False

# Scaled state
scaled = False

# Game termination state
game_termination = False

# Game phase change
phase_change = False

#  /-----------------------------------------\
# | SURFACES FOR THE HUD ELEMENTS WHICH GET   |
# | SHOWN WHEN THE GAME SESSION IS TERMINATED |
#  \-----------------------------------------/
game_over_surface = pygame.image.load(os.path.join(cmndef.assets_path, "hud/game_over/game_over.png")).convert_alpha()
game_over_shadow = pygame.image.load(os.path.join(cmndef.assets_path, "hud/game_over/shadows/game_over.png")).convert_alpha()
winning_player_surface = [pygame.image.load(os.path.join(cmndef.assets_path, f"hud/game_over/p{i+1}_won.png")).convert_alpha() for i in range(4)]
winning_player_shadows = [pygame.image.load(os.path.join(cmndef.assets_path, f"hud/game_over/shadows/p{i+1}_won.png")).convert_alpha() for i in range(4)]


#  /----------------------------------------------------------------\
# | SURFACE FOR THE "TIME LEFT" HUD ELEMENT WITH THE RELATIVE SHADOW |
#  \----------------------------------------------------------------/
time_left_surface = pygame.image.load(os.path.join(cmndef.assets_path, "hud/time_left.png")).convert_alpha()
time_left_shadow = pygame.image.load(os.path.join(cmndef.assets_path, "hud/time_left_shadow.png")).convert_alpha()


# This will get used to update the timer
start_time = pygame.time.get_ticks()

# The timer surface is - initially - transparent
timer_surface =  pygame.Surface((120, 40), pygame.SRCALPHA)

# List of "PowerUp" objects
# which are currently present
# on the map
power_ups = []

# Second in which the most
# recent power up was appended
# to the list
most_recent_power_up_sec = 0

# These are the objects with
# which every player will collide
global_colliders = []
global_colliders += pogo_board.board_borders['side_tiles'][Direction.UP.value]
global_colliders += pogo_board.board_borders['side_tiles'][Direction.RIGHT.value]
global_colliders += pogo_board.board_borders['side_tiles'][Direction.DOWN.value]
global_colliders += pogo_board.board_borders['side_tiles'][Direction.LEFT.value]

#  /---------\
# | GAME LOOP |
#  \---------/
while running:
    #  /------------------------------------\
    # | VARIOUS CHECKS WHICH HAVE TO BE DONE |
    # | FOR STARTING THE PROPER GAME PHASE   |
    #  \------------------------------------/
    if game_phase == GamePhase.PLAYER_SPAWNING:
        # As soon as all the players have
        # spawned, the game starts        
        if len(players) == spwpl.MAX_PLAYERS_NUM:
            phase_change = True

        # If the phase has changed, prepare for the
        # next game phase by terminating and joining 
        # the player spawning thread 
        if phase_change:
            for player in players:
                other_players = [p for p in players if p != player] if len(players) > 1 else []
                player.blocking_colliders = global_colliders + other_players
            player_spawning_stop_event.set()
            player_spawning_thread.join()
            game_phase = GamePhase.GAME_SESSION

    # Rendering of the game scenario backgrond
    playing_surface.blit(background_surface,(0,0))

    # Rendering the shadows underneath the board
    playing_surface.blit(shadows_under_the_board,(0,0))

    # Rendering of the "underneath part" of the board
    playing_surface.blit(underneath_the_board,(0,0))

    # Rendering of the "pogo" tiles matrix
    for tile_row in pogo_board.pogo_tiles:
        for tile in tile_row:
            playing_surface.blit(tile.surface, tile.screen_position)
            #pygame.draw.rect(playing_surface, (255,0,0), tile.hitbox) # -> [FOR DEBUGGING PURPOSES]

    # [Rendering of the "pogo board" border]
    # Rendering of the side tiles
    for tile_row in pogo_board.board_borders['side_tiles']:
        for side_tile in tile_row:
            playing_surface.blit(side_tile.surface, side_tile.screen_position)
            #pygame.draw.rect(playing_surface, (255,0,0), side_tile.hitbox) # -> [FOR DEBUGGING PURPOSES]

    # Rendering of the angle blocks
    for angle_block in pogo_board.board_borders['angle_blocks']:
        playing_surface.blit(angle_block.surface, angle_block.screen_position)
        
    # Rendering of the board shadows
    playing_surface.blit(board_shadows,(0,0))

    # Rendering the board's upper light
    playing_surface.blit(board_upper_light,(0,0))

    # The playing surface gets blitted on the
    # global game surface.
    game_surface.blit(playing_surface,(0,0))

    # Event detection in the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detection of a single key pressing 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                if(fullscreen):
                    if(scaled):
                        screen = pygame.display.set_mode(cmndef.base_game_size,pygame.SCALED)
                    else:
                        screen = pygame.display.set_mode(cmndef.base_game_size)
                else:
                    screen = pygame.display.set_mode(cmndef.fullscreen_game_size,pygame.FULLSCREEN)
                fullscreen = not fullscreen
                #fullscreen, game_surface, screen = scrsz.toggle_fullscreen(fullscreen,scaled,game_surface,screen)

            elif event.key == pygame.K_F10:
                if(not fullscreen):
                    if(scaled):
                        screen = pygame.display.set_mode(cmndef.base_game_size) 
                    else:
                        screen = pygame.display.set_mode(cmndef.base_game_size,pygame.SCALED)
                    scaled = not scaled
                #scaled, game_surface, screen = scrsz.toggle_scaled_2x(fullscreen, scaled, game_surface, screen)


    #  /------------------------------------------------------\
    # | PLAYER CONTROL SYSTEM (MOVEMENT, POWER UP, COLLISIONS) |
    #  \------------------------------------------------------/
    # It's only active during the "game session" phase
    if game_phase == GamePhase.GAME_SESSION:
        #  /------------------------\
        # | POWER UP/SPEED UP SYSTEM |
        #  \------------------------/
        for player in players:
            if player.has_power_up:
                # If the player has pressed the USER BUTTON
                # (a "HspeedPgo" message has arrived), the
                # power up gets used
                if(player.speed_msg[0] != None):
                    player.speed_msg[0] = None
                    player.has_power_up = False    # The power up has been consumed
                    player.is_powered_up = True    # The player is now "powered up"
                    player.power_up_duration = player.initial_power_up_duration
                    player.power_up_activation_time = elapsed_time_sec


        #  /---------------\
        # | MOVEMENT SYSTEM |
        #  \---------------/
        if(not game_termination):
            for player in players:
                player.last_position_update = player.gyro_buffer
                if not player.is_powered_up:
                    player.last_position_update = (player.last_position_update[0]*7.5, - player.last_position_update[1]*7.5)
                else:
                    player.last_position_update = (player.last_position_update[0]*15, - player.last_position_update[1]*15)
                player.change_direction(cmndef.determine_direction(player.last_position_update))
                player.update_position(player.last_position_update)


        #  /----------------\
        # | COLLISION SYSTEM |
        #  \----------------/
        # If the movement has caused the current player to collide,
        # the position update gets reverted before the actual blitting.
        # By doing so, the player's hitbox won't get stuck into other
        # player's (or entity's) hitboxes.
        for player in players:            
            # [CHECK COLLISIONS]
            if(player.check_collisions(player.blocking_colliders)):
                # If a player collides with at least one
                # collider, its latest movement gets "reverted"
                player.update_position((player.last_position_update[0] * -1,
                                        player.last_position_update[1] * -1))

    #  /----------------------------------------------------------------\
    # | CHECK IF THE "CHANGE TILE ACQUISITION" EVENT HAS TO BE TRIGGERED |
    #  \----------------------------------------------------------------/
    for player in players:
        for i in range(len(pogo_board.pogo_tiles)):
            for j in range(len(pogo_board.pogo_tiles[0])):
                # [If the player collides with the tile's hitbox]
                if(player.check_collisions([pogo_board.pogo_tiles[i][j]])):
                    # Change the "player_id" for the tile
                    pogo_board.pogo_tiles[i][j].change_acquisition(player.player_id)

                    # Update the status of the board: the "i,j" element of the "player_id - 1" matrix
                    # of the status will be set to "1", the same element of the two remaining matrices
                    # will be set to "0"
                    for z in range(1, len(players)+1):
                        if z == player.player_id:
                            pogo_board.status[z-1][i][j] = 1
                        else:
                            pogo_board.status[z-1][i][j] = 0
                    
                    # Check if a rectangle has been closed
                    closed_rectangle = find_smallest_rectangle(pogo_board.status[player.player_id - 1],(3,3))

                    # If the player has closed a rectangle
                    if(closed_rectangle[0] != (-1,-1)):
                        # [PRINT FOR DEBUGGING PURPOSES]
                        #print(f"Player {players[current_player].player_id} closed a {closed_rectangle[1]}x{closed_rectangle[2]} rectangle at the following path: {closed_rectangle[3]}")

                        # The player's score gets updated with the rectangle's area
                        player.update_score_and_leds(closed_rectangle[1]*closed_rectangle[2])

                        # [PRINT FOR DEBUGGING PURPOSES]
                        #print(f"Player {players[current_player].player_id}'s current score is {players[current_player].score}")

                        # [THE TILES CORRESPONDING TO THE CLOSED RECTANGLE GET "RESET"-TED]
                        for tile_coordinates in closed_rectangle[3]:
                            pogo_board.pogo_tiles[tile_coordinates[0]][tile_coordinates[1]].change_acquisition(0)
                            pogo_board.status[player.player_id - 1][tile_coordinates[0]][tile_coordinates[1]] = 0


    #  /---------------------------\
    # | POWER UP ACQUISITION SYSTEM |
    #  \---------------------------/
    # It's only active during the "game session" phase
    if game_phase == GamePhase.GAME_SESSION:
        # Decrement the validity of each currently instantiated power
        # up + Removing the powerUPs whose validity has expired
        for power_up in power_ups:
            for player in players:
                if(power_up.check_collisions([player])):
                    if(power_up.validity > 0):
                        #print(f"Player {player.player_id} has acquired a power up") # [FOR DEBUGGING PURPOSES]
                        power_up.validity = 0                                       # Once the power up has been
                                                                                    # acquired, its validity expires
                        
                        # [Thus, the power up gets removed from the
                        #  list of power ups positioned on the board]
                        if(power_up in power_ups):
                            power_ups.remove(power_up)

                        # Whichever branch removed the power up, the "has_power_up"
                        # attribute of the player gets set to "True".
                        player.has_power_up = True
                        player.power_up_instantiation_time = elapsed_time_sec
                        
                        # The surface for the "power up" slot has to be computed as soon as the
                        # player acquires this power up, so that it can be blitted later in
                        # this very game loop iteration
                        player.scorer.compute_power_up_surface()
                else:
                    power_up.validity = power_up.initial_validity - (elapsed_time_sec - power_up.instantiation_time)
                    if(power_up.validity == 0):
                        if(power_up in power_ups):                                  # The item is removed only if it hasn't
                            power_ups.remove(power_up)                              # been already removed in the meanwhile


        # [For each player, if they already possess a power up, its validity gets decreased every second]
        for player in players:
            if player.has_power_up:
                player.power_up_validity = player.power_up_initial_validity - (elapsed_time_sec - player.power_up_instantiation_time)
                if(player.power_up_validity == 0):
                    player.has_power_up = False
            
            #If the player is currently powered up, the power up "duration" also gets decreased
            if player.is_powered_up:
                player.power_up_duration = player.initial_power_up_duration - (elapsed_time_sec - player.power_up_activation_time)
                if(player.power_up_duration == 0):
                    player.is_powered_up = False
                

        #  /--------------------------------------------\
        # | BLITTING EVERY ACTIVE POWER UP ON THE SCREEN |
        #  \--------------------------------------------/
        for power_up in power_ups:
            game_surface.blit(power_up.surface, power_up.screen_position)
            # All of the power ups get blitted underneath the players


    #  /-----------------------------------------------------------------------------\
    # | Blitting the player(s) on the game surface (not on the playing surface, given | 
    # | that the back of the player's sprite will be cut out off of said surface)     |
    #  \-----------------------------------------------------------------------------/
    # The order in which the players get blitted is ascending with the "Y" screen
    # coordinate (if a player has got a bigger "Y" screen coordinate, said player is
    # positioned closer to the camera).
    sorted_players = sorted(players, key=lambda p: p.screen_position[1])
    for i in range(len(players)):
        #pygame.draw.rect(game_surface, (255,0,0), sorted_players[i].hitbox) # -> [FOR DEBUGGING PURPOSES]
        game_surface.blit(sorted_players[i].surface,
                          sorted_players[i].screen_position)

    # Rendering the global shadows
    game_surface.blit(global_shadow,(0,0))

    # Rendering the global lights and ambience
    game_surface.blit(lights_and_ambience,(0,0))
    
    #  /------------\
    # | HUD BLITTING |
    #  \------------/
    # It's only active during the "game session" phase
    if game_phase == GamePhase.GAME_SESSION:
        # [THE HUD GETS BLITTED ON TOP OF EVERYTHING]
        for i in range(len(players)):
            # Blitting the "power up" slot shadow, if the player indexed by "i" does have one
            if players[i].has_power_up:
                game_surface.blit(players[i].scorer.__class__.POWER_UP_SLOT_BASE_SHADOW, players[i].scorer.power_up_screen_position)
            
            # Blitting the PlayerScorer element of the HUD
            game_surface.blit(players[i].scorer.surface, players[i].scorer.screen_position)

            # Blitting the "power up" slot surface, if the player indexed by "i" does have one
            if players[i].has_power_up:
                game_surface.blit(players[i].scorer.power_up_surface, players[i].scorer.power_up_screen_position)

        game_surface.blit(time_left_shadow,(230,-10))
        game_surface.blit(time_left_surface,(230,-10))
        game_surface.blit(timer_surface, (222,20))

        if(game_termination):
            game_surface.blit(game_over_shadow)
            game_surface.blit(game_over_surface)

            # The "winning surface" associated with the player
            # with the highest score gets blitted on the game_surface.
            game_surface.blit(winning_player_shadows[sorted(players, key=lambda p: p.score)[-1].player_id - 1])
            game_surface.blit(winning_player_surface[sorted(players, key=lambda p: p.score)[-1].player_id - 1])
    else:
        #  /----------------------------------------------------------------------------------------------\
        # | IF THE GAME IS IN THE "PLAYER_SPAWNING" PHASE, WHAT GETS BLITTED ARE THE "WAITING FOR PLAYERS" |
        # | HUD ELEMENT ON THE TOP HALF OF THE SCREEN AND THE "PLAYER READY" UNDER THE PLAYERS' SPRITES    |
        #  \----------------------------------------------------------------------------------------------/
        game_surface.blit(wait_players_surface)
        

    if(fullscreen):
        fullscreen_surface = pygame.transform.scale(game_surface, cmndef.fullscreen_game_size)
        screen.blit(fullscreen_surface, (0,0))
    else:
        screen.blit(game_surface,(0,0))

    pygame.display.flip()

    # The players surfaces get updated
    for i in range(len(players)):
        players[i].compute_surface()
        players[i].scorer.compute_surface()
        players[i].scorer.compute_power_up_surface()

    # The surfaces for the
    # board's tiles get updated
    pogo_board.compute_surfaces()

    # The game gets terminated as soon as a
    # player reaches the highest score
    if any(players[i].score == cmndef.MAX_SCORE for i in range(len(players))):
        game_termination = True

    #  /--------------------------------------------------\
    # | Calculating the time (in seconds) that has elapsed |
    # | between the first game loop and the current one    |
    #  \--------------------------------------------------/
    elapsed_time_sec = (pygame.time.get_ticks() - start_time) // 1000

    if not game_termination:
        # This gets used to calculate the time left
        # for the game session to get terminated.
        time_left = cmndef.MAX_TIME - elapsed_time_sec

        # If a multiple of 15 seconds has passed, a power 
        # up gets added in a random place on the board. 
        # [N.B]:
        #   The final "and" in the condition guarantees that a new power up does not get added at each game
        #   loop which has the same "divide-able by 15" elapsed time count (if "elapsed_time_sec == 15", for
        #   example, the last condition makes it so the power up gets added just only at the first game loop
        #   in which "elapsed_time_sec == 15").
        if(elapsed_time_sec != 0 and elapsed_time_sec % 15 == 0 and elapsed_time_sec != most_recent_power_up_sec):
            most_recent_power_up_sec = elapsed_time_sec
            power_ups.append(PowerUp((random.randint(0,7) + 9, random.randint(0,7) + 5), most_recent_power_up_sec))
            # [FOR DEBUGGING PURPOSES]
            #print(f"New power up added at second {elapsed_time_sec}, at position ({power_ups[-1].grid_position[0]},{power_ups[-1].grid_position[1]})")

        if(time_left == 0):
            game_termination = True
            power_ups = []  # When there's no time left, all of the "PowerUp" objects
                            # get removed from the list (this way, they won't be
                            # blitted on the board in the following game loops)


    timer_surface = cmndef.update_timer_surface(time_left)

    # Wait for 60 ticks
    clock.tick(60)

# [The connections with the BT modules get closed]
for player in players:
    sercom.turn_led_on(0,player.controller_serial_port)
    player.receiver_stop_event.set()    # To stop the reading thread operations
    player.receiver_thread.join()                                    
    player.dequeueing_thread.join()     # Wait for the thread's termination, before
                                        # closing the connection and terminating the
                                        # main thread.
                                                                     
    sercom.close_connection(player.controller_serial_port)

# The game gets closed
pygame.quit()