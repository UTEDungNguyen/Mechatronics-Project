import serial
import threading
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

def read_from_port(ser):
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print(data.decode("utf-8"))
            
def sensor(ser):
    global state
    while True:
        if (PLC.ReadMemory(5,3,S7WLBit) == True and PLC.ReadMemory(5,4,S7WLBit)== True and state == 1):
            ser.write(b"S")
            state = 0

if __name__ == "__main__":
    # Thiết lập các thông số cho kết nối serial
    port = "/dev/ttyAMA0"  # Thay đổi tên cổng serial tương ứng với hệ điều hành và phần cứng của bạn
    baudrate = 9600  # Tốc độ baud của kết nối
    state = 0

    ser = serial.Serial(port, baudrate)
    if ser.isOpen():
        print(f"Đã mở kết nối serial tới {port} với tốc độ baudrate là {baudrate}.")

    # Tạo một luồng để đọc dữ liệu từ serial
    thread = threading.Thread(target=read_from_port, args=(ser,))
    thread.daemon = True
    thread.start()
    
    # Tạo một luồng để đọc dữ liệu từ serial
    thread_sensor = threading.Thread(target=sensor, args=(ser,))
    thread_sensor.daemon = True
    thread_sensor.start()

    # Giữ chương trình chạy để có thể nhận dữ liệu
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Kết thúc chương trình.")
        ser.close()
