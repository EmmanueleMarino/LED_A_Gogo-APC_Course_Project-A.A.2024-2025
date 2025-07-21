'''
[SPAWN PLAYERS]:
This module handles the detection and spawning of players on
the "pogo board". A player gets inserted in a list of players
when a new connection towards a bluetooth module is successful.
'''


# [IMPORT OF LIBRARIES]
from modules.scripts.serial_communication import serial_communication as sercom
from modules.entities.player import Player
import serial
import threading

# [FOR DEBUGGING PURPOSES] => Highest possible number of players in a same game session
MAX_PLAYERS_NUM = 3

# [Function which adds players to the list of
#  players when it manages to connect to the
#  COM ports]
def detect_players(players_list, stop_event):
    while not stop_event.is_set():
        #  /-----------------------------------------------------------------------------------------------------------------\
        # | The reason the while condition has not been set as "not stop_event.is_set && len(players_list) < MAX_PLAYERS_NUM" |
        # | is the fact that in the main program, the "players detecting thread" will get terminated only when each of the    |
        # | four players will have pressed the "USER BUTTON" to declare themselves ready to start the game session.           |
        #  \-----------------------------------------------------------------------------------------------------------------/
        # That means, this cycle will keep on executing even if all the boards
        # have been detected (until every player is in the "ready" state).
        if len(players_list) < MAX_PLAYERS_NUM:
            serial_port_object = sercom.connect_bt_module(sercom.COM_PORTS[len(players_list)], 9600, 2)
            if isinstance(serial_port_object, serial.Serial):
                players_list.append(Player(Player.STARTING_POSITIONS[len(players_list)], len(players_list) + 1, serial_port_object))


# [Function to spawn the thread which detects players]
def start_players_detecting_thread(players_list, stop_event):
    thread = threading.Thread(
        target=detect_players,
        args=(players_list, stop_event),
        daemon=True         # ["daemon=True"]: this means the thread 
                            # will close when the main program ends
    )
    thread.start()
    return thread