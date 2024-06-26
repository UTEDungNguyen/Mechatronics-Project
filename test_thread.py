import serial
import threading

def read_from_port(ser):
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print(data.decode("utf-8"))

# def handle_data(data):
#     print(f"Received: {data.decode("utf-8")}")
    # Thực hiện các xử lý khác với dữ liệu nhận được tại đây

if __name__ == "__main__":
    # Thiết lập các thông số cho kết nối serial
    port = "/dev/ttyAMA0"  # Thay đổi tên cổng serial tương ứng với hệ điều hành và phần cứng của bạn
    baudrate = 9600  # Tốc độ baud của kết nối

    ser = serial.Serial(port, baudrate)
    if ser.isOpen():
        print(f"Đã mở kết nối serial tới {port} với tốc độ baudrate là {baudrate}.")

    # Tạo một luồng để đọc dữ liệu từ serial
    thread = threading.Thread(target=read_from_port, args=(ser,))
    thread.daemon = True
    thread.start()

    # Giữ chương trình chạy để có thể nhận dữ liệu
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Kết thúc chương trình.")
        ser.close()
