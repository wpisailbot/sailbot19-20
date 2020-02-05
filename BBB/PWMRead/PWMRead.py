import Adafruit_BBIO.UART as UART
import serial
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import PWMMessages_pb2 as pwm
from gRPC import PWMMessages_pb2_grpc as pwm_grpc

import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)


PWMReads = ms_grpc.PMWValues()
class PWMReaderServicer(ms_grpc.PWMReaderServicer):
    def GetPWMInputs(self, request, context):
        return PWMReads


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ms_grpc.add_PWMReaderServicer_to_server(PWMReaderServicer, server)
server.add_insecure_port('localhost:50051')
server.start()

UART.setup("UART1")

ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600)
ser.close()
ser.open()

try:
    while True:
        if ser.isOpen():
            PWMReads = ser.read(100)

except KeyboardInterrupt:    
    ser.close()
    #UART.cleanup() # Check https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/uart if this is implemented