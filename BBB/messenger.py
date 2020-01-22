import PWM_read as PWM_read
import comms_pb2 as comms
import comms_pb2_grpc as comms_grpc
import Constants as CONST
import logger as LOG
import socket
from concurrent import futures
import grpc as gRPC




__pwm_reader = PWM_read.PWM_Reader()
__vessel_state_out = comms.vessel_state()
__vessel_state_in = comms.vessel_state()
__s = socket.socket()
__s.bind( (CONST.OWN_IP, CONST.TRIM_PORT) )
server = gRPC.server(futures.ThreadPoolExecutor(max_workers=10))

class Messenger(comms_grpc.WebserverServicer):
    def put_message(self, request, context):
        """
        gRPC servicer method - check gRPC for documentation
        Called asynchronously by the client (web_server.py)
        """
        state = make_msg()
        LOG.LOG_D("Request")
        LOG.LOG_M(state)
        return state

    def get_put_message(self, request, context):
        """
        gRPC servicer method - check gRPC for documentation
        Called asynchronously by the client (web_server.py)
        """
        __vessel_state_out = make_msg()
        
        __vessel_state_in = request

        LOG.LOG_D("Request")
        LOG.LOG_M(__vessel_state_out)
        return __vessel_state_out
        

messenger = Messenger()

def init():
    """
    Initializes gRPC server
    """
    comms_grpc.add_WebserverServicer_to_server(messenger, server)
    comms_grpc.add_TeensyserverServicer_to_server(messenger, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    LOG.LOG_I("Messenger is ready!")

def serve():
    """
    UNTESTED
    Sends protobuf message over the socket connection to the trim tab
    """
    __send_msg(make_msg())

def make_msg():
    """
    Fills out the protobuf message with info
    :returns [proto.vessel_state] filled out vessel state
    """
    vessel_state = comms.vessel_state()
    vessel_state.device_id = comms.BBB
    vessel_state.state = comms.MAN_CTRL
    vessel_state.curHeelAngle = 0
    vessel_state.maxHeelAngle = CONST.MAX_HEEL_ANGLE
    #__pwm_reader.get_manctr_val()
    vessel_state.controlAngle = 0
    vessel_state.windAngle = 0
    vessel_state.vIn = 0
    vessel_state.hallPortTrip = False
    vessel_state.hallStbdTrip = False

    return vessel_state

def __send_msg(vessel_state):
    """
    Serializes the vessel_state message and sends it on the socket
    :param [proto.vessel_state] vessel_state made by make_msg
    """
    try:
        __s.send(vessel_state.SerializeToString())
        #https://batchloaf.wordpress.com/2014/01/02/simple-communication-with-a-tcpip-device-using-python/
    except Exception as e:
        # LOG.LOG_W("Send failed, error: " + str(e))
        # stringified = str(__vessel_state_out)
        # LOG.LOG_M(stringified)
        pass

def __rcv_msg():
    """
    UNTESTED, UNUSED.
    Receives message from socket and deserializes it
    """
    __vessel_state_in.ParceFromString(__s.recv(CONST.BUFFER_SIZE))
    

def cleanup():
    """
    Perfroms messaging cleanup in case we restart
    """
    server.wait_for_termination()
    __pwm_reader.cleanup()
    __s.close()
    

