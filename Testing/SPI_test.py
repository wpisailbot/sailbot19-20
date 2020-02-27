#https://gist.github.com/pdp7/33a8ad95efcbcc0fadc3f96a70d4b159
#^^ VERY IMPORTANT prereq for this to work

import subprocess
output = subprocess.check_output(['bash','-c', "config-pin P9.17 spi_cs"])
output = subprocess.check_output(['bash','-c', "config-pin P9_18 spi"])
output = subprocess.check_output(['bash','-c', "config-pin P9_21 spi"])
output = subprocess.check_output(['bash','-c', "config-pin P9.22 spi_sclk"])

from Adafruit_BBIO.SPI import SPI
import binascii
from ast import literal_eval
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
import sys

spi = SPI(1,0)

# message = "hello SPI, do I work??"

pwm_values = PWMmsgs.PWMValues()
pwm_values.ch1 = 15
pwm_values.ch2 = 16
pwm_values.ch3 = 13
pwm_values.ch4 = 14
pwm_values.ch5 = 15
pwm_values.ch6 = 3214

control_angles = PWMmsgs.ControlAngles()
control_angles.rudder_angle = 91

control_angles.ballast_angle = 92

AirmarData = ms.AirmarData()

AirmarData.apparentWind.speed           = 1.0
AirmarData.apparentWind.direction       = 2.0
AirmarData.theoreticalWind.speed        = 3.0
AirmarData.theoreticalWind.direction    = 4.0
AirmarData.baro_press                   = 5.0
AirmarData.temperature.air_temp         = 6.0
AirmarData.temperature.wind_chill       = 7.0
AirmarData.gps.lat                      = 8.0
AirmarData.gps.lon                      = 9.0
AirmarData.gps.alt                      = 10.0
AirmarData.gps.ground_speed             = 11.0
AirmarData.gps.ground_course            = 12.0
AirmarData.compass.x                    = 13.0
AirmarData.compass.y                    = 14.0
AirmarData.compass.z                    = 15.0
AirmarData.acceleration.x               = 16.0
AirmarData.acceleration.y               = 17.0
AirmarData.acceleration.z               = 18.0
AirmarData.rateGyros.phi_dot            = 19.0
AirmarData.rateGyros.theta_dot          = 20.0
AirmarData.rateGyros.psi_dot            = 21.0
AirmarData.pitchRoll.pitch              = 22.0
AirmarData.pitchRoll.roll               = 23.0
AirmarData.rel_hum                      = 24.0 

message = AirmarData.SerializeToString()

def str2SPI(msg):
    int_array = []

    for letter in repr(msg):
        int_array.append(int(binascii.hexlify(letter),16))
    
    return int_array

def SPI2str(spi_msg):
    message = ""
    for x in spi_msg:
        message = message + binascii.unhexlify(hex(x)[2:])
    
    return literal_eval(message)

print("Message: ")
print(repr(message))
print("sized:")
print(str(sys.getsizeof(message)))
print("By parts: ")
print("Ch1: " + str(pwm_values.ch1))
print("Ch2: " + str(pwm_values.ch2))
print("Ch3: " + str(pwm_values.ch3))
print("Ch4: " + str(pwm_values.ch4))
print("Ch5: " + str(pwm_values.ch5))
print("Ch6: " + str(pwm_values.ch6))
spi_msg = str2SPI(message)
print("SPI sent")
print(spi_msg)
print("sized:")
print(str(sys.getsizeof(spi_msg)))

returned_msg = spi.xfer2(spi_msg)
print("SPI Returned")
print(returned_msg)

stringified_msg = SPI2str(returned_msg)

decodedProto = ms.AirmarData()
decodedProto.ParseFromString(stringified_msg)

print(str(decodedProto))
# print("ballast_angle: " + str(decodedProto.ballast_angle))
# print("Ch3: " + str(decodedProto.ch3))
# print("Ch4: " + str(decodedProto.ch4))
# print("Ch5: " + str(decodedProto.ch5))
# print("Ch6: " + str(decodedProto.ch6))

spi.close()