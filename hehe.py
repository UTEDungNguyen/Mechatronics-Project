import serial
import time

def main():
    # Open the serial port
    with serial.Serial("/dev/ttyAMA0", 9600) as ser:
        print("Serial test begin...")

        # Send messages
        ser.write(b"Hello guys\n")
        ser.write(b"Dungdeptrai\n")

        while True:
            # Check if there is data available to read
            if ser.in_waiting > 0:
                # Read and print the received data
                data = ser.read(ser.in_waiting)
                print(data.decode("utf-8"))

            # You might want to add a delay to avoid busy-waiting and improve performance
            time.sleep(0.1)

if __name__ == "__main__":
    main()
