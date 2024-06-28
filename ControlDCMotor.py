

import time
import serial
import PLCController
from PLCController import PLC
from snap7.util import *
from snap7.types import *
import snap7.client as c
import snap7
import threading

'''
areas = ADict({
    'PE': 0x81,
    'PA': 0x82,
    'MK': 0x83,
    'DB': 0x84,
    'CT': 0x1C,
    'TM': 0x1D,
})
'''
state = 0
state_count = False
stop_threads = False
ser = serial.Serial("/dev/ttyAMA0", 9600)
            
def read_from_port(ser):
    global data_receive, stop_threads
    while True:
        if ser.in_waiting > 0:
            data_receive = ser.read(ser.in_waiting)
            data_receive = data_receive.decode("utf-8")
            print(data_receive)
            if data_receive == "H" :
                stop_threads = True
                data_receive = ""
            
# Create thread to read data from serial
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.daemon = True
thread.start()

def main():
    # Open the serial port
    # with serial.Serial("/dev/ttyAMA0", 9600) as ser:
    #     #print("Serial test begin...")
    #     state = 0 

    #     # Send messages
    #     # ser.write(b"Hello guys\n")
    #     # ser.write(b"Dungdeptrai\n")
    global state, stop_threads, state_count
    while True:
        # Check if there is data available to read
        if ser.in_waiting > 0:
            # Read and print the received data
            data = ser.read(ser.in_waiting)
            #print(data.decode("utf-8"))
            
        if state == 0:
            vel = PLC.ReadMemory( 160, 0, S7WLWord)
            if vel > 99:
                vel = 99
            ser.write(str.encode(str(vel))) 
            state = 1
        else :
            if (PLC.ReadMemory( 160, 0, S7WLWord) - vel) != 0 :
                state = 0
        print(vel)
        # You might want to add a delay to avoid busy-waiting and improve performance
        # time.sleep(0.1)
        # global stop_threads
        # Sensor =PLC.ReadMemory(5,2,S7WLBit)
        # if Sensor == True and state_count == False:
        # # if Sensor == True:
        #     ser.write(b"R")
        #     state_count = True
        while stop_threads:
            if (PLC.ReadMemory(5,3,S7WLBit) == True):
                ser.write(b"S")
                stop_threads = False



if __name__ == "__main__":
 
    time.sleep(2)
    print(PLC.ReadMemory(20, 0, S7WLDWord))
    main()
