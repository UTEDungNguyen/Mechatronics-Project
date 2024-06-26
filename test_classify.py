import serial 
import time 
import PLCController
from PLCController import PLC
import snap7
from snap7.util import *
from snap7.types import *
import snap7.client as c
ser = serial.Serial("/dev/ttyAMA0", 9600)

# CLassification DC Motor
while(True):
    Sensor =PLC.ReadMemory(5,2,S7WLBit)
    if Sensor == True:
    
        ser.write(b"R")
#time.sleep(0.2)
#ser.write(b"L")
# time.sleep(0.35)