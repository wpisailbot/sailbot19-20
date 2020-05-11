"""
This code sets up serial communication with the Arduino, PWM output to the rudder and ballast, and gRPC communication.
This code has only been partially tested, but it does appear to work.
"""
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.UART as UART
import serial



# Set up serial for communcation with the Arduino Mega
print("setting up UART")
UART.setup("UART2")
ser = serial.Serial(port = "/dev/ttyO2", baudrate=115200) # Make sure that the baud here and in PWMReader.ino are the same and that the tty device is not occupied by something else!!
ser.close() # Make sure that we don't try to open something that is already open
ser.open() # Open the serial connection

# Check that we've opened the connection and inform the programmer of the event if it is true
if ser.isOpen():
    print("Serial is open!")



# Create a protobuf to store PWM values and fill it in with dummy values.
# NOTE: filling protobufs with 0s seems to result in a completely empty structure that will not be properly decoded on the other side.
pwm_values = PWMmsgs.PWMValues()
pwm_values.ch1 = 11
pwm_values.ch2 = 12
pwm_values.ch3 = 13
pwm_values.ch4 = 14
pwm_values.ch5 = 15
pwm_values.ch6 = 16

# Create a protobuf to store control values for the rudder and the ballast and fill it in with dummy values.
# NOTE: filling protobufs with 0s seems to result in a completely empty structure that will not be properly decoded on the other side.
control_angles = PWMmsgs.ControlAngles()
control_angles.rudder_angle = 91
control_angles.ballast_angle = 92



# Set up PWM for controlling the TalonSRX and the rudder servo. This has been tested on a servo that comes in the RBE kit, but not on the hw on the boat.
# Adafruit's BBB Servo instructions were very helpful in setting this up.
print("setting up PWM")
duty_min = 3
duty_max = 14.5
duty_span = duty_max - duty_min
 
PWM.start(CONST.RUDDER_PIN, (100-duty_min), 60.0, 1)
PWM.start(CONST.MOV_BAL_PIN, (100-duty_min), 60.0, 1)



def rudder_action():
    # Read the position to which to set the rudder
    control_angles.rudder_angle = float(pwm_values.ch1)

    # Software limits to prevent overrotation
    if(control_angles.rudder_angle > CONST.RUDDER_MAX_ANGL):
        control_angles.rudder_angle = CONST.RUDDER_MAX_ANGL
    if(control_angles.rudder_angle < CONST.RUDDER_MIN_ANGL):
        control_angles.rudder_angle = CONST.RUDDER_MIN_ANGL

    # Calculte duty cycle and set it
    # https://learn.adafruit.com/controlling-a-servo-with-a-beaglebone-black/writing-a-program
    duty1 = 100 - ((control_angles.rudder_angle / 180) * duty_span + duty_min) 
    PWM.set_duty_cycle(CONST.RUDDER_PIN, duty1)



def mov_bal_action():
    # Read SPEED (not position) with which to move the mov. ballast
    control_angles.ballast_angle = float(pwm_values.ch2)
    
    # Limit the speed with which the movable ballast can move - these values are untested
    if(control_angles.ballast_angle > 90 + CONST.MOV_BAL_MAX_SPEED):
        control_angles.ballast_angle = control_angles.ballast_angle + CONST.MOV_BAL_MAX_SPEED
    elif(control_angles.ballast_angle < 90 - CONST.MOV_BAL_MAX_SPEED):
        control_angles.ballast_angle = control_angles.ballast_angle - CONST.MOV_BAL_MAX_SPEED

    # Request sensor state from SensorReader.py
    responseSensors = ms.BBBSersorData()
    with grpc.insecure_channel('localhost:50053') as channel: # make sure the port matches what is on the other side in SensorReader.py
        stubPWM = ms_grpc.BBBSensorReaderStub(channel)
        responseSensors = stubPWM.GetSensorData(ms.Server_request(req=True))

    # Do not move the ballast past design limits - these values are untested
    if(responseSensors.hall_port and control_angles.ballast_angle > 90):
        control_angles.ballast_angle = 90
    if(responseSensors.hall_stbd and control_angles.ballast_angle < 90):
        control_angles.ballast_angle = 90

    # Calculte duty cycle and set it
    # https://learn.adafruit.com/controlling-a-servo-with-a-beaglebone-black/writing-a-program
    duty2= 100 - ((control_angles.ballast_angle / 180) * duty_span + duty_min) 
    PWM.set_duty_cycle(CONST.MOV_BAL_PIN, duty2)



# gRPC class for responding to info requests
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


# Start and attach server
serverPWM = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
ms_grpc.add_PWMReaderServicer_to_server(PWMReaderServicer(), serverPWM)
serverPWM.add_insecure_port('localhost:50052') # Make sure that the port is unique (not used by any other servers on the board)
serverPWM.start()



# Get data from the Arduino using the Serial connection
# If you find trouble, first make sure that your crossed your connections - TX of BBB to RX of Arduino and vice versa
def serial_exchange():
    # print("Serial exchange")
    if ser.isOpen():
        # print("Serial still open")
        try:
            # Serial read - pause means next message
            # Reading one byte at a time because the size of the message is not deterministic
            data = bytearray()
            if(ser.in_waiting):
                while(ser.in_waiting):
                    byte = ser.read(1)
                    data.extend(byte)

            print("Decoding ")
            pwm_values.ParseFromString(data) # Receiving a single float

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print(str(e))
    else:
        print("Serial is no longer open")
        # pass



try:
    while True:
        try:
            # Receive PWM data from Arduino
            serial_exchange()
            # Move movable ballast
            mov_bal_action()
            # Move rudder
            rudder_action()
        except Exception as e:
            print(str(e))

except KeyboardInterrupt:    
    #UART.cleanup() # Check https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/uart if this is implemented
    pass