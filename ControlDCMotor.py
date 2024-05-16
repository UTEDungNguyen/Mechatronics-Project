

import time
import serial
import PLCController
from PLCController import PLC
from snap7.util import *
from snap7.types import *
import snap7.client as c
import snap7

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

def main():
    # Open the serial port
    with serial.Serial("/dev/ttyAMA0", 9600) as ser:
        #print("Serial test begin...")
        state = 0 

        # Send messages
        # ser.write(b"Hello guys\n")
        # ser.write(b"Dungdeptrai\n")

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
            time.sleep(0.1)



if __name__ == "__main__":
 
    time.sleep(2)
    print(PLC.ReadMemory(20, 0, S7WLDWord))
    main()
