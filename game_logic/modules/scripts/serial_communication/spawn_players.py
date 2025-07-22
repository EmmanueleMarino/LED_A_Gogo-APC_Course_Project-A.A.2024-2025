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
MAX_PLAYERS_NUM = 4

# [Function which adds players to the list of
#  players when it manages to connect to the
#  COM ports]
def detect_players(players_list, stop_event):
    while not stop_event.is_set():
        # If the number of known ports is < 4,
        # the thread tries to detect a new
        # connected port, and eventually adds it
        # to the ports list
        if len(sercom.COM_PORTS) < 4:
            new_port = sercom.detect_new_COM_port(sercom.COM_PORTS)
            if len(new_port) != 0:
                print(f"A new port has been detected: {new_port[0]}")
                sercom.COM_PORTS.append(new_port[0])
        #  /-----------------------------------------------------------------------------------------------------------------\
        # | The reason the while condition has not been set as "not stop_event.is_set && len(players_list) < MAX_PLAYERS_NUM" |
        # | is the fact that in the main program, the "players detecting thread" will get terminated only when each of the    |
        # | four players will have pressed the "USER BUTTON" to declare themselves ready to start the game session.           |
        #  \-----------------------------------------------------------------------------------------------------------------/
        # That means, this cycle will keep on executing even if all the boards
        # have been detected (until every player is in the "ready" state).
        if len(players_list) < MAX_PLAYERS_NUM and len(players_list) < len(sercom.COM_PORTS):
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