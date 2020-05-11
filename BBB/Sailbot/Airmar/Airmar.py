"""
This is a stub code and must be filled out with the serial reading (USB) and parsing code.
The code presented in this file now shows how to fill out the protobuf and reply with it when a request comes in.
The code currently waits for termination, but the more logical thing to do would be to continuasly read the serial data.
Other modules will be useful examples of how to get this to a more operational state.
"""
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc

# gRPC class - required for modularization
class AirmarReaderServicer(ms_grpc.AirmarReaderServicer):
    def __init__(self):
        pass
    
    def GetAirmarData(self, request, context):
        # Replies to a request for the Airmar data

        # Create protobuf data container
        AirmarData = ms.AirmarData()

        # Fill out the protobuf with dummy data
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

        # Reply with filled out protobuf
        return AirmarData


# Create gRPC server
serverAirmar = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
# Add the servisor to server
ms_grpc.add_AirmarReaderServicer_to_server(AirmarReaderServicer(), serverAirmar)
# Attach server to local port - make sure the port is unique (not used by any other servers on the system)
serverAirmar.add_insecure_port('localhost:50051')
# Start the server
serverAirmar.start()
# Wait until the file is terminated to stop the server. This is where you read the Airmar and stuff with it. 
serverAirmar.wait_for_termination() # blocking code - comment out when want to do other stuff