import Adafruit_BBIO.UART as UART
import serial
import signal
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc
from gRPC import PWMMessages_pb2 as PWMmsgs
from gRPC import PWMMessages_pb2_grpc as PWMmsgs_grpc

UART.setup("UART2")

ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
ser.close()
ser.open()
if ser.isOpen():
    print("Serial is open")
try:
    while True:
        if ser.isOpen():
            receivedData = PWMmsgs.PWMValues()
            data = ser.read(200)
            print("Data size: ")
            print(len(data))
            print('\n')
            if data:
                receivedData.ParseFromString(data) # Receiving a single float
            aw_data_ch1 = receivedData.ch1
            aw_data_ch2 = receivedData.ch2
            aw_data_ch3 = receivedData.ch3
            aw_data_ch4 = receivedData.ch4
            aw_data_ch5 = receivedData.ch5
            aw_data_ch6 = receivedData.ch6
            print("Ch1: " + str(aw_data_ch1))
            print("Ch2: " + str(aw_data_ch2))
            print("Ch3: " + str(aw_data_ch3))
            print("Ch4: " + str(aw_data_ch4))
            print("Ch5: " + str(aw_data_ch5))
            print("Ch6: " + str(aw_data_ch6))
            if not aw_data_ch1:
                pass
            sendData = PWMmsgs.RudderAngle()

            try:
                sendData.control_angle = input("Control Angle: ")
                if sendData.control_angle:
                    ser.write(sendData.SerializeToString())
            except:
                pass


            # PWMReads = ser.read(192)
            # print(PWMReads)
            # ser.write("BBB here")

except KeyboardInterrupt:    
    ser.close()
    #UART.cleanup() # Check https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/uart if this is implemented