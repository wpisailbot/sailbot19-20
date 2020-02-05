from concurrent import futures
import grpc
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc
from gRPC import PWMMessages_pb2 as pwm
from gRPC import PWMMessages_pb2_grpc as pwm_grpc
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)
#https://keyboardinterrupt.org/catching-a-keyboardinterrupt-signal/


rudderControlAngle = 50
apparentWind = ms_grpc.ApparentWind()

class RudderGetterServicer(ms_grpc.RudderGetterServicer):
    def GetTrimTabSetting(self, request, context):
        rudderControlAngle = ms_grpc.ControlAngle()
        rudderControlAngle.control_angle = rudderControlAngle
        return apparentWind


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ms_grpc.add_RudderGetterServicer_to_server(RudderGetterServicer, server)
server.add_insecure_port('localhost:50051')
server.start()



# Setup grpc
channel = grpc.insecure_channel('localhost:50051')
stubTrim = ms_grpc.TrimTabGetterStub(channel)
stubPWM = ms_grpc.PWMReaderStub(channel)



def loop():
    PWMInput = stubPWM.GetPWMInputs(ms_grpc.req(succ=True))

    trimControlAngle = ms_grpc.ControlAngle()
    trimControlAngle.control_angle = PWMInput.ch1
    rudderControlAngle = PWMInput.ch2

    apparentWind = stubTrim.GetTrimTabSetting(ms_grpc.req(succ=True))

def cleanup():
    pass

try:
    while True:
        loop()
except KeyboardInterrupt:
    cleanup()