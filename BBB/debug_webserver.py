# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc

from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc

aw_data = 0 # Apparent wind from Teensy
ta_data = 0 # Control angle for Teensy
PWMvalues = PWMmsgs.PWMValues()
PWMvalues.ch1 = 0
PWMvalues.ch2 = 0
PWMvalues.ch3 = 0
PWMvalues.ch4 = 0
PWMvalues.ch5 = 0
PWMvalues.ch6 = 0
rudderAngle = 0
ballastAngle = 0


class Webserver(ms_grpc.WebserverServicer):

    def MakeServerRequest(self, request, context):
        """
        gRPC servicer method - check gRPC for documentation
        Called asynchronously by the client (web_server.py)
        """
        print("servicer called")
        state = ms.Server_response()
        state.apparent_trim_wind = aw_data
        state.trim_angle = ta_data
        state.rudder_angle = rudderAngle
        state.ballast_angle = ballastAngle
        print("Done with primitives")
        state.pwm_values.ch1 = PWMvalues.ch1
        state.pwm_values.ch2 = PWMvalues.ch2
        state.pwm_values.ch3 = PWMvalues.ch3
        state.pwm_values.ch4 = PWMvalues.ch4
        state.pwm_values.ch5 = PWMvalues.ch5
        state.pwm_values.ch6 = PWMvalues.ch6
        print("Done with nested, returning")
        return state


def serve():
    print("Starting server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ms_grpc.add_WebserverServicer_to_server(Webserver(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()