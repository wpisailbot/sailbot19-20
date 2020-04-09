import socket
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc



# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# s.bind((CONST.OWN_IP, 50000))
# s.listen(1)
# conn, addr = s.accept()

aw_data = None # Apparent wind from Teensy
ca_data = None # Control angle for Teensy

trim_state = tt.TrimState()
trim_state.control_angle = 90
trim_state.state = tt.TrimState.TRIM_STATE.MANUAL

apparent_wind = tt.ApparentWind_Trim()
apparent_wind.apparent_wind = 1024/2

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


serverTrim = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
ms_grpc.add_TrimTabGetterServicer_to_server(TrimTabGetterServicer(), serverTrim)
serverTrim.add_insecure_port('localhost:50050')
serverTrim.start()

try:
    while True:
        receivedData = tt.ApparentWind_Trim()
        # data = conn.recv(32)
        data = None # FOR TESTING ONLY
        if data:
            receivedData.ParseFromString(data) # Receiving a single float
        aw_data = receivedData.apparent_wind
        # print("Apparent Wind: " + str(aw_data))
        if not aw_data:
            pass
        sendData = tt.TrimState()
        try:
            # print("Trim angle: ")
            # print(ca_data)
            # print("\n")
            sendData.control_angle = ca_data
            sendData.state = tt.TrimState.TRIM_STATE.MANUAL
            if sendData.control_angle:
                # conn.sendall(sendData.SerializeToString())
                pass
        except:
            pass
except KeyboardInterrupt:    
    pass
    # s.shutdown(socket.SHUT_RDWR)
    # s.close()
