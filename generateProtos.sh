#!/bin/bash

PROTOC_PATH=protoc.exe # modify this if your protoc is in a different place
NANOPB_PATH=../nanopb*/generator-bin/protoc # moodify this if your nanopb copy is elsewhere

# Generate BBB proto files
$PROTOC_PATH -I=Protos --python_out=BBB/Sailbot/gRPC Protos/*.proto
py -3 -m grpc_tools.protoc -I=Protos --python_out=BBB/Sailbot/gRPC --grpc_python_out=BBB/Sailbot/gRPC Protos/*.proto

# Generate Teensy proto files
$NANOPB_PATH --nanopb_out=./custom_libraries/nanopb-lib/ Protos/TrimTabMessages.proto
# $NANOPB_PATH --nanopb_out=./custom_libraries/nanopb-lib/ Protos/ArduinoMessages.proto # Uncomment if you've changed the protos to depend on this file
$PROTOC_PATH -I=Protos --python_out=Teensy/Simulator Protos/TrimTabMessages.proto