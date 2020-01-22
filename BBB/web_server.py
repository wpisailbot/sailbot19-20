from flask import Flask
import comms_pb2 as comms
import comms_pb2_grpc as comms_grpc
import grpc as gRPC
import logger as LOG
import Constants as CONST
from werkzeug.serving import run_simple

app = Flask(__name__)

count = 0

def get_mesgs():
    """
    gRPC client routine. Gets proto.vessel_state from the main program.
    :returns proto.vessel_state returned by the serviser
    """
    with gRPC.insecure_channel('localhost:50051') as channel:
        stub = comms_grpc.WebserverStub(channel)
        response = stub.put_message(comms.server_req(succ=True))

    return response

@app.route("/")
def publish():
    """
    Flask server
    :returns [string] stringified proto.vessel_state returned by the gRPC client routine
    """
    LOG.LOG_D("Count: " + str(count))
    return CONST.stringify_proto_flask(get_mesgs())

@app.route("/teensy")
def publish():
    """
    Flask server
    :returns [string] stringified proto.vessel_state returned by the gRPC client routine
    """
    LOG.LOG_D("Count: " + str(count))
    return get_mesgs()

def run():
    """
    Runs the Flask server and manages exceptions
    """
    try:
        LOG.LOG_I("Requesting info")
        publish()
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        LOG.LOG_W("gRPC not available - " + str(e))
    # run_simple('192.168.7.2', 5000, app, use_reloader=True)
    app.run(host='192.168.7.2', threaded=True)

try:
    while True:
        run()
except KeyboardInterrupt:
    LOG.LOG_I("Keyboard Interrupt")