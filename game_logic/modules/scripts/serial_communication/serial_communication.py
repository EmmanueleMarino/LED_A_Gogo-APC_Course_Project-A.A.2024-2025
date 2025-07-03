'''
[SERIAL COMMUNICATION MODULE]:
This software module handles the transmission and
reception of messages to and by the "HC-05" Bluetooth
module.

[AN ISSUE]:
This module is dependent from the way the specific
OS handles the connection with Bluetooth devices.

For now, it only works for Windows: eventually, making it
independent from the specific OS could be a desirable result.
'''

# [IMPORT OF LIBRARIES]
import serial   # Pyserial

# [Function to enstablish the connection
#  with the Bluetooth module]
def connect_bt_module(COM_port, baud_rate, timeout):
    '''
    [PARAMETERS]:
        "COM_port"  : the name (str) of the "virtual serial port"
                      defined by Windows when a BT device gets
                      paired with the computer.
         
        "baud_rate" : it's the transmission rate,
                      expressed in bits/second.

        "timeout"   : the time - in seconds - after which a
                      connection is deemed "failed".

    [RETURN]:
        "serial_port_obj" : reference of the object of the "Serial"
                            class which gets instantiated.

        If the connection fails, an error code gets returned
    '''
    try:
        serial_port_obj = serial.Serial(COM_port, baudrate=baud_rate, timeout=timeout)
        return serial_port_obj
    except serial.SerialException as e:
        return f"[SERIAL PORT OPENING ERROR]:\n{e}\n\n"


# [Function which gets called when 
#  a new LED has to be turned on]
def turn_led_on(led_code, serial_port_obj):
    '''
    [PARAMETERS]:
        "led_code"        : integer code of the LED which has to be turned on.
        "serial_port_obj" : reference to the object of the "Serial" class
                            relative to a certain player.
        
    [RETURN]:
        "return_type"     : "s" character (for "success") if the message has
                            succesfully been sent to the board 
                            
                            "e" character if there's been an error in the
                            communication.
    '''
    try:
        # The message is constructed as a string containing
        # the LED code and the "new line" (\n) character
        msg = f"{led_code}\n"

        # The LED turning on is handled by the STM32F3DISCOVERY board's firmware,
        # so the Python program only has to send a message containing the LED
        # code to the BT module.
        serial_port_obj.write(msg.encode('utf-8'))  # The message gets converted
                                                    # to a sequence of raw bytes
        return "s", "The message was successfully sent to the BT module"
    except Exception as e:
        return "e", (f"[SERIAL COMMUNICATION ERROR]: {e}")


# [Function used to close the connection with the
#  BT device when the game session gets terminated]
def close_connection(serial_port_obj):
    '''
    [PARAMETERS]:
        "serial_port_obj" : reference to the object of the "Serial" class
                            relative to a certain player.
    [RETURN]:
        None
    '''
    serial_port_obj.close()