import serial 
import time 

ser = serial.Serial("/dev/ttyAMA0", 9600)

# CLassification DC Motor 
ser.write(b"L")
time.sleep(0.2)
ser.write(b"L")
# time.sleep(0.35)