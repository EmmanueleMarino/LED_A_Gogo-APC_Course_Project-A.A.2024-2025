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
import serial       # Pyserial
import queue        # To build a queue
import threading    # To spawn a new thread for message reception
import re           # For regex expressions used to validate message formats
import time         # To put the "reading/receiving thread" to sleep if there's
                    # no available data to receive in its current iteration


# Regex expressions to validate the message formats
GYRO_REGEX = re.compile(r"^HgyroP-?\d+\.\d+,-?\d+\.\d+$")   # Gyroscope readings
SPEED_REGEX = re.compile(r"^HspeedPgo$")                    # Power up/Speed up commands


# COM ports towards which the connections will be opened.
# For now, they're hardcoded (the BT module have already been paired with the computer),
# if we have time, we'll try to determine them in a dynamic fashion.
COM_PORTS = ['COM7','COM12','COM14','']

# [N.B.]: it's likely the computer can handle just a single BT connection at once, so
# we'll have to try using UART to USB adapters for the rest of the boards... for now,

# We'll have to check if the "USER USB" on the STM32F3DISCOVERY board is capable of
# sending and receiving data in a full-duplex (or even "half-duplex") mode, or if
# it is only simplex. Anyway, even if it is solely simplex, we'll use it just to
# start testing the movement for the rest of the boards.

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
        # [FOR DEBUGGING PURPOSES]
        print(f"Connection detected on the '{COM_port}' port\n")
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


# [Function to validate a message which is
#  received from the Bluetooth Module via the
#  virtual serial port]
def check_msg_validity(msg_line):
    return GYRO_REGEX.match(msg_line) or SPEED_REGEX.match(msg_line)


# [Function for reception of messages on "the virtual serial port" and
#  the insertion of said messages in two different queues]
def msg_rx_and_enqueueing(serial_port_obj, gyro_msgs, speed_msg, stop_event):
    '''
    Receives messages from the "serial_port_obj", validates
    them and inserts them in two different queues:
    - gyro_msgs (max size 64) for the gyroscope readings
    - speed_msg (max size 1) for a "speed up" command

    A new "speed up" command overwrites the former "speed_msg".
    '''
    # Lock to synchronize access to the queues, ensuring thread safety
    lock = threading.Lock()
    
    # This cycle will have to be terminated by setting a "stop_event"
    # before closing the connection with the "virtual serial port"
    while not stop_event.is_set():
        # Check if there are bytes waiting to be read on the serial port
        if serial_port_obj.in_waiting > 0:
            try:
                # Read one full line from serial (until '\n'), decode as ASCII, strip whitespace
                line = serial_port_obj.readline().decode(errors='ignore').strip()
            except Exception as e:
                print(f"Error decoding or reading from serial port: {e}")
                continue  # Skip to next iteration on error
            
            # [Validate the message format]
            if check_msg_validity(line):
                # [Checking and enqueueing "gyroscope readings" messages]
                if GYRO_REGEX.match(line):
                    with lock:
                        # If the gyro queue is full, remove the oldest message to make
                        # space for new ones [what is being realized is a CIRCULAR QUEUE,
                        # in which the oldest messages get overwritten if the queue is full
                        # but there's new available messages to receive]
                        if gyro_msgs.full():
                            try:
                                gyro_msgs.get_nowait()  # Non-blocking removal
                            except queue.Empty:
                                pass  # Queue unexpectedly empty, ignore

                        # ------------------------\
                        # [FOR DEBUGGING PURPOSES] |
                        #print(line)               |
                        # -------------------------/

                        # Add the new message consisting of gyroscope readings
                        gyro_msgs.put(line)
                # [Checking the presence of a "power up"/"speed up"]
                elif SPEED_REGEX.match(line):
                    with lock:
                        # Overwrite the existing "speed up" message
                            speed_msg[0] = line
                        
                            # ------------------------\
                            # [FOR DEBUGGING PURPOSES] |
                            #print(line)               |
                            # -------------------------/
                            print(line)
            # Messages that don't match the expected format are ignored
        else:
            # No data available, sleep briefly to avoid busy-waiting
            time.sleep(0.01)


# [Function to start a background thread to receive and enqueue serial messages]
def start_serial_receiver_thread(serial_port_obj, gyro_msgs, speed_msg, stop_event):
    thread = threading.Thread(
        target=msg_rx_and_enqueueing,
        args=(serial_port_obj, gyro_msgs, speed_msg, stop_event),
        daemon=True         # ["daemon=True"]: this means the thread 
                            # will close when the main program ends
    )
    thread.start()
    return thread


# [Function to process gyroscope readings and
#  turn them to a 2-elements tuple of floats]
def gyro_msg_processing(msg):
    readings = msg[6:-1]    # The "HgyroP" part of the message gets deleted
    
    gyro_x_str, gyro_y_str = readings.split(",",1)  # The readings get split into 
                                                    # two substrings (separated by
                                                    # the "," character)

    # Those readings are converted to floats
    gyro_x = float(gyro_x_str)
    gyro_y = float(gyro_y_str)

    # The 2-elements couple of readings gets returned to the caller
    return (gyro_x,gyro_y)