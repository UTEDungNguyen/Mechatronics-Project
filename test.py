from snap7.util import *
from snap7.snap7types import *
import snap7.client as c
import snap7
import time
import serial

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
                vel = ReadMemory(plc, 160, 0, S7WLWord)
                if vel > 99 :
                    vel = 99
                ser.write(str(vel)) 
                state = 1
            else :
                if (ReadMemory(plc, 160, 0, S7WLWord) - vel) != 0 :
                    state = 0
            #print(vel)
            # You might want to add a delay to avoid busy-waiting and improve performance
            time.sleep(0.1)


def WriteMemory(plc, byte, bit, datatype, value):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        set_bool(result, 0, bit, value)
    elif datatype == S7WLByte or datatype == S7WLWord:
        set_int(result, 0, value)
    elif datatype == S7WLReal:
        set_real(result, 0, value)
    elif datatype == S7WLDWord:
        set_dword(result, 0, value)
    plc.write_area(areas["MK"], 0, byte, result)


def ReadMemory(plc, byte, bit, datatype):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        return get_bool(result, 0, bit)
    elif datatype == S7WLByte or datatype == S7WLWord:
        return get_int(result, 0)
    elif datatype == S7WLReal:
        return get_real(result, 0)
    elif datatype == S7WLDWord:
        return get_dword(result, 0)
    else:
        return None


if __name__ == "__main__":
    plc = c.Client()
    plc.connect('192.168.0.1', 0, 1)
    #print(plc.get_connected())
    time.sleep(2)
    #WriteMemory(plc, 0, 0, S7WLBit, 0)
    #print('Done')
    #print(ReadMemory(plc, 100, 0, S7WLWord))
    main()