import Adafruit_BBIO.UART as UART
import serial
UART.setup("UART2")
ser = serial.Serial(port = "/dev/ttyO2", baudrate=115200)
ser.close()
ser.open()
if ser.isOpen():
    print("Serial is open")
    read = ser.read(5) 
    print(read)
    while True:
        ser.write("bye")
        
