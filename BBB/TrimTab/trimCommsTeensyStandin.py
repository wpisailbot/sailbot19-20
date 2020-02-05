import socket
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc
import signal
import random


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (CONST.OWN_IP, 50000)

s.connect(server_address)


try:
    while True:
        sendData = tt.ApparentWind()
        sendData.apparent_wind = random.random()*10
        print("Apparent Wind: " + str(sendData.apparent_wind))
        s.sendall(sendData.SerializeToString()) # Receiving a single float
        recvData = tt.ControlAngle()
        recvData.ParseFromString(s.recv(32))
        if not recvData.control_angle:
            pass
        print("Control Angle: " + str(recvData.control_angle))
except KeyboardInterrupt:    
    s.close()