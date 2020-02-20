from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc
import grpc
import Constants as CONST
from flask import Flask
from werkzeug.serving import run_simple
import signal
import sys

app = Flask(__name__)

count = 0

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    sys.exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

def stringify_proto_flask(proto):
    string = ""    
    string = string + "<br/>apparent_trim_wind: " + str(proto.apparent_trim_wind)
    string = string + "<br/>trim_angle: " + str(proto.trim_angle)
    string = string + "<br/>rudder_angle: " + str(proto.rudder_angle)
    string = string + "<br/>ballast_angle: " + str(proto.ballast_angle)
    string = string + "<br/>PWM: "
    string = string + "<pre>&#9;</pre>CH1: " + str(proto.pwm_values.ch1)
    string = string + "<pre>&#9;</pre>CH2: " + str(proto.pwm_values.ch2)
    string = string + "<pre>&#9;</pre>CH3: " + str(proto.pwm_values.ch3)
    string = string + "<pre>&#9;</pre>CH4: " + str(proto.pwm_values.ch4)
    string = string + "<pre>&#9;</pre>CH5: " + str(proto.pwm_values.ch5)
    string = string + "<pre>&#9;</pre>CH6: " + str(proto.pwm_values.ch6)

    return string

def get_mesgs():
    """
    gRPC client routine. Gets proto.vessel_state from the main program.
    :returns [string] stringified proto.vessel_state returned by the serviser
    """
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ms_grpc.WebserverStub(channel)
        response = stub.MakeServerRequest(ms.Server_request(req=True))

    return stringify_proto_flask(response)

@app.route("/")
def publish():
    """
    Flask server
    :returns [string] stringified proto.vessel_state returned by the gRPC client routine
    """
    return get_mesgs()

def run():
    """
    Runs the Flask server and manages exceptions
    """
    try:
        publish()
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print("gRPC not available - " + str(e))
    # run_simple('192.168.7.2', 5000, app, use_reloader=True)
    app.run(host=CONST.OWN_IP, threaded=True)

try:
    while True:
        run()
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    sys.exit(0)