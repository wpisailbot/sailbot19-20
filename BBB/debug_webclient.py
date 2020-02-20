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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc

from gRPC import MessagesServices_pb2 as ms
from gRPC import MessagesServices_pb2_grpc as ms_grpc
from gRPC import ArduinoMessages_pb2 as PWMmsgs
from gRPC import ArduinoMessages_pb2_grpc as PWMmsgs_grpc

def stringify_proto_flask(proto):
    string = ""    
    string = string + "<br/> apparent_trim_wind: " + str(proto.apparent_trim_wind)
    string = string + "<br/> trim_angle: " + str(proto.trim_angle)
    string = string + "<br/> rudder_angle: " + str(proto.rudder_angle)
    string = string + "<br/> ballast_angle: " + str(proto.ballast_angle)
    string = string + "<br/> PWM: "
    string = string + "     <br/> CH1: " + str(proto.pwm_values.ch1)
    string = string + "     <br/> CH2: " + str(proto.pwm_values.ch2)
    string = string + "     <br/> CH3: " + str(proto.pwm_values.ch3)
    string = string + "     <br/> CH4: " + str(proto.pwm_values.ch4)
    string = string + "     <br/> CH5: " + str(proto.pwm_values.ch5)
    string = string + "     <br/> CH6: " + str(proto.pwm_values.ch6)

    return string

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ms_grpc.WebserverStub(channel)
        response = stub.MakeServerRequest(ms.Server_request(req=True))
    print(stringify_proto_flask(response))


if __name__ == '__main__':
    logging.basicConfig()
    run()