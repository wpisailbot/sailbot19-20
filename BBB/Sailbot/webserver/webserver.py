"""
This is the webserver with the debug information. It uses templates created using TOPOL.io.
To access the webpage published by this server, connect to the boat's wifi network and navigate to the IP of the BBB, port 5000, and subpage you want.
"""

from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc
from gRPC import TrimTabMessages_pb2 as tt
from gRPC import TrimTabMessages_pb2_grpc as tt_grpc
import grpc
import Constants as CONST
from flask import Flask, render_template
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

@app.route("/Subsystem_state")
def Subsystem_state():
    """
    Flask server
    :returns [string] stringified proto.vessel_state returned by the gRPC client routine
    """
    responsePWM = PWMmsgs.PWMValues()
    responseControlAngles = PWMmsgs.ControlAngles()
    responseTrimState = tt.TrimState()
    responseApparentWind = tt.ApparentWind_Trim()
    responseSensors = ms.BBBSersorData()
    
    with grpc.insecure_channel('localhost:50053') as channel:
        stubPWM = ms_grpc.BBBSensorReaderStub(channel)
        responseSensors = stubPWM.GetSensorData(ms.Server_request(req=True))
    with grpc.insecure_channel('localhost:50052') as channel:
        stubPWM = ms_grpc.PWMReaderStub(channel)
        responsePWM = stubPWM.GetPWMValues(ms.Server_request(req=True))
        responseControlAngles = stubPWM.GetControlAngles(ms.Server_request(req=True))
    with grpc.insecure_channel('localhost:50050') as channel:
        stubTrim = ms_grpc.TrimTabGetterStub(channel)
        responseTrimState = stubTrim.GetTrimState(ms.Server_request(req=True))
        responseApparentWind = stubTrim.GetApparentWind(ms.Server_request(req=True))

    return render_template('Subsystem_state.html',    
                                            ch1                 = str(responsePWM.ch1),
                                            ch2                 = str(responsePWM.ch2),
                                            ch3                 = str(responsePWM.ch3),
                                            ch4                 = str(responsePWM.ch4),
                                            ch5                 = str(responsePWM.ch5),
                                            ch6                 = str(responsePWM.ch6),
                                            rudder_ctrl_angle   = str(responseControlAngles.rudder_angle),
                                            ballast_ctrl_angle  = str(responseControlAngles.ballast_angle),
                                            trim_ctrl_angle     = str(responseTrimState.control_angle),
                                            trim_state          = str(responseTrimState.state),
                                            apparent_wind       = str(responseApparentWind.apparent_wind))

@app.route("/Airmar")
def Airmar():
    """
    Flask server
    :returns [string] stringified proto.vessel_state returned by the gRPC client routine
    """
    response = ms.AirmarData()
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ms_grpc.AirmarReaderStub(channel)
        response = stub.GetAirmarData(ms.Server_request(req=True))
    return render_template('Airmar.html',    
                                            aw_speed        = str(response.apparentWind.speed),
                                            aw_direction    = str(response.apparentWind.direction),
                                            tw_speed        = str(response.theoreticalWind.speed),
                                            tw_dir          = str(response.theoreticalWind.direction),
                                            baro_press      = str(response.baro_press),
                                            air_temp        = str(response.temperature.air_temp),
                                            wind_chill      = str(response.temperature.wind_chill),
                                            lat             = str(response.gps.lat),
                                            lon             = str(response.gps.lon),
                                            alt             = str(response.gps.alt),
                                            ground_speed    = str(response.gps.ground_speed),
                                            ground_course   = str(response.gps.ground_course),
                                            compass_x       = str(response.compass.x),
                                            compass_y       = str(response.compass.y),
                                            compass_z       = str(response.compass.z),
                                            accel_x         = str(response.acceleration.x),
                                            accel_y         = str(response.acceleration.y),
                                            accel_z         = str(response.acceleration.z),
                                            phi_dot         = str(response.rateGyros.phi_dot),
                                            theta_dot       = str(response.rateGyros.theta_dot),
                                            psi_dot         = str(response.rateGyros.psi_dot),
                                            pitch           = str(response.pitchRoll.pitch),
                                            roll            = str(response.pitchRoll.roll),
                                            rel_hum         = str(response.rel_hum))

# def run():
#     """
#     Runs the Flask server and manages exceptions
#     """
#     try:
#         publish()
#     except (KeyboardInterrupt, SystemExit):
#         raise
#     except Exception as e:
#         print("gRPC not available - " + str(e))
#     # run_simple('192.168.7.2', 5000, app, use_reloader=True)
#     app.run(host=CONST.OWN_IP, threaded=True)

# try:
#     while True:
#         run()
# except KeyboardInterrupt:
#     print("Keyboard Interrupt")
#     sys.exit(0)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host=CONST.OWN_IP, threaded=True)