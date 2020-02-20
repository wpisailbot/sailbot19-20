from Adafruit_BBIO.SPI import SPI
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)


ch1 = 0
ch2 = 0
ch3 = 0
ch4 = 0
ch5 = 0
ch6 = 0
rudderAngle = 0

class PWMReaderServicer(ms_grpc.PWMReaderServicer):
    def __init__(self):
        pass
    def GetPWMInputs(self, request, context):
        rudderAngle = request.control_angle

        PWMReads = PWMmsgs.PWMValues()

        PWMReads.ch1 = ch1
        PWMReads.ch2 = ch2
        PWMReads.ch3 = ch3
        PWMReads.ch4 = ch4
        PWMReads.ch5 = ch5
        PWMReads.ch6 = ch6

        return PWMReads


serverPWM = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
ms_grpc.add_PWMReaderServicer_to_server(PWMReaderServicer(), serverPWM)
serverPWM.add_insecure_port('localhost:50051')
serverPWM.start()


spi = SPI(0,0)	#/dev/spidev1.0

try:
    while True:
        try:
            sendData = PWMmsgs.ControlAngles()
            try:
                sendData.rudder_angle = rudderAngle
                sendData.ballast_angle = 0
                print("Rudder angle: ")
                print(sendData.rudder_angle)
                print("\n")

                print("Rudder angle: ")
                print(sendData.ballast_angle)
                print("\n")
            except:
                pass

            data = spi.xfer(sendData, delay = 20)
            PWMReads = PWMmsgs.PWMValues()

            if data:
                PWMReads.ParseFromString(data) # Receiving a single float
                ch1 = PWMReads.ch1
                ch2 = PWMReads.ch2
                ch3 = PWMReads.ch3
                ch4 = PWMReads.ch4
                ch5 = PWMReads.ch5
                ch6 = PWMReads.ch6
                print("Ch1: " + str(ch1))
                print("Ch2: " + str(ch2))
                print("Ch3: " + str(ch3))
                print("Ch4: " + str(ch4))
                print("Ch5: " + str(ch5))
                print("Ch6: " + str(ch6))

            
        except:
            pass

except KeyboardInterrupt:    
    spi.close()
    #UART.cleanup() # Check https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/uart if this is implemented