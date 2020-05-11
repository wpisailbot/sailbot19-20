"""
This code communicates with the Teensy in the Rigid Sail. This code has mostly been tested with the actual hardware,
but there are some things that are still not certainly working.
"""
import socket
import sys
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc



# Create a socket for talking with the Teensy
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set socket options. This was an attempt to resolve issues with socket not getting released the code would stop. I don't think this fixed the issue, but it also didn't really hurt anything either.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the ip and port
s.bind((CONST.OWN_IP, CONST.TRIM_PORT))
print("bound")
# Liste for connections from other devices. This is where the Teensy connects. This code is blocking, so nothing will happen until something connects.
s.listen(1)
# Accept the incoming connection and get the address
conn, addr = s.accept()
print("connecting to ", addr)

# Container variables. Should be phased out since you can write directly to probobuf fields.
aw_data = None # Apparent wind from Teensy
ca_data = None # Control angle for Teensy

# Create a protobuf to store teensy state values and fill it in with dummy values.
# NOTE: filling protobufs with 0s seems to result in a completely empty structure that will not be properly decoded on the other side.
trim_state = tt.TrimState()
trim_state.control_angle = 90
trim_state.state = tt.TrimState.TRIM_STATE.MANUAL

# Create a protobuf to store apparent wind values and fill it in with dummy values.
# NOTE: filling protobufs with 0s seems to result in a completely empty structure that will not be properly decoded on the other side.
apparent_wind = tt.ApparentWind_Trim()
apparent_wind.apparent_wind = 1024/2 # this should be middle



# gRPC class for responding to requests
class TrimTabGetterServicer(ms_grpc.TrimTabGetterServicer):
    def __init__(self):
        pass
    def SetTrimTabSetting(self, request, context):
        trim_state = request
        return apparent_wind

    def GetTrimState(self, request, context):
        return trim_state

    def GetApparentWind(self, request, context):
        return apparent_wind


# Start and attach server
serverTrim = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
ms_grpc.add_TrimTabGetterServicer_to_server(TrimTabGetterServicer(), serverTrim)
serverTrim.add_insecure_port('localhost:50050') # Make sure that the port is unique (not used by any other servers on the board)
serverTrim.start()

try:
    while True:
        # Create variable to store info we are about to receive from the Teensy
        receivedData = tt.ApparentWind_Trim()

        # Receive data from Teensy 32 bytes at a time.
        # The size of the data is not deterministic and something similar to how it is done with Arduino can be done where you pause when done sending data.
        # Flags could also work.
        data = conn.recv(32)

        if data:
            receivedData.ParseFromString(data) # Parse data from string garble to protobuf variable

        # Extract out the apparent wind information. Not necessary since you can just keep everything in the protobuf, but left over from trying to get this to work.
        aw_data = receivedData.apparent_wind
        print("Apparent Wind: " + str(aw_data))
        if not aw_data:
            pass
        
        # Create data to send
        sendData = tt.TrimState()
        try:
            # Fill in trim state data - this will ideal come from PWM_IO.py
            print("Trim angle: ")
            print(ca_data)
            print("\n")
            sendData.control_angle = ca_data
            sendData.state = tt.TrimState.TRIM_STATE.MANUAL
            if trim_state.control_angle:
                # serialize data using protobuf and make it ready for sending
                stringified = trim_state.SerializeToString()
                print(len(stringified))
                # Send the entire protobuf to Teensy
                conn.sendall(stringified)
        except:
            pass
except KeyboardInterrupt:    
    # pass
    # End the socket connection when the file is interrupted
    s.shutdown(socket.SHUT_RDWR)
    s.close()
