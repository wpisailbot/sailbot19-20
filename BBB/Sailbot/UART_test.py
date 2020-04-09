import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.GPIO as GPIO
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
servo_pin1 = "P9_14"
servo_pin2 = "P9_16"
duty_min = 3
duty_max = 14.5
duty_span = duty_max - duty_min
 
PWM.start(servo_pin1, (100-duty_min), 60.0, 1)
PWM.start(servo_pin2, (100-duty_min), 60.0, 1)

hallPortPin = "P9_23"
hallStbdPin = "P9_15"
GPIO.setup(hallPortPin, GPIO.IN)
GPIO.setup(hallStbdPin, GPIO.IN)

hallPort = False
hallStbd = False

def readHall():
    hallPort = GPIO.input(hallPortPin)
    hallStbd = GPIO.input(hallStbdPin)

    print("port:" + str(hallPort))
    print("stbd:" + str(hallStbd))


def servo_action():
    # angle_f1 = float(control_angles.rudder_angle)
    angle_f1 = float(pwm_values.ch1)
    duty1= 100 - ((angle_f1 / 180) * duty_span + duty_min) 
    PWM.set_duty_cycle(servo_pin1, duty1)

    # angle_f2 = float(control_angles.ballast_angle)
    angle_f2 = float(pwm_values.ch1)
    duty2= 100 - ((angle_f2 / 180) * duty_span + duty_min) 
    PWM.set_duty_cycle(servo_pin2, duty2)

def serial_exchange():
    # print("Serial exchange")
    if ser.isOpen():
        # print("Serial still open")
        try:
            data = bytearray()
            if(ser.in_waiting):
                while(ser.in_waiting):
                    byte = ser.read(1)
                    # if(byte == b' '):
                    #     print("!space!")
                        # data.extend(byte)
                        # break
                    data.extend(byte)
                    
                    # print(len(data))
                # data = ser.read(24)
            print("print(len(data))")
            print(len(data))
            print("data: ")
            print(data)
            # if len(data) == 18:
            print("Decodeing ")
            pwm_values.ParseFromString(data) # Receiving a single float
            # print("When gotten")
            print("Ch1: " + str(pwm_values.ch1))
            print("Ch2: " + str(pwm_values.ch2))
            print("Ch3: " + str(pwm_values.ch3))
            print("Ch4: " + str(pwm_values.ch4))
            print("Ch5: " + str(pwm_values.ch5))
            print("Ch6: " + str(pwm_values.ch6))

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print(str(e))
    else:
        # print("Serial is no longer open")
        pass


if __name__ == '__main__':
    try:
        while True:
            serial_exchange()
            readHall()
            servo_action()
            
        # pass
    except KeyboardInterrupt:    
        PWM.stop(servo_pin1)
        PWM.stop(servo_pin2)
        PWM.cleanup()
        # pass