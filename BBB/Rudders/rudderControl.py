import Adafruit_BBIO.PWM as PWM
import grpc
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)


# Setup grpc
channel = grpc.insecure_channel('localhost:50051')
stub = ms_grpc.RudderGetterStub(channel)

# Setup PWM out
PWM.start(str(CONST.RUDDER_OUT_PIN), 50)

try:
    while True:
        ## Comms
        ControlAngle = stub.GetRudderSetting(succ=True)
        ## Set PWM to comms value
        PWM.set_duty_cycle(str(CONST.RUDDER_OUT_PIN), ControlAngle.controlAngle)
except KeyboardInterrupt:
    PWM.stop(str(CONST.RUDDER_OUT_PIN))
    PWM.cleanup()