import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc

pwm_values = PWMmsgs.PWMValues()
pwm_values.ch1 = 11
pwm_values.ch2 = 12
pwm_values.ch3 = 13
pwm_values.ch4 = 14
pwm_values.ch5 = 15
pwm_values.ch6 = 16

control_angles = PWMmsgs.ControlAngles()
control_angles.rudder_angle = 91
control_angles.ballast_angle = 92

class PWMReaderServicer(ms_grpc.PWMReaderServicer):
    def __init__(self):
        pass
    def GetPWMInputs(self, request, context):
        rudderAngle = request.control_angle
        return pwm_values

    def GetPWMValues(self, request, context):
        return pwm_values

    def GetControlAngles(self, request, context):
        return control_angles


serverPWM = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
ms_grpc.add_PWMReaderServicer_to_server(PWMReaderServicer(), serverPWM)
serverPWM.add_insecure_port('localhost:50052')
serverPWM.start()


# spi = SPI(0,0)	#/dev/spidev1.0

try:
    while True:
        try:
            sendData = PWMmsgs.ControlAngles()
            try:
                sendData.rudder_angle = control_angles.rudder_angle 
                sendData.ballast_angle = control_angles.ballast_angle 
                # print("Rudder angle: ")
                # print(sendData.rudder_angle)
                # print("\n")

                # print("Rudder angle: ")
                # print(sendData.ballast_angle)
                # print("\n")
            except Exception as e:
                print(str(e))

            # data = spi.xfer(sendData, delay = 20)
            PWMReads = PWMmsgs.PWMValues()
            data = None # FOR TESTING ONLY
            if data:
                PWMReads.ParseFromString(data) # Receiving a single float
                pwm_values.ch1 = PWMReads.ch1
                pwm_values.ch2 = PWMReads.ch2
                pwm_values.ch3 = PWMReads.ch3
                pwm_values.ch4 = PWMReads.ch4
                pwm_values.ch5 = PWMReads.ch5
                pwm_values.ch6 = PWMReads.ch6
                # print("Ch1: " + str(pwm_values.ch1))
                # print("Ch2: " + str(pwm_values.ch2))
                # print("Ch3: " + str(pwm_values.ch3))
                # print("Ch4: " + str(pwm_values.ch4))
                # print("Ch5: " + str(pwm_values.ch5))
                # print("Ch6: " + str(pwm_values.ch6))

            
        except Exception as e:
            print(str(e))

except KeyboardInterrupt:    
    # spi.close()
    #UART.cleanup() # Check https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/uart if this is implemented
    pass