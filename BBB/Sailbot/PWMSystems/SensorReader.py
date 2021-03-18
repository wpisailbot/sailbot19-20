"""
"""
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC



# Set up GPIO reading of the hall effect sensors. Need to do this using the logic level shifter because the sensors need and output 5V, while the BBB runs on 3V!!
# print("setting up GPIO")
GPIO.setup(CONST.HALL_STBD_PIN, GPIO.IN)
GPIO.setup(CONST.HALL_PORT_PIN, GPIO.IN)



# Set up the ADC for reading the pot that was in the plans, but never materialized due to campus closure.
# print("setting up ADC")
ADC.setup()



# Create a protobuf to store sensor values and fill it in with dummy values.
# NOTE: filling protobufs with 0s seems to result in a completely empty structure that will not be properly decoded on the other side.
sensor_msg = ms.BBBSersorData()
sensor_msg.hall_port = False
sensor_msg.hall_stbd = False
sensor_msg.pot_val = 0.5
sensor_msg.pot_centered = True



def readSensors(): # Call this with some regularity
    # Check if the pot is centered
    sensor_msg.pot_val = ADC.read(CONST.MOV_BAL_POT_PIN)
    sensor_msg.pot_centered = sensor_msg.pot_val > CONST.MOV_BAL_MIN_ANGL + CONST.MOV_BAL_ANGL_TOL and sensor_msg.pot_val < CONST.MOV_BAL_MAX_ANGL - CONST.MOV_BAL_ANGL_TOL

    # The idea in these statements is that if this function is called with some
    # regularity, the sensors will get tripped both going up and down, so it
    # switching the state variables should be possible. This is UNTESTED.
    if(GPIO.input(CONST.HALL_STBD_PIN) and not sensor_msg.pot_centered):
        sensor_msg.hall_port = not sensor_msg.hall_port
    if(GPIO.input(CONST.HALL_PORT_PIN) and not sensor_msg.pot_centered):
        sensor_msg.hall_stbd = not sensor_msg.hall_stbd
    if(sensor_msg.pot_centered):
        sensor_msg.hall_port = False
        hallSsensor_msg.hall_stbdtbd = False

    # print("port:" + str(sensor_msg.hall_port))
    # print("stbd:" + str(sensor_msg.hall_stbd))



# gRPC class for responding to requests
class BBBSensorReaderServicer(ms_grpc.BBBSensorReaderServicer):
    def __init__(self):
        pass
    def GetSensorData(self, request, context):
        return sensor_msg


# Start and attach server
serverSensor = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
ms_grpc.add_BBBSensorReaderServicer_to_server(BBBSensorReaderServicer(), serverSensor)
serverSensor.add_insecure_port('localhost:50053') # Make sure that the port is unique (not used by any other servers on the board)
serverSensor.start()



try:
    while True:
        try:
            # continuusly read sensor state
            readSensors()
        except Exception as e:
            print(str(e))

except KeyboardInterrupt:    
    GPIO.cleanup()