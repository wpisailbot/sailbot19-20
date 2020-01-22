import comms_pb2 as comms
import comms_pb2_grpc as comms_grpc
import grpc as gRPC
import logger as LOG
import Constants as CONST
import socket

count = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def exchange_data(teensy_data):
    """
    gRPC client routine. Gets proto.vessel_state from the main program.
    :returns proto.vessel_state returned by the serviser
    """
    with gRPC.insecure_channel('localhost:5005') as channel:
        stub = comms_grpc.TeensyserverStub(channel)
        response = stub.get_put_message(ParseFromString(teensy_data))

    return response
    


def run():
    """
    """
    try:
        teensy_data = conn.recv(CONST.BUFFER_SIZE)

        if teensy_data:
            own_data = exchange_data(teensy_data)
            
            conn.send(own_data.SerializeToString())

    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        LOG.LOG_W("gRPC not available - " + str(e))



try:
    s.connect((CONST.OWN_IP, CONST.TRIM_PORT))
    s.listen(1)

    conn, addr = s.accept()
    LOG.LOG_I("Connection addr: " + str(addr))

    while True:
        run()

    conn.close()
except KeyboardInterrupt:
    LOG.LOG_I("Keyboard Interrupt")
    s.close()