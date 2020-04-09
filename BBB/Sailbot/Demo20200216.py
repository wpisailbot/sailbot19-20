import Adafruit_BBIO.UART as UART
import serial
import socket
import grpc
from concurrent import futures
import Constants as CONST
from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc
import signal
import logging
import sys



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UART.setup("UART2")
ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
ser.close()
ser.open()
if ser.isOpen():
    print("Serial is open")





aw_data = 0 # Apparent wind from Teensy
ta_data = 1 # Control angle for Teensy
PWMvalues = PWMmsgs.PWMValues()
PWMvalues.ch1 = 1
PWMvalues.ch2 = 1
PWMvalues.ch3 = 1
PWMvalues.ch4 = 1
PWMvalues.ch5 = 1
PWMvalues.ch6 = 1
rudderAngle = 20
ballastAngle = 50


class Webserver(ms_grpc.WebserverServicer):

    def MakeServerRequest(self, request, context):
        """
        gRPC servicer method - check gRPC for documentation
        Called asynchronously by the client (web_server.py)
        """
        state = ms.Server_response()
        state.apparent_trim_wind = aw_data
        state.trim_angle = ta_data
        state.rudder_angle = rudderAngle
        state.ballast_angle = ballastAngle
        state.pwm_values.ch1 = PWMvalues.ch1
        state.pwm_values.ch2 = PWMvalues.ch2
        state.pwm_values.ch3 = PWMvalues.ch3
        state.pwm_values.ch4 = PWMvalues.ch4
        state.pwm_values.ch5 = PWMvalues.ch5
        state.pwm_values.ch6 = PWMvalues.ch6
        return state
        
def serve():
    print("Starting web RPC server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ms_grpc.add_WebserverServicer_to_server(Webserver(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # server.wait_for_termination()

def socket_exchange(conn, PWMReads):
    # print("Socket exchange")
    receivedData = tt.ApparentWind()
    # print("Waiting for data")
    data = conn.recv(32)
    # print("Received Data")
    if data:
        receivedData.ParseFromString(data) # Receiving a single float
    aw_data = receivedData.apparent_wind
    # print("Apparent Wind: " + str(aw_data))
    if not aw_data:
        pass
    # print("Making send data")
    sendData = tt.TrimAngle()
    try:

        # print("When needed")
        # print("Ch1: " + str(PWMvalues.ch1))
        # print("Ch2: " + str(PWMvalues.ch1))
        # print("Ch3: " + str(PWMvalues.ch1))
        # print("Ch4: " + str(PWMvalues.ch1))
        # print("Ch5: " + str(PWMvalues.ch1))
        # print("Ch6: " + str(PWMvalues.ch1))
    # if(PWMReads.ch5 != 0):
        ta_data = PWMReads.ch5
        # print("Trim angle: ")
        # print(ta_data)
        # print("\n")

        sendData.control_angle = ta_data
        conn.sendall(sendData.SerializeToString())
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
            print(str(e))

def serial_exchange():
    # print("Serial exchange")
    if ser.isOpen():
        # print("Serial still open")
        try:
            data = ""
            if(ser.in_waiting):
                while(ser.in_waiting):
                    data = data + ser.read(1)
            PWMReads = PWMmsgs.PWMValues()
            print(len(data))
            if len(data) == 18:
                # print(len(data))
                PWMReads.ParseFromString(data) # Receiving a single float
                PWMvalues.ch1 = PWMReads.ch1
                PWMvalues.ch2 = PWMReads.ch2
                PWMvalues.ch3 = PWMReads.ch3
                PWMvalues.ch4 = PWMReads.ch4
                PWMvalues.ch5 = PWMReads.ch5
                PWMvalues.ch6 = PWMReads.ch6
                # print("When gotten")
                # print("Ch1: " + str(PWMvalues.ch1))
                # print("Ch2: " + str(PWMvalues.ch1))
                # print("Ch3: " + str(PWMvalues.ch1))
                # print("Ch4: " + str(PWMvalues.ch1))
                # print("Ch5: " + str(PWMvalues.ch1))
                # print("Ch6: " + str(PWMvalues.ch1))

        
            sendData = PWMmsgs.ControlAngles()

            try:
                if(PWMReads.ch2 != 0):
                    sendData.rudder_angle = PWMReads.ch2
                if(PWMReads.ch3 != 0):
                    sendData.ballast_angle = PWMReads.ch3
                # print("Rudder angle: ")
                # print(sendData.rudder_angle)
                # print("\n")

                # print("Rudder angle: ")
                # print(sendData.ballast_angle)
                # print("\n")
                sendString = sendData.SerializeToString()
                if len(sendString) == 6:
                    ser.write(sendString)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                print(str(e))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print(str(e))
    else:
        # print("Serial is no longer open")
        pass


if __name__ == '__main__':
    logging.basicConfig()
    serve()
    print("Connecting the socket")
    s.bind((CONST.OWN_IP, 50000))
    s.listen(1)
    conn, addr = s.accept()
    print("Connected")

    try:
        while True:
            serial_exchange()
            socket_exchange(conn, PWMvalues)
            
        # pass
    except KeyboardInterrupt:    
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        sys.exit(0)
        # pass
