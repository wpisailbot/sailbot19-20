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



print("setting up UART")
UART.setup("UART2")
ser = serial.Serial(port = "/dev/ttyO2", baudrate=115200)
ser.close()
ser.open()
if ser.isOpen():
    print("Serial is open!")



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
    
    # Limit the speed with which the movable ballast can move
    if(control_angles.ballast_angle > 90 + CONST.MOV_BAL_MAX_SPEED):
        control_angles.ballast_angle = control_angles.ballast_angle + CONST.MOV_BAL_MAX_SPEED
    elif(control_angles.ballast_angle < 90 - CONST.MOV_BAL_MAX_SPEED):
        control_angles.ballast_angle = control_angles.ballast_angle - CONST.MOV_BAL_MAX_SPEED

    responseSensors = ms.BBBSersorData()
    with grpc.insecure_channel('localhost:50053') as channel:
        stubPWM = ms_grpc.BBBSensorReaderStub(channel)
        responseSensors = stubPWM.GetSensorData(ms.Server_request(req=True))

    # Do not move the ballast past design limits
    if(responseSensors.hall_port and control_angles.ballast_angle > 90):
        control_angles.ballast_angle = 90
    if(responseSensors.hall_stbd and control_angles.ballast_angle < 90):
        control_angles.ballast_angle = 90

    # Calculte duty cycle and set it
    # https://learn.adafruit.com/controlling-a-servo-with-a-beaglebone-black/writing-a-program
    duty2= 100 - ((control_angles.ballast_angle / 180) * duty_span + duty_min) 
    PWM.set_duty_cycle(CONST.MOV_BAL_PIN, duty2)



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



def serial_exchange():
    # print("Serial exchange")
    if ser.isOpen():
        # print("Serial still open")
        try:
            # Serial read - pause means next message
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
            serial_exchange()
            mov_bal_action()
            rudder_action()
        except Exception as e:
            print(str(e))

except KeyboardInterrupt:    
    #UART.cleanup() # Check https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/uart if this is implemented
    pass