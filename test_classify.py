import serial 
import time 
import PLCController
from PLCController import PLC
import snap7
from snap7.util import *
from snap7.types import *
import snap7.client as c
import threading
ser = serial.Serial("/dev/ttyAMA0", 9600)
state = False
stop_threads = False

# def sensor(ser):
#     while True:
#         global stop_threads
#         while stop_threads:
#             if (PLC.ReadMemory(5,3,S7WLBit) == True and PLC.ReadMemory(5,4,S7WLBit) == True):
#                 ser.write(b"S")
#                 stop_threads = False
            
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
            elif data_receive == "F" :
                data_receive = ""
            
# Create thread to read data from serial
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.daemon = True
thread.start()
            
# # Tạo một luồng để đọc dữ liệu từ serial
# thread_sensor = threading.Thread(target=sensor, args=(ser,))
# thread_sensor.daemon = True
# thread_sensor.start()

# CLassification DC Motor
while(True):
    # global stop_threads
    Sensor =PLC.ReadMemory(5,2,S7WLBit)
    if Sensor == True and state == False:
    # if Sensor == True:
        ser.write(b"R")
        state = True
    while stop_threads:
        if (PLC.ReadMemory(5,3,S7WLBit) == True):
            ser.write(b"S")
            stop_threads = False
#time.sleep(0.2)
#ser.write(b"L")
# time.sleep(0.35)