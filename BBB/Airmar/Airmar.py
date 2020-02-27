import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

class AirmarReaderServicer(ms_grpc.AirmarReaderServicer):
    def __init__(self):
        pass
    def GetAirmarData(self, request, context):
        AirmarData = ms.AirmarData()

        print("Servicing request")

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
        print("Filled out variable")
        return AirmarData


serverAirmar = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
ms_grpc.add_AirmarReaderServicer_to_server(AirmarReaderServicer(), serverAirmar)
serverAirmar.add_insecure_port('localhost:50051')
serverAirmar.start()
serverAirmar.wait_for_termination() # blocking code - comment out when want to do other stuff