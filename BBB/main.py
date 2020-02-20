from concurrent import futures
import grpc
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)
#https://keyboardinterrupt.org/catching-a-keyboardinterrupt-signal/

apparentWind = tt.ApparentWind()
controlAngles = PWMmsgs.ControlAngles()
controlAngles.rudder_angle = 0
controlAngles.ballast_angle = 0
trimAngle = tt.TrimAngle()
PWMInput = PWMmsgs.PWMValues()
PWMInput.ch1 = 1
PWMInput.ch2 = 2
PWMInput.ch3 = 3
PWMInput.ch4 = 4
PWMInput.ch5 = 5
PWMInput.ch6 = 6



# Setup grpc

channelTrim = grpc.insecure_channel('localhost:50050')
stubTrim = ms_grpc.TrimTabGetterStub(channelTrim)
channelPWM = grpc.insecure_channel('localhost:50051')
stubPWM = ms_grpc.PWMReaderStub(channelPWM)



def loop():
    # PWMInput = stubPWM.GetPWMInputs(PWMmsgs.RudderAngle(control_angle = 0))
    stubPWM.GetPWMInputs(controlAngles)

    trimAngle.control_angle = PWMInput.ch1
    controlAngle.rudder_angle = PWMInput.ch2
    controlAngle.ballast_angle = PWMInput.ch3

    apparentWind = stubTrim.GetTrimTabSetting(trimAngle)



def cleanup():
    pass



try:
    while True:
        loop()
except KeyboardInterrupt:
    cleanup()